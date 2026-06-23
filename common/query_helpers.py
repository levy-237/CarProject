def filter_by_relation(queryset, request, field_name):
    relation = request.query_params.get("relation")
    if not relation:
        return queryset
    relation_ids = [item.strip() for item in relation.split(",") if item.strip()]
    if relation_ids:
        queryset = queryset.filter(**{f"{field_name}__in": relation_ids})
    return queryset
