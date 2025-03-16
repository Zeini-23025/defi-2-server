from django.db import models
from users.models import User

class Word(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('under_review', 'En cours de révision'),
        ('approved', 'Validé'),
        ('rejected', 'Rejeté'),
    ]

    mot = models.CharField(max_length=255, unique=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mots")
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.mot
class Definition(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="definitions")
    texte = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Définition de {self.word.mot}"
class Comment(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="commentaires")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Commentaire sur {self.word.mot} par {self.auteur.nom}"
class History(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="historique")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)  # Ex: "Ajouté", "Modifié", "Validé"
    date_action = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} - {self.word.mot}"
class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification pour {self.utilisateur.nom}"
class Badge(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_obtention = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titre} pour {self.utilisateur.nom}"
class DocumentImport(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to="documents/")
    date_import = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    def __str__(self):
        return f"Document importé par {self.utilisateur.nom}"
