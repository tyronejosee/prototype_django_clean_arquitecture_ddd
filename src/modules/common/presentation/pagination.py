from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response


def paginate_queryset(request: Request, queryset: list, serializer_class) -> Response:
    paginator = PageNumberPagination()
    paginated = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(paginated, many=True)
    return paginator.get_paginated_response(serializer.data)
