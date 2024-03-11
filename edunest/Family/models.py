from django.db import models


class Families(models.Model):
    name = models.TextField()
    instruction = models.TextField(null=True)
    family_image = models.ImageField(upload_to='family/images',null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    

class Message(models.Model):
    family = models.ForeignKey(Families, on_delete=models.CASCADE)
    sender = models.CharField(max_length=150) 
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)