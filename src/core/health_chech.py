from django.urls import URLPattern, URLResolver, get_resolver
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from src.modules.common.presentation.api_messages import API_MESSAGES


def _collect_urls(resolver: URLResolver, prefix: str = "") -> list[str]:
    endpoints = []

    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            endpoints.extend(_collect_urls(pattern, prefix + str(pattern.pattern)))
        elif isinstance(pattern, URLPattern):
            path = (prefix + str(pattern.pattern)).lstrip("^").rstrip("$")

            if not path.startswith("admin/"):
                endpoints.append(path)

    return endpoints


@extend_schema(
    summary="Health check",
    responses={
        200: OpenApiResponse(
            inline_serializer(
                name="HealthCheckResponse",
                fields={
                    "status": serializers.CharField(),
                    "endpoints": serializers.ListField(child=serializers.CharField()),
                },
            ),
            description=API_MESSAGES["OK"],
        ),
    },
    tags=["health"],
)
@api_view(["GET"])
def health_check(request: Request) -> Response:
    resolver = get_resolver()
    endpoints = _collect_urls(resolver)
    return Response({"status": "ok", "endpoints": endpoints}, status=status.HTTP_200_OK)
