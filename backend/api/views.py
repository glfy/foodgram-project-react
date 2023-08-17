from djoser.views import UserViewSet
from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework import filters
from rest_framework import status


from rest_framework.response import Response
from django.db.models import Q

from api.serializers.users import CustomUserSerializer
from users.models import User
from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    # IngredientInRecipe,
)
from api.serializers.recipe import (
    TagSerializer,
    RecipeReadSerializer,
    IngredientSerializer,
    RecipeWriteSerializer,
    RecipeMinifiedSerializer,
)
from api.permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS


# from api.exception_handlers import custom_exception_handler
# from rest_framework.exceptions import NotFound


...


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ["get", "post", "delete"]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    # pagination_class =

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if request.method == "POST":
            if user.favorite_recipes.filter(id=recipe.id).exists():
                return Response(
                    {"detail": "Рецепт уже есть в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.favorite_recipes.add(recipe)
            user.save()
            serializer = RecipeMinifiedSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not user.favorite_recipes.filter(id=recipe.id).exists():
                return Response(
                    {"detail": "Рецепта нет в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.favorite_recipes.remove(recipe)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=True, methods=["delete"], permission_classes=[IsAuthenticated]
    # )
    # def unfavorite(self, request, pk=None):
    #     recipe = self.get_object()
    #     user = request.user

    #     if not user.favorite_recipes.filter(id=recipe.id).exists():
    #         return Response(
    #             {"detail": "Рецепта нет в избранном."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     user.favorite_recipes.remove(recipe)
    #     user.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        name_query = self.request.query_params.get("name")

        if name_query:
            queryset = queryset.filter(
                Q(name__icontains=name_query)
                | Q(name__icontains=name_query.capitalize())
                | Q(name__icontains=name_query.lower())
            )

        return queryset

    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = IngredientFilter
