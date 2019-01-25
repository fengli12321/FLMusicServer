from django.shortcuts import render
from rest_framework import mixins, viewsets

from .models import Music
from .serializers import MusicSerializer

# Create your views here.
class musicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
