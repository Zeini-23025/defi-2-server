from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
import os
import requests
from django.http import JsonResponse
from .model.model_hassanya import generate_words

def generate_word_variants(request, word):
    # word = request.GET.get("word", "shrab")
    result = generate_words(word)
    
    return JsonResponse({"word": word, "variants": result.get("choices", [{}])[0].get("text", "").strip()})
    
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from users.models import User
from users.serializers import UserSerializer
from .models import Word, Definition, Comment, History, Notification, Badge, DocumentImport
from .serializers import WordSerializer, DefinitionSerializer, CommentSerializer, HistorySerializer, NotificationSerializer, BadgeSerializer, DocumentImportSerializer
from users.permissions import IsAdminOrReadOnly, IsModeratorOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny

User = get_user_model()

class WordViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les mots du dictionnaire.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté au mot proposé."""
        serializer.save(auteur=self.request.user, statut="pending")
        attribuer_badge(self.request.user)

    # @action(detail=True, methods=["post"], permission_classes=[IsModeratorOrReadOnly])
    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def approuver(self, request, pk=None):
        """Permet à un modérateur de valider un mot."""
        mot = self.get_object()
        mot.statut = "approved"
        mot.save()

        # Envoi d'une notification à l'auteur
        envoyer_notification(mot.auteur, f"Félicitations ! Votre mot '{mot.mot}' a été validé.")

        # Attribuer un badge à l'auteur si certaines conditions sont remplies
        attribuer_badge(mot.auteur)

        return Response({"message": "Mot validé avec succès."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    # @action(detail=True, methods=["post"], permission_classes=[IsModeratorOrReadOnly])
    def rejeter(self, request, pk=None):
        """Permet de rejeter un mot avec un commentaire explicatif."""
        mot = self.get_object()
        mot.statut = "rejected"
        mot.save()
        return Response({"message": "Mot rejeté."}, status=status.HTTP_200_OK)


class DefinitionViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les définitions des mots.
    """
    queryset = Definition.objects.all()
    serializer_class = DefinitionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté à la définition proposée."""
        serializer.save(auteur=self.request.user)
        attribuer_badge(self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset permettant aux modérateurs d'ajouter des commentaires sur les mots en attente de validation.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)
        attribuer_badge(self.request.user)


class DocumentImportViewSet(viewsets.ViewSet):
    """
    API permettant d'importer un document et de détecter les mots non reconnus.
    """
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def importer_document(self, request):
        fichier = request.FILES.get("document")
        if not fichier:
            return Response({"error": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST)

        # Traitement du fichier (extraction de texte et détection des mots inconnus)
        mots_inconnus = extraire_mots_inconnus(fichier)

        return Response({"mots_inconnus": mots_inconnus}, status=status.HTTP_200_OK)


# Fonction simulant l'extraction des mots inconnus à partir d'un document.
def extraire_mots_inconnus(fichier):
    # Simule la détection des mots inconnus dans un fichier
    return ["mot1", "mot2", "mot3"]


class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les utilisateurs et suivre leur progression.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def contributions(self, request, pk=None):
        """Retourne les contributions d'un utilisateur."""
        utilisateur = self.get_object()
        contributions = Word.objects.filter(auteur=utilisateur)
        serializer = WordSerializer(contributions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def score(self, request, pk=None):
        """Retourne le score d'un utilisateur basé sur ses contributions."""
        utilisateur = self.get_object()
        score = utilisateur.points
        return Response({"score": score})


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset pour consulter l'historique des actions sur les mots du dictionnaire.
    """
    queryset = History.objects.all()
    serializer_class = HistorySerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les notifications des utilisateurs.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté à la notification."""
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=["post"])
    def marquer_comme_lu(self, request, pk=None):
        """Permet à un utilisateur de marquer une notification comme lue."""
        notification = self.get_object()
        notification.lu = True
        notification.save()
        return Response({"message": "Notification marquée comme lue."}, status=status.HTTP_200_OK)


class BadgeViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les badges des utilisateurs.
    """
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté au badge attribué."""
        serializer.save(utilisateur=self.request.user)

def attribuer_badge(utilisateur):
    """Attribuer un badge à un utilisateur en fonction de ses contributions."""
    nombre_contributions = Word.objects.filter(auteur=utilisateur, statut='approved').count()
    nombre_definitions = Definition.objects.filter(auteur=utilisateur).count()
    nombre_commentaires = Comment.objects.filter(auteur=utilisateur).count()
    
    badges_deja_obtenus = utilisateur.badges.values_list('titre', flat=True)
    
    niveaux_badges = [
        (10, "Contributeur actif", "Vous avez contribué avec succès à 10 mots validés."),
        (50, "Contributeur avancé", "Vous avez contribué avec succès à 50 mots validés."),
        (100, "Grand contributeur", "Vous avez contribué avec succès à 100 mots validés."),
    ]
    for seuil, titre, description in niveaux_badges:
        if nombre_contributions >= seuil and titre not in badges_deja_obtenus:
            Badge.objects.create(utilisateur=utilisateur, titre=titre, description=description)
            envoyer_notification(utilisateur, f"Félicitations ! Vous avez reçu le badge '{titre}'.")
    
    niveaux_definitions = [
        (5, "Maître des définitions", "Vous avez ajouté 5 définitions approuvées."),
        (20, "Expert en définitions", "Vous avez ajouté 20 définitions approuvées."),
        (50, "Lexicographe accompli", "Vous avez ajouté 50 définitions approuvées."),
    ]
    for seuil, titre, description in niveaux_definitions:
        if nombre_definitions >= seuil and titre not in badges_deja_obtenus:
            Badge.objects.create(utilisateur=utilisateur, titre=titre, description=description)
            envoyer_notification(utilisateur, f"Félicitations ! Vous avez reçu le badge '{titre}'.")
    
    niveaux_commentaires = [
        (20, "Interagissant engagé", "Vous avez publié 20 commentaires sur les mots et définitions."),
        (50, "Débatteur actif", "Vous avez publié 50 commentaires sur les mots et définitions."),
        (100, "Pilier de la communauté", "Vous avez publié 100 commentaires sur les mots et définitions."),
    ]
    for seuil, titre, description in niveaux_commentaires:
        if nombre_commentaires >= seuil and titre not in badges_deja_obtenus:
            Badge.objects.create(utilisateur=utilisateur, titre=titre, description=description)
            envoyer_notification(utilisateur, f"Félicitations ! Vous avez reçu le badge '{titre}'.")


def envoyer_notification(utilisateur, message):
    """Envoyer une notification à un utilisateur."""
    Notification.objects.create(utilisateur=utilisateur, message=message)


class EnrichissementDictionnaireViewSet(viewsets.ViewSet):
    """
    API permettant d'importer un document et de détecter les mots non reconnus.
    """
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def importer_document(self, request):
        fichier = request.FILES.get("document")
        if not fichier:
            return Response({"error": "Aucun fichier fourni."}, status=status.HTTP_400_BAD_REQUEST)

        # Traitement du fichier (extraction de texte et détection des mots inconnus)
        mots_inconnus = extraire_mots_inconnus(fichier)

        return Response({"mots_inconnus": mots_inconnus}, status=status.HTTP_200_OK)


# Fonction simulant l'extraction des mots inconnus à partir d'un document.
def extraire_mots_inconnus(fichier):
    # Simule la détection des mots inconnus dans un fichier
    return ["mot1", "mot2", "mot3"]


class RegisterView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Inscription réussie',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
