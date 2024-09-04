from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers.sections import SectionSerializer
from ..permissions import (
    OwnerEventPermissions,
)
from ..models import Section
from drf_spectacular.utils import extend_schema


# Create Section
@extend_schema(tags=["Events-Section"])
class SectionCreateAPIView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [
        IsAuthenticated,
        OwnerEventPermissions,
    ]


# Detail Event
@extend_schema(tags=["Events-Section"])
class SectionDetailAPIView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


# Update Section
@extend_schema(tags=["Events-Section"])
class SectionUpdateAPIView(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [
        IsAuthenticated,
        OwnerEventPermissions,
    ]


# Destroy Event
@extend_schema(tags=["Events"])
class SectionDestroyAPIView(SectionUpdateAPIView, generics.DestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        OwnerEventPermissions,
    ]
