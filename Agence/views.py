# Agence/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .forms import AnnonceUpdateForm, AnnonceForm, AnnonceSearchForm
from .models import Annonce, Candidature
from django.http import JsonResponse
from django.template.loader import render_to_string
import logging
from authentification.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape




logger = logging.getLogger(__name__)

def index(request):
    dernieres_annonces = Annonce.objects.order_by('-date_creation')[:2]
    candidatures = {}
    
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'candidate':
        candidatures = {annonce.id: 'déjà postulé' if Candidature.objects.filter(user=request.user, annonce=annonce).exists() else None for annonce in dernieres_annonces}

    return render(request, 'index.html', {
        'dernieres_annonces': dernieres_annonces,
        'candidatures': candidatures,
    })



def planDuSite(request):
    return render(request, "planDuSite.html")
def cookies(request):
    return render(request, "cookies.html")

def accessibilite(request):
    return render(request, "accessibilite.html")

def confidentialite(request):
    return render(request, "confidentialite.html")

def mentionsLegales(request):
    return render(request, "mentionsLegales.html")
def article(request):
    return render(request, "article.html")

@login_required
def dashboard(request):
    if request.user.profile.user_type != 'recruiter':
        return redirect('index')
    
    form = AnnonceForm()
    status = request.GET.get('status', 'active')

    if request.method == 'POST':
        if 'create-annonce' in request.POST:
            form = AnnonceForm(request.POST)
            if form.is_valid():
                annonce = form.save(commit=False)
                annonce.recruiter = request.user
                annonce.status = 'pending'
                annonce.save()
                messages.success(request, 'Annonce créée avec succès. Elle est en attente de validation.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Erreur lors de la création de l\'annonce. Veuillez vérifier le formulaire.')

    if status == 'archived':
        annonces = Annonce.objects.filter(recruiter=request.user, is_archived=True).order_by('-date_creation')
    elif status == 'pending':
        annonces = Annonce.objects.filter(recruiter=request.user, status='pending').order_by('-date_creation')
    else:
        annonces = Annonce.objects.filter(recruiter=request.user, is_archived=False, status='published').order_by('-date_creation')

    return render(request, 'dashboard.html', {
        'form': form,
        'annonces': annonces,
        'status': status
    })

@login_required
def approve_announce(request, id):
    if request.user.profile.user_type in ['admin', 'superadmin']:
        annonce = get_object_or_404(Annonce, id=id)
        action = request.POST.get('action', 'approve')
        if action == 'approve':
            annonce.status = 'published'
            annonce.refusal_comment = ''
        elif action == 'refuse':
            annonce.status = 'refused'
            annonce.refusal_comment = request.POST.get('comment', '')
        annonce.save()
        messages.success(request, f'Annonce {annonce.titre} mise à jour.')
        return redirect('admin_dashboard')
    messages.error(request, 'Vous n\'avez pas les autorisations nécessaires.')
    return redirect('dashboard')

@login_required
@user_passes_test(lambda u: u.profile.user_type in ['admin', 'superadmin'])
def admin_dashboard(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_user_type = request.POST.get('user_type')
        user = get_object_or_404(User, id=user_id)

        user.profile.user_type = new_user_type
        user.profile.save()

        # Échappement des chaînes pour éviter les problèmes d'encodage JSON
        message = escape(f"Le statut de l'utilisateur {user.get_full_name()} a été mis à jour avec succès.")
        
        user_html = render_to_string('admin/admin_user_card.html', {'user': user, 'request': request})
        message_html = render_to_string('partials/message.html', {'messages': [message]})
        
        return JsonResponse({'user_html': user_html, 'message_html': message_html})

    status = request.GET.get('status', 'published')
    annonces = Annonce.objects.filter(status=status)
    users = User.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'annonces': annonces, 'users': users})
from django.views.decorators.csrf import csrf_protect

@login_required
@user_passes_test(lambda u: u.profile.user_type in ['superadmin', 'admin']) 
@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        message_html = render_to_string('partials/message.html', {'messages': ["Utilisateur supprimé avec succès."]}, request=request)
        return JsonResponse({'message_html': message_html})
    return JsonResponse({'error': 'Requête non autorisée'}, status=400)


@user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.user_type in ['admin', 'superadmin'])
def validate_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')
        if action == 'approve':
            annonce.status = 'published'
            annonce.save()
            # Notification.objects.create(
            #     user=annonce.recruiter,
            #     message=f"Votre annonce '{annonce.metier.nom_metier}' a été validée et est maintenant publiée."
            # )
            messages.success(request, f"L'annonce '{annonce.metier.nom_metier}' a été validée et publiée.")
        elif action == 'refuse':
            annonce.status = 'refused'
            annonce.refusal_comment = comment
            annonce.save()
            # Notification.objects.create(
            #     user=annonce.recruiter,
            #     message=f"Votre annonce '{annonce.metier.nom_metier}' a été refusée. Commentaire: {comment}"
            # )
            messages.error(request, f"L'annonce '{annonce.metier.nom_metier}' a été refusée.")
    return redirect('admin_dashboard')

@login_required
def update_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.user != annonce.recruiter:
        return JsonResponse({'success': False, 'errors': 'Permission denied.'})

    if request.method == 'POST':
        form = AnnonceUpdateForm(request.POST, instance=annonce)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect': reverse('dashboard')})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AnnonceUpdateForm(instance=annonce)
        data = {
            'id': annonce.id,
            'metier': annonce.metier.id,
            'description': annonce.description,
            'lieu': annonce.lieu,
            'type_contrat': annonce.type_contrat,
            'salaire': annonce.salaire,
        }
        return JsonResponse({'annonce': data})

