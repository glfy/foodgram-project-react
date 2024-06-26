from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CustomUserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(r"users", CustomUserViewSet, basename="users")
router_v1.register("tags", TagViewSet, basename="tags")
router_v1.register(r"recipes", RecipeViewSet)
router_v1.register("ingredients", IngredientViewSet, basename="ingredients")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
