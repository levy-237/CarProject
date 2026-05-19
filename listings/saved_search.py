from django.http import QueryDict

from users.models import savedSearch
from listings.models import Listing
from listings.filters import ListingFilter


def listing_matches_any_saved_search(listing):
    base_queryset = Listing.objects.filter(id=listing.id)
    matched_searches = []
    

    for search in savedSearch.objects.all():
        print(search)
        data = QueryDict(search.saved_url)

        filterset = ListingFilter(
            data=data,
            queryset=base_queryset
        )

        if filterset.is_valid() and filterset.qs.exists():
            if search not in matched_searches:
                matched_searches.append(search)

    return matched_searches