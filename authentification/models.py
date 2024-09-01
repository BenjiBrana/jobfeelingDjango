# authentification/models.py

from django.db import models
from django.contrib.auth.models import User
from Agence.models import Competence, Metier 

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Administrateur'),
        ('superadmin', 'Super Administrateur'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='candidate')
    ville = models.CharField(max_length=100, blank=True, null=True)
    metier = models.ForeignKey(Metier, on_delete=models.SET_NULL, null=True, blank=True) 
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    nom_entreprise = models.CharField(max_length=100, blank=True, null=True)
    numero_siret = models.CharField(max_length=14, blank=True, null=True)
    competences = models.ManyToManyField(Competence, blank=True)

    def __str__(self):
        return self.user.username
