from django_filters import FilterSet, ModelChoiceFilter
from .models import Reply, Post


class ReplyFilter(FilterSet):

   #post_id__in = ModelChoiceFilter(queryset=Post.objects.all())

   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Reply
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'body': ['icontains'],
           'post_id': ['in'],
           #'date': ['gt'],

       }