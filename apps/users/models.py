from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="手机号")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name