from rest_framework import serializers
from dictionary.models import Word, Definition, Comment, History, Notification, Badge, DocumentImport # type: ignore
from users.models import User

class WordSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()  # Affiche le nom de l’auteur

    class Meta:
        model = Word
        fields = ['id', 'mot', 'auteur', 'statut', 'date_ajout']

class DefinitionSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    auteur = serializers.StringRelatedField()

    class Meta:
        model = Definition
        fields = ['id', 'word', 'texte', 'auteur', 'date_ajout']

class CommentSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    auteur = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'word', 'texte', 'auteur', 'date_ajout']

class HistorySerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    utilisateur = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = History
        fields = ['id', 'word', 'utilisateur', 'action', 'date_action']

class NotificationSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'utilisateur', 'message', 'lu', 'date_envoi']

class BadgeSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()

    class Meta:
        model = Badge
        fields = ['id', 'utilisateur', 'titre', 'description', 'date_obtention']

class DocumentImportSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField()

    class Meta:
        model = DocumentImport
        fields = ['id', 'utilisateur', 'fichier', 'date_import', 'traite']
