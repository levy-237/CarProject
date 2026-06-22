from django.conf import settings
from ollama import Client
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from listings.models import Listing
from rest_framework import status
from .aiAdvisor import AiAdvisor
from .aiComparator import AiComparator
from listings.filters import ListingFilter
from listings.serializers import ListingListDetailSerializer
from users.models import City, Province


# Translates the AI advisor's hard_filters keys into ListingFilter param names.
# Kept separate from the prompt so filter naming and AI output can evolve independently.
SORT_MAP = {
    "price_asc": "price",
    "price_desc": "-price",
    "year_desc": "-makeyear",
    "date_desc": "-publish_date",
    "kilometers_asc": "mileage",
    "range_desc": "-real_summer_range",
    "dc_charging_desc": "-model_trim__max_dc_charge_kw",
}
def build_filter_data(hard_filters):
    data = {}
    if not hard_filters:
        return data

    list_map = {
        "brand": "brand",
        "model": "model",
        "body_type": "body",
        "condition": "condition",
        "drivetrain": "drivetrain",
    }
    for src, dest in list_map.items():
        value = hard_filters.get(src)
        if value:
            data[dest] = value if isinstance(value, list) else [value]

    scalar_map = {
        "price_min": "minprice",
        "price_max": "maxprice",
        "year_min": "mindate",
        "year_max": "maxdate",
        "kilometers_min": "minmileage",
        "kilometers_max": "maxmileage",
        "power_min": "minpower",
        "power_max": "maxpower",
        "battery_capacity_min": "minbattery",
        "battery_capacity_max": "maxbattery",
        "summer_range_min": "minsummerrange",
        "winter_range_min": "minwinterrange",
        "dc_charging_power_min": "mindccharging",
        "ac_charging_power_min": "minaccharging",
    }
    for src, dest in scalar_map.items():
        value = hard_filters.get(src)
        if value is not None:
            data[dest] = value

    bool_map = {
        "heat_pump": "heatpump",
        "warranty": "garantie",
        "pickerl": "pickerl",
    }
    for src, dest in bool_map.items():
        value = hard_filters.get(src)
        if value is not None:
            data[dest] = value

    if hard_filters.get("search"):
        data["search"] = hard_filters["search"]

    # AI returns location names; the filter expects DB IDs.
    city_name = hard_filters.get("city")
    if city_name:
        city_ids = list(
            City.objects.filter(name__iexact=city_name).values_list("id", flat=True)
        )
        if city_ids:
            data["city"] = city_ids

    province_name = hard_filters.get("province")
    if province_name:
        province_ids = list(
            Province.objects.filter(name__iexact=province_name).values_list("id", flat=True)
        )
        if province_ids:
            data["province"] = province_ids

    return data


def build_advisor_response(reply, matched_listings):
    default = {
        "message": "",
        "listing_reasons": [],
        "suggested_filter_relaxations": [],
        "suggested_follow_up_questions": [],
        "matched_listings": matched_listings,
    }

    try:
        parsed = json.loads(reply)
    except json.JSONDecodeError:
        default["message"] = "Sorry, I couldn't format that response. Please try again."
        default["parse_error"] = True
        return default

    default["message"] = parsed.get("message", "")
    default["listing_reasons"] = parsed.get("listing_reasons", [])
    default["suggested_filter_relaxations"] = parsed.get("suggested_filter_relaxations", [])
    default["suggested_follow_up_questions"] = parsed.get("suggested_follow_up_questions", [])
    return default


