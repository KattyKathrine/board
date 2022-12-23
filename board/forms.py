from django import forms
from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    body = forms.CharField(widget=CKEditorUploadingWidget(external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor/ckeditor/plugins/youtube/',
                                          'plugin.js',
                                          )],
                                      ))

    class Meta:
       model = Post
       fields = [
           'title',
           'body',
           'category',
       ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
