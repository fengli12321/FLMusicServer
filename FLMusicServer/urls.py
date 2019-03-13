"""FLMusicServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
import xadmin
from users.views import VerifyCodeViewSet, UserViewSet, LoginView
from musics.views import musicViewSet, RecommendViewSet

router = DefaultRouter()
# 获取注册验证码
router.register(r'getsmscode', VerifyCodeViewSet, base_name="getsmscode")

# 注册
router.register(r'register', UserViewSet, base_name="register")

# 音乐列表
router.register(r'musics', musicViewSet, base_name="musics")

# 推荐列表
router.register(r'recommend', RecommendViewSet, base_name="recommend")

urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'docs/', include_docs_urls("Fox Music 文档")),
    path(r'', include(router.urls)),
    path(r'login/', LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
