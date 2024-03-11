from django.urls import path,include
from .views import *


urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes-list/', AllNotesListView.as_view(), name='all-notes-list'),
    path('available-chapters/<int:user_id>/', AvailableChapterNotes.as_view(), name='availablechapters'),
    path('chapters-notes-view/<str:chaptername>/<int:user_id>/', AvailableNotesDetail.as_view(), name='available-chapters-notes'),
    path('notes-update-delete/<int:pk>/', NoteEditDeleteView.as_view(), name='note-edit-delete'),
]