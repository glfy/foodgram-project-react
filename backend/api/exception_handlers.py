# from rest_framework.exceptions import (
#     ValidationError as DRFValidationError,
#     PermissionDenied,
#     NotFound,
#     AuthenticationFailed,
# )

# from rest_framework.views import exception_handler as drf_exception_handler
# from django.utils.encoding import force_text
# from rest_framework import status, exceptions, serializers


# class CustomValidation(exceptions.APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = "Error"

#     def __init__(self, detail, field, status_code):
#         if status_code is not None:
#             self.status_code = status_code
#         if detail is not None:
#             self.detail = {field: force_text(detail)}
#         else:
#             self.detail = {"detail": force_text(self.default_detail)}


# def custom_exception_handler(exc, context):
#     if isinstance(exc, NotFound):
#         exc = NotFound(detail={"message": "Ошибка доступа. У вас нет прав."})
#     return drf_exception_handler(exc, context)


# # from rest_framework.views import exception_handler
# # from rest_framework.response import Response
# # from rest_framework import status
# # from rest_framework.exceptions import (
# #     ValidationError as DRFValidationError,
# #     PermissionDenied,
# #     NotFound,
# #     AuthenticationFailed,
# # )

# # from django.http.response import Http404

# # from rest_framework.views import exception_handler
# # from rest_framework.response import Response

# # from rest_framework.exceptions import APIException


# # def custom_exception_handler(exc, context):
# #     # Call REST framework's default exception handler first to get the standard error response.
# #     response = exception_handler(exc, context)

# #     # if there is an IntegrityError and the error response hasn't already been generated
# #     if isinstance(exc, NotFound):
# #         response = Response(
# #             {
# #                 "message": "It seems there is a conflict between the data you are trying to save and your current "
# #                 "data. Please review your entries and try again."
# #             },
# #             status=status.HTTP_400_BAD_REQUEST,
# #         )

# #     return response


# # # def custom_exception_handler(exc, context):
# # #     handler = {
# # #         "AuthenticationFailed": _handle_authentication_error,
# # #         "PermissionDenied": _handle_permission_error,
# # #         "NotFound": _handle_not_found_error,
# # #     }
# # #     response = exception_handler(exc, context)
# # #     print("erroororhandler**********************", response)
# # #     exception_class = exc.__class__.__name__
# # #     if response is not None:
# # #         response.data["status_code"] = response.status_code

# # #     if exception_class in handler:
# # #         return handler[exception_class](exc, context, response)
# # #     print(exception_class)
# # #     print(Response(response.data))
# # #     return Response({"error": str(exc)})


# # # def _handle_authentication_error(exc, context, response):
# # #     response.data["detail"] = "Пользователь не авторизован"
# # #     return response


# # # def _handle_permission_error(exc, context, response):
# # #     response.data["detail"] = "Недостаточно прав"
# # #     return response


# # # def _handle_not_found_error(exc, context, response):
# # #     return Response({"detail": "Объект не найден"})
# # #     Response.data["detail"] = "Объект не найден"
# # #     return response


# # # def custom_exception_handler(exc, context):
# # #     if isinstance(exc, NotFound):
# # #         exc = NotFound("Record not found")

# # #     response = exception_handler(exc, context)

# # #     if response is not None:
# # #         response.data["message"] = response.data.pop("detail", "")

# # #     return response
# # #     # if isinstance(exc, NotFound):
# # #     response = Response()
# # #     response.data["detail"] = "Страница не найдена."
# # #     response.status_code = status.HTTP_404_NOT_FOUND

# # # if response is not None:
# # #     response.data["detail"] = "Страница не найдена."
# # #     response.data["detail"] = "Страница не найдена."
# # #     if isinstance(exc, DRFValidationError):
# # #         response.data["detail"] = "Стандартные ошибки валидации DRF"
# # #     elif isinstance(exc, AuthenticationFailed):
# # #         response.data["detail"] = "Пользователь не авторизован"
# # #     elif isinstance(exc, PermissionDenied):
# # #         exc = PermissionDenied(detail={"message": "Недостаточно прав."})

# # #     if isinstance(exc, NotFound):
# # #         response.data["detail"] = "Пользователь не авторизован"
# # #         #exc = NotFound(detail={"message": "Объект не найден"})

# # # return response


# # # from rest_framework.exceptions import NotFound

# # # # Example exception instance
# # # exc = NotFound("Object not found")

# # # # Check if the exception instance is an instance of NotFound
# # # if isinstance(exc, NotFound):
# # #     print("The exception is an instance of NotFound")
# # # else:
# # #     print("The exception is not an instance of NotFound")
