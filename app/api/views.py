from rest_framework import generics, permissions
from .models import Word, Definition
from .serializers import WordSerializer, DefinitionSerializer
from users.permissions import IsAuthenticated

class WordCreateView(generics.CreateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class WordUpdateView(generics.UpdateAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [IsAuthenticated]

class WordListView(generics.ListAPIView):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class DefinitionCreateView(generics.CreateAPIView):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class DefinitionUpdateView(generics.UpdateAPIView):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    permission_classes = [IsAuthenticated]