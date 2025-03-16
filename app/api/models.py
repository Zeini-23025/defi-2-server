from django.db import models
from users.models import User

class Mot(models.Model):
    texte = models.CharField(max_length=100)
    auteur = models.ForeignKey(User, related_name='mots', on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[('en_attente', 'En Attente'), ('approuve', 'Approuvé'), ('rejete', 'Rejeté')], default='en_attente')

    def __str__(self):
        return self.texte

class Definition(models.Model):
    mot = models.ForeignKey(Mot, related_name='definitions', on_delete=models.CASCADE)
    definition_texte = models.TextField()
    auteur = models.ForeignKey(User, related_name='definitions', on_delete=models.CASCADE)

    def __str__(self):
        return f"Définition de {self.mot.texte}"

class Commentaire(models.Model):
    mot = models.ForeignKey(Mot, related_name='commentaires', on_delete=models.CASCADE)
    commentaire_texte = models.TextField()
    moderateur = models.ForeignKey(User, related_name='commentaires', on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire sur {self.mot.texte}"

class Historique(models.Model):
    mot = models.ForeignKey(Mot, related_name='historiques', on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    effectue_par = models.ForeignKey(User, related_name='historiques', on_delete=models.CASCADE)
    horodatage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action sur {self.mot.texte} par {self.effectue_par.username}"

class Notification(models.Model):
    utilisateur = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    est_lu = models.BooleanField(default=False)
    horodatage = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.utilisateur.username}"

class Badge(models.Model):
    utilisateur = models.ForeignKey(User, related_name='badges', on_delete=models.CASCADE)
    nom_badge = models.CharField(max_length=50)
    attribue_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} a gagné le badge {self.nom_badge}"
