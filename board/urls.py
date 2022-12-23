from django.urls import path
from board.views import PostCreate, PostDetail, PostUpdate, PostDelete


urlpatterns = [
    path('create/', PostCreate.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]