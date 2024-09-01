from django.db import models
from django.contrib.auth.models import User

class Competence(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Metier(models.Model):
    nom_metier = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_metier
class Annonce(models.Model):
    CONTRACT_TYPES = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('stage', 'Stage'),
        ('alternance', 'Alternance'),
        # Ajoutez d'autres types de contrat si nécessaire
    ]

    STATUS_CHOICES = [
        ('published', 'Publiée'),
        ('pending', 'En attente'),
        ('refused', 'Refusée')
    ]
    metier = models.ForeignKey(Metier, on_delete=models.CASCADE)
    description = models.TextField()
    lieu = models.CharField(max_length=255)
    type_contrat = models.CharField(max_length=50, choices=CONTRACT_TYPES)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    refusal_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.titre

    def lieu_capitalized(self):
        return self.lieu.capitalize()
    
    

class Candidature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    etat = models.CharField(max_length=50, default='en_attente')  # Par exemple : 'en_attente', 'acceptee', 'refusee'
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.annonce.titre}"


