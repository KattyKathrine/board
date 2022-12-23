from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title.title()}: {self.body[:20]}'


class Reply(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.body[:20]}'


class NewsLetter(models.Model):
    sender_name = models.CharField(max_length=255)
    sender_email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    body = models.TextField()


    def __str__(self):
        return f'{self.subject[:20]}'
