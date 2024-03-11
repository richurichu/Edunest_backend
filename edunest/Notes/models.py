from django.db import models


class Note(models.Model):
    user = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE)
    chapter = models.ForeignKey('Courses.Chapter', on_delete=models.CASCADE)
    timestamp = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
