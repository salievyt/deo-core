from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        errors = response.data
        response.data = {
            "message": str(errors.get("detail", "Проверьте заполненные поля."))
            if isinstance(errors, dict)
            else "Проверьте заполненные поля.",
            "errors": errors,
        }
    return response
