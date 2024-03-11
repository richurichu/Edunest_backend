from rest_framework  import serializers
from Family.serializers import FamilySerializer
from .models import *
from Courses.models import *
class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'profile_image', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('username', 'email','role','id','profile_image','family','quiz_points','temp_role' )



# class UserRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
        
#         fields = ('temp_role','role')
class CourseSerializer(serializers.ModelSerializer):
    total_amount_received = serializers.IntegerField() 
    class Meta:
        model = Course
        fields = '__all__'
