from django.db import models
from authentification.models import *
from Courses.models import *

class Comment(models.Model):
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    video_chapter = models.ForeignKey('Courses.Chapter', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Discussion(models.Model):
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

class Discussion_Comment(models.Model):
    question = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    audio = models.FileField(upload_to='discussion_audios/', blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