@login_required
def delete_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    if request.user == annonce.recruiter or (hasattr(request.user, 'profile') and request.user.profile.user_type in ['admin', 'superadmin']):
        annonce.delete()
        messages.success(request, 'Annonce supprimée avec succès.')
    else:
        messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cette annonce.')
    return redirect('dashboard')

@login_required
def archive_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.is_archived = True
    annonce.save()
    messages.success(request, 'Annonce archivée avec succès.')
    return redirect('dashboard')

@login_required
def unarchive_annonce(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    annonce.is_archived = False
    annonce.save()
    messages.success(request, 'Annonce désarchivée avec succès.')
    return redirect('dashboard')

def annonces(request):
    annonces = Annonce.objects.filter(is_archived=False, status='published')
    user_candidatures = {}

    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.user_type == 'candidate':
        user_candidatures = {
            candidature.annonce.id: candidature.etat
            for candidature in Candidature.objects.filter(user=request.user)
        }

    form = AnnonceSearchForm(request.GET or None)

    if form.is_valid():
        localisation = form.cleaned_data.get('localisation')
        metier = form.cleaned_data.get('metier')
        type_contrat = form.cleaned_data.get('type_contrat')
        salaire_min = form.cleaned_data.get('salaire_min')
        salaire_max = form.cleaned_data.get('salaire_max')
        tri = form.cleaned_data.get('tri')

        if localisation:
            annonces = annonces.filter(lieu__icontains=localisation)
        if metier:
            annonces = annonces.filter(metier=metier)
        if type_contrat:
            annonces = annonces.filter(type_contrat__in=type_contrat)
        if salaire_min:
            annonces = annonces.filter(salaire__gte=salaire_min)
        if salaire_max:
            annonces = annonces.filter(salaire__lte=salaire_max)

        if tri:
            if tri == 'date_asc':
                annonces = annonces.order_by('date_creation')
            elif tri == 'date_desc':
                annonces = annonces.order_by('-date_creation')

    if request.headers.get('HX-Request'):
        return render(request, 'annonces_list.html', {
            'annonces': annonces,
            'user_candidatures': user_candidatures,
        })

    return render(request, 'annonces.html', {
        'annonces': annonces,
        'user_candidatures': user_candidatures,
        'form': form,
    })
    
@login_required
def postuler(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    candidature_existante = Candidature.objects.filter(user=request.user, annonce=annonce).exists()

    if candidature_existante:
        messages.warning(request, 'Vous avez déjà postulé à cette annonce.')
        response_html = "<span class='px-4 py-2 mt-4 text-gray-500 rounded-md btnValidate'>Déjà postulé</span>"
    else:
        Candidature.objects.create(user=request.user, annonce=annonce)
        messages.success(request, 'Votre candidature a été envoyée avec succès.')
        response_html = "<span class='px-4 py-2 mt-4 text-gray-500 rounded-md btnValidate'>Déjà postulé</span>"

    if request.headers.get('HX-Request'):
        return HttpResponse(response_html)

    return redirect('annonces')

#Visionner les candidatures
@login_required
def voir_candidature(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id, recruiter=request.user)
    candidatures = Candidature.objects.filter(annonce=annonce, etat='en_attente')
    accepted_candidatures = Candidature.objects.filter(annonce=annonce, etat='acceptee')
    refused_candidatures = Candidature.objects.filter(annonce=annonce, etat='refusee')
    
    context = {
        'annonce': annonce,
        'candidatures': candidatures,
        'accepted_candidatures': accepted_candidatures,
        'refused_candidatures': refused_candidatures
    }
    return render(request, 'voir_candidature.html', context)

#Valider les candidatures
@login_required
def valider_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)

    if request.user != candidature.annonce.recruiter:
        return JsonResponse({'success': False, 'message': "Vous n'avez pas la permission d'accéder à cette page."})

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accepter':
            candidature.etat = 'acceptee'
        elif action == 'refuser':
            candidature.etat = 'refusee'
        else:
            return JsonResponse({'success': False, 'message': 'Action non valide'})

        candidature.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=400)

@login_required
def accepted_candidatures(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    accepted_candidatures = Candidature.objects.filter(annonce=annonce, etat='acceptee')
    return render(request, 'partials/accepted_candidatures.html', {'accepted_candidatures': accepted_candidatures})

@login_required
def refused_candidatures(request, annonce_id):
    annonce = get_object_or_404(Annonce, id=annonce_id)
    refused_candidatures = Candidature.objects.filter(annonce=annonce, etat='refusee')
    return render(request, 'partials/refused_candidatures.html', {'refused_candidatures': refused_candidatures})

#voir profil candidat
@login_required
def view_candidate_profile(request, user_id, annonce_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    return render(request, 'view_candidate_profile.html', {'user': user, 'profile': profile, 'annonce_id': annonce_id})

#changer le statut d'un utilisateur (superadmin)
@login_required
@user_passes_test(lambda u: u.profile.user_type == 'superadmin')
def change_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        profile = user.profile
        if request.user.profile.user_type == 'superadmin' or user_type in ['candidate', 'recruiter']:
            profile.user_type = user_type
            profile.save()
            messages.success(request, 'Le type d\'utilisateur a été mis à jour.')
        else:
            messages.error(request, 'Vous n\'êtes pas autorisé à attribuer ce type d\'utilisateur.')
        return redirect('admin_dashboard')
    return render(request, 'change_user_status.html', {'user': user})


