from rest_framework  import serializers
from .models import *
from authentification.serializers import *

class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class ReplyCreateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class EditDeleteSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Comment
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
   
    
    image = serializers.ImageField(required=False)
    class Meta:
        model = Discussion
        fields = '__all__'

class DiscussionCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Discussion_Comment
        fields = '__all__'

# class DiscussionSerializer(serializers.ModelSerializer):
   

#     class Meta:
#         model = Discussion
#         fields = '__all__'


class DiscussionResponseCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    audio = serializers.FileField(required=False)  
    text = serializers.CharField(required=False)
    class Meta:
        model = Discussion_Comment
        fields = '__all__'


        
class DiscussionCommentEditDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Discussion_Comment
        fields = '__all__'

class DiscussionNestedCommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    audio = serializers.FileField(required=False)  
    text = serializers.CharField(required=False)
    class Meta:
        model = Discussion_Comment
        fields = '__all__'