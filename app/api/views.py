from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from app.users.models import User
from app.users.serializers import UserSerializer
from .models import Word, Definition, Comment, History, Notification, Badge, DocumentImport
from .serializers import WordSerializer, DefinitionSerializer, CommentSerializer, HistorySerializer, NotificationSerializer, BadgeSerializer, DocumentImportSerializer
from users.permissions import IsAdminOrReadOnly, IsModeratorOrReadOnly, IsAuthenticated

class WordViewSet(viewsets.ModelViewSet):
    """
    Viewset pour gérer les mots du dictionnaire.
    """
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté au mot proposé."""
        serializer.save(auteur=self.request.user, statut="pending")

    @action(detail=True, methods=["post"], permission_classes=[IsModeratorOrReadOnly])
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

    @action(detail=True, methods=["post"], permission_classes=[IsModeratorOrReadOnly])
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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Associe l'utilisateur connecté à la définition proposée."""
        serializer.save(auteur=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Viewset permettant aux modérateurs d'ajouter des commentaires sur les mots en attente de validation.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)


class DocumentImportViewSet(viewsets.ViewSet):
    """
    API permettant d'importer un document et de détecter les mots non reconnus.
    """
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [IsAdminOrReadOnly]

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
    """Attribuer un badge à un utilisateur pour sa contribution."""
    if utilisateur.contributions.count() >= 10:  # Exemple : Attribuer un badge après 10 contributions
        Badge.objects.create(
            utilisateur=utilisateur,
            titre="Contributeur actif",
            description="Vous avez contribué avec succès à 10 mots.",
        )


def envoyer_notification(utilisateur, message):
    """Envoyer une notification à un utilisateur."""
    Notification.objects.create(utilisateur=utilisateur, message=message)



class EnrichissementDictionnaireViewSet(viewsets.ViewSet):
    """
    API permettant d'importer un document et de détecter les mots non reconnus.
    """
    permission_classes = [permissions.IsAuthenticated]

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
