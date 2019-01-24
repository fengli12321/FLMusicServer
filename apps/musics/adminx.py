import xadmin

from .models import Music


class MusicAdmin(object):
    list_display = ["name", "singer", "album", "like_num", "fav_num", "music", "lyric", "image"]

xadmin.site.register(Music, MusicAdmin)
