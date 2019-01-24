from datetime import datetime
from django.db import models

# Create your models here.
class Music(models.Model):
    name = models.CharField(null=False, blank=False, verbose_name="歌曲名称", help_text="歌名", max_length=30)
    singer = models.CharField(max_length=20, default='未知歌手', verbose_name='歌手名', help_text='歌手')
    album = models.CharField(max_length=20, default='未知专辑', verbose_name='专辑名', help_text='专辑')
    music = models.FileField(upload_to="musics/musics", null=False, blank=False, verbose_name="歌曲文件", help_text="文件")
    lyric = models.FileField(upload_to="musics/lyrics", null=True, blank=True, verbose_name="歌词", help_text="歌词")
    image = models.ImageField(upload_to="musics/images", null=True, blank=True, verbose_name="图片", help_text="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    like_num = models.IntegerField(default=0, verbose_name="点赞数")
    fav_num = models.IntegerField(default=0, verbose_name="喜欢数")

    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
