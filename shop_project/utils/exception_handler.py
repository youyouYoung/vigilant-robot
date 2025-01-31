from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.http import JsonResponse
import logging
import traceback
import json

# Configure a logger for error handling
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    request = context.get("request")

    # If response is None, handle it as a server error
    if response is None:
        # Log the error
        logger.error(f"Exception Handler - Error: {str(exc)}, Context: {str(context)}, An exception occurred:\n{traceback.format_exc()}")

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
        try:
            body = request.body.decode("utf-8")
        except Exception:
            body = "[无法解析]"

        if request:
            # 获取请求方法
            method = request.method
            # 获取请求路径
            path = request.get_full_path()
            # 获取请求头
            headers = dict(request.headers)
            # 记录日志
            log_data = {
                "method": method,
                "path": path,
                "headers": headers,
                "body": body,
                "exception": str(exc),
            }
            logger.error(f"ValidationError: {json.dumps(log_data, ensure_ascii=False)}")

        return JsonResponse({
            "error": "Validation Error",
            "message": exc.default_detail,
            "details": {field: error_list[0] if error_list else "Unknown error"
                               for field, error_list in exc.detail.items()} if hasattr(exc, 'detail') else {}
        }, status=response.status_code)

    # For other errors, follow the same structure
    return JsonResponse({
        "error": response.status_text,
        "message": response.data.get("detail", "An error occurred")
    }, status=response.status_code)
