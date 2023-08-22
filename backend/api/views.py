from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from django.db.models import Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO

from api.paginators import PageLimitPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers.recipe import (
    IngredientSerializer,
    RecipeMinifiedSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)
from api.serializers.users import (
    CustomUserSerializer,
    UserSubscriptionsSerializer,
)
from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import User

from .filters import RecipeFilter


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all().annotate(recipes_count=Count("recipes"))
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ["get", "post", "delete"]
    pagination_class = PageLimitPagination
    filterset_class = RecipeFilter

    @action(
        detail=False,
        methods=["GET"],
    )
    def subscriptions(self, request):
        subscriber = request.user
        queryset = (
            subscriber.subscriptions.all()
            .order_by("id")
            .annotate(recipes_count=Count("recipes"))
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer = UserSubscriptionsSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserSubscriptionsSerializer(
            many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        to_subscribe = get_object_or_404(User, id=id)
        subscriber = request.user

        if to_subscribe == subscriber:
            return Response(
                {"detail": "Вы не можете подписаться на себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == "POST":
            if subscriber.subscriptions.filter(id=to_subscribe.id).exists():
                return Response(
                    {"detail": "Автор уже добавлен в подписки."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscriber.subscriptions.add(to_subscribe)
            subscriber.save()

            serializer = UserSubscriptionsSerializer(
                to_subscribe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        deleted_count = subscriber.subscriptions.remove(to_subscribe)
        if deleted_count == 0:
            return Response(
                {"detail": "Автора нет в подписках."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related("author").prefetch_related(
        "tags", "ingredients"
    )
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == "POST":
            if user.favorite_recipes.filter(id=recipe.id).exists():
                return Response(
                    {"detail": "Рецепт уже есть в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.favorite_recipes.add(recipe)
            user.save()

            serializer = RecipeMinifiedSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        deleted_count = user.favorite_recipes.remove(recipe)
        if deleted_count == 0:
            return Response(
                {"detail": "Рецепта нет в избранном."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == "POST":
            if user.shopping_cart.filter(id=recipe.id).exists():
                return Response(
                    {"detail": "Рецепт уже добавлен в корзину."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.shopping_cart.add(recipe)
            user.save()
            serializer = RecipeMinifiedSerializer(
                recipe, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        deleted_count = user.shopping_cart.remove(recipe)
        if deleted_count == 0:
            return Response(
                {"detail": "Рецепта нет в корзине."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Your view
    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        def create_shopping_list_file(ingredients):
            shopping_list = "\n".join(
                [
                    f"{ing['ingredient__name']} - {ing['amount']} "
                    f"{ing['ingredient__measurement_unit']}"
                    for ing in ingredients
                ]
            )

            buffer = BytesIO()
            buffer.write(shopping_list.encode())
            buffer.seek(0)
            return buffer

        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__recipes_in_shopping_cart=request.user.id
            )
            .order_by("ingredient__name")
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )

        shopping_list_buffer = create_shopping_list_file(ingredients)

        response = HttpResponse(
            shopping_list_buffer,
            content_type="text/plain",
        )
        response["Content-Disposition"] = "attachment; filename=pipi.txt"
        return response


#     @action(
#         detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
#     )
#     def download_shopping_cart(self, request):
#         ingredients = (
#             IngredientInRecipe.objects.filter(
#                 recipe__recipes_in_shopping_cart=request.user.id
#             )
#             .order_by("ingredient__name")
#             .values("ingredient__name", "ingredient__measurement_unit")
#             .annotate(amount=Sum("amount"))
#         )

#         # concatenate ingredient names and amounts to txt
#         shopping_list = "\n".join(
#             [
#                 f"""{ing['ingredient__name']} - {ing['amount']} \
# {ing['ingredient__measurement_unit']}"""
#                 for ing in ingredients
#             ]
#         )

#         response = HttpResponse(shopping_list, content_type="text/plain")
#         response[
#             "Content-Disposition"
#         ] = "attachment; filename=download_shopping_list"
#         return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        name_query = self.request.query_params.get("name")

        if name_query:
            queryset = queryset.filter(Q(name__icontains=name_query.lower()))
        return queryset


class ShoppingCartViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageLimitPagination
    serializer_class = RecipeMinifiedSerializer

    @action(
        detail=False, methods=["GET"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .order_by("ingredient__name")
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )

        # concatenate ingredient names and amounts to txt
        shopping_list = "\n".join(
            [
                f"""{ing['ingredient__name']} - {ing['amount']}
                    {ing['ingredient__measurement_unit']}"""
                for ing in ingredients
            ]
        )

        response = HttpResponse(
            "\n".join(shopping_list), content_type="text/plain"
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=shooping_list.txt"
        return response
