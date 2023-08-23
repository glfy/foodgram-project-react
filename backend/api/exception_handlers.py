from django.http import HttpResponseForbidden, HttpResponseNotFound
from rest_framework.views import exception_handler


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


# я тебе писала в пачке, но ты не ответил
#  1. в джанго нет такого прописанного 401 и получается два варианта – либо
# как у меня, либо через
#  class HttpResponseUnauthorized(HttpResponse):
# def init self;
# self.status_ code = 401

# return HttpResponseUnauthorized ()

# что выглядит супер избыточным

# 2.  ты пишешь что надо использовать постгрес, но ведь мы разрабатываем на
# склайт, чтоб было проще тестить, а потом если весь код ок, то уже перед
# деплоем меняем на постгрес
# сча не вижу если честно смысла менять и прыгать с бд на бд, когда мы просто
# разбираемся с бэком

# 3. у меня импорты так как ставит айсорт, я не понимаю, как ты просишь их
# перенастроить в фильтрах
