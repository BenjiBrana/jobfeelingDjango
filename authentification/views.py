# authentification/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile
from Agence.models import Competence, Metier
from django.http import JsonResponse
from django.db import IntegrityError, transaction
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inscription utilisateur
def inscription(request):
    if request.method == "POST":
        logger.debug("Méthode POST reçue pour l'inscription")
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_type = request.POST.get('user_type')  # Récupérer le type d'utilisateur du formulaire
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Un compte avec cet email existe déjà.')
                logger.debug("Un compte avec cet email existe déjà : %s", email)
                return render(request, 'inscription.html', {'form': form})
            
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.username = user.email  # Utiliser l'email comme nom d'utilisateur
                    user.save()
                    # Créer le profil avec le user_type
                    Profile.objects.create(user=user, user_type=user_type)

                messages.success(request, 'Votre compte a été enregistré avec succès. Vous pouvez maintenant vous connecter.')
                logger.debug('Inscription réussie pour l\'utilisateur : %s', email)
                return redirect('connexion')
            except IntegrityError as e:
                messages.error(request, 'Erreur d\'intégrité. Un compte avec cet email existe déjà.')
                logger.error('Erreur d\'intégrité lors de l\'inscription pour l\'email : %s, Erreur: %s', email, str(e))
                # Assurez-vous de supprimer l'utilisateur en cas d'erreur d'intégrité
                if user.pk:
                    user.delete()
        else:
            messages.error(request, 'Erreur lors de l\'inscription. Veuillez vérifier le formulaire.')
            logger.error('Formulaire invalide : %s', form.errors)
    else:
        logger.debug("Méthode GET reçue pour l'inscription")
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscription.html', context)

# Vue pour vérifier si l'email est déjà utilisé
def check_email(request):
    email = request.GET.get('email', None)
    is_taken = User.objects.filter(email=email).exists()
    return JsonResponse({'is_taken': is_taken})

# Profil utilisateur
@login_required
def profil(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profil')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    metiers = Metier.objects.all()  # Récupère tous les métiers

    return render(request, 'profil.html', {'form': form, 'user': request.user, 'metiers': metiers})

# Connexion utilisateur
def connexion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('annonces')  
        else:
            messages.error(request, "Erreur d'adresse email ou de mot de passe")
    return render(request, 'connexion.html')

# Déconnexion utilisateur
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('connexion')

# Définir le type d'utilisateur
def set_user_type(request):
    if request.method == "POST":
        username = request.POST['username']
        user_type = request.POST['user_type']
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        profile.user_type = user_type
        profile.save()
        messages.success(request, 'Le type d\'utilisateur a été mis à jour.')
        return redirect('set_user_type')
    return render(request, "set_user_type.html")

# Ajouter une compétence
@login_required
def add_competence(request):
    if request.method == 'POST':
        competence_name = request.POST.get('competence')
        if competence_name:
            competence, created = Competence.objects.get_or_create(name=competence_name)
            request.user.profile.competences.add(competence)
            messages.success(request, 'Compétence ajoutée avec succès.')
    return redirect('profil')

# Supprimer une compétence
@login_required
def remove_competence(request, competence_id):
    competence = get_object_or_404(Competence, id=competence_id)
    request.user.profile.competences.remove(competence)
    messages.success(request, 'Compétence supprimée avec succès.')
    return redirect('profil')
