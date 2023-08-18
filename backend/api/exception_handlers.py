from rest_framework.views import exception_handler

from django.http import Http404


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        custom_response_data = {"detail": "Страница не найдена."}
        response.data = custom_response_data
    elif exc.status_code == 403:
        custom_response_data = {
            "detail": "Недостаточно прав для выполнения данного действия."
        }
        response.data = custom_response_data
    elif exc.status_code == 401:
        custom_response_data = {
            "detail": "Учетные данные не были предоставлены."
        }
        response.data = custom_response_data

    return response
