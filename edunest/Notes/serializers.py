from rest_framework import serializers
from  .models import *
from Courses.serializers import ChapterNotesSerializer

class NoteSerializerAdd(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = ['id', 'chapter', 'timestamp', 'content', 'created_at']

class NoteSerializer(serializers.ModelSerializer):
    chapter = ChapterNotesSerializer( read_only=True)

    class Meta:
        model = Note
        fields = '__all__' 