class ChatBot(APIView):
    def post(self, request):
        base_queryset = Listing.objects.for_advisor()
        question = request.data.get("question")
        history = request.data.get("history") or []
        
        if not question:
            return Response({"error": "Pass a question in the JSON body as question."}, status=400)


        if not isinstance(history, list):
            return Response({"error": "history must be a list."}, status=400)

        advisor_response = AiAdvisor(question, history=history)
        # print(advisor_response)
        data = json.loads(advisor_response)

        # The planner decided this question is not a listing search.
        # Quit early so we skip filtering, serialization and the expensive advisor LLM call.
        require_advisor = data.get("require_advisor")
        hard_filters = {}
        soft_preferences = {}
        matched_listings = []
        
        if require_advisor:
            hard_filters = data.get("hard_filters") or {}
            soft_preferences = data.get("soft_preferences") or {}
            sort = data.get("sort") 
            
            print(hard_filters)
            print(soft_preferences)
            filter_data = build_filter_data(hard_filters)
            print("filter_data:", filter_data)
            filterset = ListingFilter(
                    data=filter_data,
                    queryset=base_queryset
                )
            order_field = SORT_MAP.get(sort)
            listings = filterset.qs if filterset.is_valid() else base_queryset.none()
            
            if order_field:
                listings = listings.order_by(order_field)
            serializer = ListingListDetailSerializer(
                    listings[:15],
                    many=True,
                    context={"request": request},  
                )
            
            matched_listings = serializer.data

            
        ADVISOR_SYSTEM_PROMPT = ADVISOR_SYSTEM_PROMPT = """
You are the eAutoKauf AI buying advisor.

Your job is to explain matched electric-car listings to the user based ONLY on the data provided by the backend.

You are not allowed to invent listings, specs, prices, features, availability, battery health, accident history, service history, warranty, or seller claims.

If the original_question is mostly German, the entire response must be in German.
If the original_question is mostly English, respond in English.

Conversation history:
- history may contain earlier turns with sender and message from the client.
- Use it to resolve follow-ups such as "the first one" or "cheaper options".
- original_question is the latest user message.

Return ONLY valid JSON.
Do not use markdown.
Do not include text outside the JSON.

Conversation modes (decide first):
- If require_advisor is false: the user did NOT ask for a listing search. There are no listings to discuss. Just answer the user's question helpfully and conversationally, but ONLY within the context of cars and electric vehicles (general EV advice, charging, batteries, ownership, buying guidance, how the marketplace works, etc.). Put your full reply in "message" and leave listing_reasons, suggested_filter_relaxations and suggested_follow_up_questions empty. Do NOT mention filters, matches, or "no results" in this mode. If the question is not about cars or electric vehicles at all, politely say you can only help with cars and electric vehicles.
- If require_advisor is true and matched_listings is empty: this WAS a listing search but nothing matched. Explain that no exact matches were found and suggest which filters could be relaxed.
- If require_advisor is true and matched_listings is not empty: explain and rank the matched listings as described below.

Tone:
- Helpful, clear, practical.
- Short and buyer-focused.
- Use the same language as the user if obvious. If the user writes German, answer in German. If English, answer in English.
- Do not sound overly certain. Use phrases like "based on the available listing data".

Core rules:
- Only discuss listings included in matched_listings.
- If require_advisor is true and matched_listings is empty, explain that no exact matches were found and suggest which filters could be relaxed.
- If matched_listings is weak, limited, or not an exact fit, mention that in message.
- Use hard_filters as strict requirements already applied by the backend.
- Use soft_preferences to explain why some listings are better matches than others.
- Mention trade-offs clearly.
- Mention missing data when relevant.
- Do not guarantee that a car is good, safe, reliable, or the best deal.
- Always recommend verifying important details with the seller.
- For used EVs, remind users to check battery warranty/health when relevant.
- Do not provide legal, financial, or technical guarantees.

Ranking logic:
- Prioritize listings that best match the user's original request and soft_preferences.
- For family needs, prefer practical body types, range, warranty, low kilometers, newer year, and usable space.
- For city use, prefer compact body type, lower price, efficiency, and easy daily usability.
- For long-distance use, prefer higher range, winter range, DC charging power, battery capacity, and heat pump.
- For winter use, prefer heat pump, winter range, all-wheel drive if available, and battery/range buffer.
- For budget requests, explain value carefully: lower price, acceptable range, mileage/year trade-offs.
- For fast charging requests, compare dc_charging_power if available.
- For "range" requests, use summer_range/winter_range according to the filter plan.
- If data is missing for an important criterion, include that as a warning.

Message behavior:
- The message must summarize the result in natural language.
- If suggested_filter_relaxations is not empty, include the most useful 1-2 relaxations naturally in the message.
- If suggested_follow_up_questions is not empty, include the most useful 1 follow-up question naturally at the end of the message.
- Do not repeat every listing detail in message; listing-specific details belong in listing_reasons.
- Keep message concise: usually 2-5 sentences.

Output schema:
{
  "message": "",
  "listing_reasons": [
    {
      "listing_id": 0,
      "rank": 1,
      "match_score": 0,
      "reason": "",
      "strengths": [],
      "tradeoffs": [],
      "warnings": []
    }
  ],
  "suggested_filter_relaxations": [],
  "suggested_follow_up_questions": []
}

Field rules:
- message: short user-facing summary of what was found, how it matches the request, and any key relaxation/follow-up if useful.
- listing_reasons: include up to 5 best listings only.
- listing_id: must match an ID from matched_listings.
- rank: 1 is best.
- match_score: integer from 0 to 100 based on fit to the request. Do not use decimals.
- reason: concise buyer-facing explanation.
- strengths: concrete positives from listing data only.
- tradeoffs: possible downsides from listing data only.
- warnings: missing/uncertain things the buyer should verify.
- suggested_filter_relaxations: if results are weak, limited, or empty, suggest filters to relax.
- suggested_follow_up_questions: useful next questions the user could answer.

If require_advisor is true and matched_listings is empty, return:
{
  "message": "No exact matches were found. Try relaxing one or two requirements, for example increasing the budget, allowing more body types, lowering the range requirement, or widening the location. What is the most important requirement for you: price, range, space, or charging speed?",
  "listing_reasons": [],
  "suggested_filter_relaxations": ["Increase budget", "Allow more body types", "Lower range requirement", "Widen location"],
  "suggested_follow_up_questions": ["What is the most important requirement for you: price, range, space, or charging speed?"]
}

If require_advisor is false, return only a conversational car/EV answer, for example:
{
  "message": "<your helpful answer about cars or electric vehicles, in the user's language>",
  "listing_reasons": [],
  "suggested_filter_relaxations": [],
  "suggested_follow_up_questions": []
}

Never output IDs that were not provided.
Never mention internal field names like hard_filters or soft_preferences to the user unless necessary.
Never say "the database says"; say "based on the available listing data".
"""


        advisor_payload = {
            "original_question": question,
            "history": history,
            "require_advisor": bool(require_advisor),
            "soft_preferences": soft_preferences,
            "matched_listings": matched_listings,
        }
        
        ADVISOR_USER_PROMPT = json.dumps(advisor_payload, ensure_ascii=False)
        print(advisor_payload)
        print("--- FINISHED ---- ")

        client = Client(
            host='https://ollama.com',
            headers={'Authorization': 'Bearer ' + settings.OLLAMA_API_KEY}
        )

        messages = [
            {
                'role': 'system',
                'content': ADVISOR_SYSTEM_PROMPT,
            },
            {
                'role': 'user',
                'content': ADVISOR_USER_PROMPT,
            },
        ]

        reply = ""
        for part in client.chat(settings.AI_MODEL, messages=messages, stream=True):
            chunk = part.message.content
            # print(chunk, end='', flush=True)  # live output in the server console
            reply += chunk
            
        print(reply)
        return Response(build_advisor_response(reply, matched_listings))


class Comparator(APIView):
    def post(self, request):
        ids_arr = request.data.get("question")
        
        if not ids_arr or len(ids_arr) < 2:
            return Response({"detail":"Please provide at least two listings"}, status=400)
            
        listings = Listing.objects.online().filter(id__in = ids_arr)
        
        if not listings or listings.count() < 2:
            return Response({"detail":"at least two listings could not be found"}, status=400)
        
        serializer = ListingListDetailSerializer(
            listings,
            many=True,
            context={"request": request},  
        )
        
        comparable_listings = serializer.data
        
        comparation_response = AiComparator(comparable_listings)
        
        print(comparation_response)
        return Response({"reply": comparation_response})

