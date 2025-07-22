from rest_framework.views import APIView


class BaseController(APIView):
    throttle_map: dict = {}

    def get_throttles(self) -> list:
        throttle_cls = self.throttle_map.get(self.request.method)
        if throttle_cls:
            return [throttle_cls()]
        return super().get_throttles()
