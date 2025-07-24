from django.urls import URLPattern, URLResolver, get_resolver
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


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


@api_view(["GET"])
def health_check(request: Request) -> Response:
    resolver = get_resolver()
    endpoints = _collect_urls(resolver)
    return Response({"status": "ok", "endpoints": endpoints}, status=status.HTTP_200_OK)
