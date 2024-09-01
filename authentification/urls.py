from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil, name='profil'),
    path('set_user_type/', views.set_user_type, name='set_user_type'),
    path('add_competence/', views.add_competence, name='add_competence'),
    path('remove_competence/<int:competence_id>/', views.remove_competence, name='remove_competence'),
    path('check_email/', views.check_email, name='check_email'),
]