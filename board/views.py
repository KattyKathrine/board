from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post, Category, Reply, NewsLetter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import PostForm
from .filters import ReplyFilter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import PermissionDenied


# Для рассылки отдельного вью нет. Отправлять рассылки можно из админки.
def send_news_letter(sender, instance, created, **kwargs):

    users = User.objects.all()

    for user in users:
        msg = EmailMultiAlternatives(
            subject=instance.subject,
            from_email=f'"{instance.sender_name}" <{instance.sender_email}>',
            to=[user.email]
        )

        html_content = render_to_string(
            'newsletter.html',
            {
                'news': instance,
                'username': user.username

            }
        )

        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()

def notify_reply(sender, instance, created, **kwargs):

    msg = EmailMultiAlternatives(
        subject='Новый отклик!',
        from_email='katty@ikatty.ru',
        to=[instance.post_id.user_id.email]
    )

    html_content = render_to_string(
        'newreply.html',
        {
            'reply': instance,
            'username': instance.post_id.user_id.username

        }
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()

post_save.connect(send_news_letter, sender=NewsLetter)
post_save.connect(notify_reply, sender=Reply)

# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('board.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def post(self, request, *args, **kwargs):

        post = Post(
            title = request.POST['title'],
            body = request.POST['body'],
            category = Category.objects.get(pk=int(request.POST['category'])),
            user_id = request.user,

        )

        post.save()
#        subscription.delay(post.pk, request.POST.getlist('categories'))

        return redirect('/')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            reply = Reply(

                body = request.POST['body'],
                user_id = request.user,
                post_id = self.get_object(),

            )
            print("kasjdfhkasjdfh")
            reply.save()

            return redirect(f'/post/{reply.post_id.id}')

        else:
            raise PermissionDenied


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.add_post', 'board.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def get_success_url(self):
        self.success_url = self.request.path
        return str(self.success_url)[:-5]

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        print(request.user == self.get_object().user_id)

        if request.user != self.get_object().user_id and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_post', 'board.change_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()

        if request.user != self.get_object().user_id and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = ['-time']
    template_name = 'replies.html'
    context_object_name = 'replies'
    paginate_by = 3

    #def get_queryset(self):

       # queryset = Reply.objects.filter(post_id__user_id = self.request.user)

        #return queryset


    def get_queryset(self):
        # Получаем обычный запрос
        #queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.

        queryset = Reply.objects.filter(post_id__user_id=self.request.user).order_by('-id')
        self.filterset = ReplyFilter(self.request.GET, queryset)
        self.filterset.filters['post_id__in'].queryset = self.filterset.filters['post_id__in'].queryset.filter(user_id=self.request.user).order_by('-id')

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


def delete_reply(request):

    c = Reply.objects.filter(pk=int(request.GET['reply'])).delete()

    return redirect('replies')

def accept_reply(request):

    rep = Reply.objects.get(pk=int(request.GET['reply']))
    rep.is_accepted = True
    rep.save()

    msg = EmailMultiAlternatives(
        subject='Отклик принят',
        from_email='katty@ikatty.ru',
        to=[rep.user_id.email]
    )

    html_content = render_to_string(
        'notification.html',
        {
            'reply': rep,
            'username': rep.user_id.username

        }
    )

    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()

    return redirect('replies')