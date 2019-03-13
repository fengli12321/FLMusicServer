from django.shortcuts import render

from base64 import b64encode

from rest_framework import mixins, viewsets
from rest_framework.pagination import CursorPagination
from django.utils.six.moves.urllib import parse as urlparse
from .models import Music
from .serializers import MusicSerializer, RecommendSerializer

# Create your views here.

class MusicPagination(CursorPagination):
    ordering = "-add_time"
    page_size = 12
    def encode_cursor(self, cursor):
        """
        Given a Cursor instance, return an url with encoded cursor.
        """
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = urlparse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded

class musicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    pagination_class = MusicPagination


class RecommendViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Music.objects.all().order_by('-like_num')[:5]
    serializer_class = RecommendSerializer

