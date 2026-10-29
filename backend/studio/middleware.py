from django.conf import settings
from django.http import JsonResponse


class RequestSizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/") and request.method == "POST":
            try:
                length = int(request.META.get("CONTENT_LENGTH") or 0)
            except ValueError:
                return JsonResponse(
                    {"message": "Некорректный размер запроса."}, status=400
                )
            if length > settings.MAX_REQUEST_BYTES:
                return JsonResponse(
                    {"message": "Размер запроса превышает 6 MB."}, status=413
                )
        return self.get_response(request)
