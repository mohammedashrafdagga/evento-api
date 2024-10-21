from apps.events.models import *
from apps.events.serializers.categories import (
    CategoryDetailSerializer,
    CategoryListSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework import generics


@extend_schema(tags=["Events-Category"])
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


@extend_schema(tags=["Events-Category"])
class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related("events")
    serializer_class = CategoryDetailSerializer
    lookup_field = "slug"
