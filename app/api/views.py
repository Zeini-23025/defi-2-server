from rest_framework import viewsets
from .models import Mot, Definition, Commentaire, Historique, Notification, Badge
from .serializers import MotSerializer, DefinitionSerializer, CommentaireSerializer, HistoriqueSerializer, NotificationSerializer, BadgeSerializer

class MotViewSet(viewsets.ModelViewSet):
    queryset = Mot.objects.all()
    serializer_class = MotSerializer

class DefinitionViewSet(viewsets.ModelViewSet):
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer

class HistoriqueViewSet(viewsets.ModelViewSet):
    queryset = Historique.objects.all()
    serializer_class = HistoriqueSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
