from rest_framework import serializers
from .models import *
from authentification.models import CustomUser


class TestSeriesSerializer(serializers.ModelSerializer):
    has_attended = serializers.SerializerMethodField()

    class Meta:
        model = TestSeries
        fields = ['id', 'name', 'description', 'has_attended']

    def get_has_attended(self, obj):
        user = self.context['request'].user
        return obj.has_user_attended(user)
    

class FacultyTestSeriesSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField()
   

    class Meta:
        model = TestSeries
        fields = ['id', 'name', 'description','question_count','is_published']

   



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class QuizResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    selected_option = OptionSerializer()
    correct_option = OptionSerializer()

    class Meta:
        model = QuizResponse
        fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'quiz_points', 'profile_image']

class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSeries
        fields = '__all__'