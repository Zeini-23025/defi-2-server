from rest_framework import serializers
from .models import Mot, Definition, Commentaire, Historique, Notification, Badge

class MotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mot
        fields = ['id', 'texte', 'auteur', 'statut']

class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ['id', 'mot', 'definition_texte', 'auteur']

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['id', 'mot', 'commentaire_texte', 'moderateur']

class HistoriqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historique
        fields = ['id', 'mot', 'action', 'effectue_par', 'horodatage']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'utilisateur', 'message', 'est_lu', 'horodatage']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'utilisateur', 'nom_badge', 'attribue_le']
