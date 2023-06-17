from rest_framework.views import exception_handler
from django.http import Http404
# from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Обработчик исключений с кастомными сообщениями
    """
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        error = {"detail": str(exc)}
        # меняем на кастомный текст исключения
        response.data = error
        # response.status_code = status.HTTP_404_NOT_FOUND
    return response
