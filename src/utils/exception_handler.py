from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.http import JsonResponse

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # If response is None, handle it as a server error
    if response is None:
        return JsonResponse({
            "error": "Server Error",
            "message": "Something went wrong on our end"
        }, status=500)

    # Handle AuthenticationFailed exceptions
    if isinstance(exc, AuthenticationFailed):
        return JsonResponse({
            "error": exc.default_code,
            "message": exc.default_detail,
        }, status=response.status_code)

    # Handle ValidationError exceptions
    if isinstance(exc, ValidationError):
        return JsonResponse({
            "error": "Validation Error",
            "message": str(exc.detail) if hasattr(exc, 'detail') else str(exc)
        }, status=response.status_code)

    # For other errors, follow the same structure
    return JsonResponse({
        "error": response.status_text,
        "message": response.data.get("detail", "An error occurred")
    }, status=response.status_code)
