from rest_framework import serializers
from .models import *
from authentification.models import CustomUser

from authentification.models import *
from .Validators.File_vaidator import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username','role')

class CourseSerializer(serializers.ModelSerializer):
    teacher = CustomUserSerializer(read_only=True) 
    class Meta:
        model = Course
        fields = '__all__'

   
class CourseadvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_advertise
        fields = '__all__'

    def validate_name(self, value):
       
        queryset = Course_advertise.objects.filter(name__icontains=value)
        coursename = Course.objects.filter(name__icontains=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("A course with a similar name already exists!")
        
        if coursename.exists():
            raise serializers.ValidationError("A course with a similar name already exists!")
        return value
    

class ApplicationApprovedSerializer(serializers.ModelSerializer):
    course_id = CourseadvSerializer(read_only=True)
    user_id =   CustomUserSerializer(read_only=True)
    class Meta:
        model = applications
        fields = '__all__'



class ApplicationSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = applications
        fields = ['course_id', 'description', 'document','aply_name','phonenumber','address','pincode','addi_document']

    def validate_course_id(self, value):
        if not Course_advertise.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course does not exist.")
        return value

class CourseRequestSerializer(serializers.ModelSerializer):
    course_id = CourseadvSerializer(read_only=True)
    class Meta:
        model = applications
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    video = serializers.FileField(validators=[ validate_video_file])
    # pdf = serializers.FileField(validators=[validate_pdf_file])

    class Meta:
        model = Chapter
        fields = '__all__'

class ChapterViewSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Chapter
        fields = '__all__' 

class ChapterEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['title', 'description']

class ChapterNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['title', 'pk']


class ChapterLikeToggle(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = ChapterLiked
        fields = '__all__'

