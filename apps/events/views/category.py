from rest_framework import generics
from ..serializers.categories import CategoryListSerializer, CategoryDetailSerializer
from ..models import Category
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Events-Category"])
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


@extend_schema(tags=["Events-Category"])
class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related("events")
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"
