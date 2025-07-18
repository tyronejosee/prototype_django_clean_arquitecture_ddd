from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


class BackpressureMiddleware:
    # Constants
    OVERLOAD_THRESHOLD: int = 90

    # Messages
    OVERLOAD_MESSAGE: str = "Server is overloaded"

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        import psutil

        if psutil.virtual_memory().percent > self.OVERLOAD_THRESHOLD:
            return HttpResponse(self.OVERLOAD_MESSAGE, status=503)
        return self.get_response(request)
