from rest_framework.views import exception_handler

from django.http import HttpResponseForbidden, HttpResponseNotFound


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if exc.status_code == HttpResponseNotFound.status_code:
        custom_response_data = {"detail": "Страница не найдена."}
        response.data = custom_response_data
    elif exc.status_code == HttpResponseForbidden.status_code:
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
