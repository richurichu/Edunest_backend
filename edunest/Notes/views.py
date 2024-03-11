from django.shortcuts import render
from rest_framework import generics
from .models import Note
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from authentification.models import *
from rest_framework.response import Response
from Courses.models import *


class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializerAdd
    
    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)


class AllNotesListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class AvailableChapterNotes(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        notes = Note.objects.filter(user=user)
        serializer = NoteSerializer(notes,many=True)
        return Response(serializer.data)
    
class AvailableNotesDetail(APIView):
    def get(self, request, chaptername,user_id):
        chapter = Chapter.objects.get(title = chaptername)
        user = get_object_or_404(CustomUser, pk=user_id)
        
        notes = Note.objects.filter(chapter = chapter , user = user)
        serializer = NoteSerializer(notes,many=True)
        return Response(serializer.data)
    
    
class NoteEditDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'pk'