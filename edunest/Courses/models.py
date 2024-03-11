from django.db import models



class Course(models.Model):
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  
    price = models.IntegerField() 
    image = models.ImageField(upload_to='courses/images/',null=True,blank=True)  
    is_blocked = models.BooleanField(default=False)
    teacher = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE, null=True,blank=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Course_advertise(models.Model):
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  
    price = models.IntegerField() 
    updated_at = models.DateTimeField(auto_now=True)
    is_vacant = models.BooleanField(default=True)
    applied = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE, null=True,blank=True)

class applications(models.Model):
    course_id = models.ForeignKey(Course_advertise,on_delete=models.CASCADE)
    user_id = models.ForeignKey('authentification.CustomUser',on_delete=models.CASCADE)
    aply_name = models.CharField(max_length=200,default='your name')
    phonenumber = models.CharField(max_length=10,default='0000000000')
    address = models.TextField(default='addresss')
    pincode = models.IntegerField(default=000000)
    description= models.TextField()
    document =  models.ImageField(upload_to='courses/images/',null=True,blank=True) 
    addi_document =  models.ImageField(upload_to='courses/images/',null=True,blank=True) 
    rejected =models.BooleanField(default=False)
    approved = models.BooleanField(default=False)


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='chapter_videos/')
    notes = models.FileField(upload_to='chapter_notes/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    Likes_count = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ChapterLiked(models.Model):
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    
class Payment(models.Model):
    user = models.ForeignKey('authentification.CustomUser', on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)