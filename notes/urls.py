from django.urls import path
from .views import NoteListCreateView, NoteDetailView
from .models import Note
from .serializers import NoteSerializer

app_name = 'notes-list'

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='notes'),
    path('notes/<int:pk>', NoteDetailView.as_view(), name='note-detail')
]
 