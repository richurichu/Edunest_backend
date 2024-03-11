from rest_framework import serializers
from .models import *
from authentification.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk','username','profile_image','family' )


class FamilySerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    class Meta:
        model = Families
        fields = '__all__'
        
class MessagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'

class FamilyCreateSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
   
    
    family_image = serializers.ImageField(required=False)
    class Meta:
        model = Families
        fields = '__all__'