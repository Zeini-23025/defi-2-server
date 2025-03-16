from rest_framework import serializers
from .models import Word, Definition, Comment, History, Notification, Badge, DocumentImport # type: ignore
from users.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class WordSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()  # Affiche le nom de l'auteur

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

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    nom = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'nom', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'nom': {'required': True},
            'role': {'read_only': True}
        }
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                nom=validated_data['nom'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
