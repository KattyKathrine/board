"""mmorpgboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from board.views import PostList, PostCreate, ReplyList, delete_reply, accept_reply
from ckeditor_uploader import views
from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', (PostList.as_view()), name='posts'),
    path('post/', include('board.urls')),
    path('replies/', (ReplyList.as_view()), name='replies'),
    path('reply/accept/', accept_reply),
    path('reply/delete/', delete_reply),
    re_path(r"^ckeditor/upload/", login_required(views.upload), name="ckeditor_upload"),
    re_path(
        r"^ckeditor/browse/",
        never_cache(login_required(views.browse)),
        name="ckeditor_browse",
    ),

]
