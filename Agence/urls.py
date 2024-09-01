from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('planDuSite/', views.planDuSite, name='planDuSite'),
    path('accessibilite/', views.accessibilite, name='accessibilite'),
    path('confidentialite/', views.confidentialite, name='confidentialite'),
    path('mentionsLegales/', views.mentionsLegales, name='mentionsLegales'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('article/', views.article, name='article'),
    path('cookies/', views.cookies, name='cookies'),
    #annonces
    path('annonces/', views.annonces, name='annonces'),
    path('annonce/update/<int:annonce_id>/', views.update_annonce, name='update_annonce'),
    path('annonce/delete/<int:annonce_id>/', views.delete_annonce, name='delete_annonce'),
    path('annonce/archive/<int:annonce_id>/', views.archive_annonce, name='archive_annonce'),
    path('annonce/unarchive/<int:annonce_id>/', views.unarchive_annonce, name='unarchive_annonce'),
    path('postuler/<int:annonce_id>/', views.postuler, name='postuler'),
    #candidatures
    path('accepted_candidatures/<int:annonce_id>/', views.accepted_candidatures, name='accepted_candidatures'),
    path('refused_candidatures/<int:annonce_id>/', views.refused_candidatures, name='refused_candidatures'),
    path('valider_candidature/<int:candidature_id>/', views.valider_candidature, name='valider_candidature'),
    path('voir_candidature/<int:annonce_id>/', views.voir_candidature, name='voir_candidature'),
    path('profil_candidat/<int:user_id>/<int:annonce_id>/', views.view_candidate_profile, name='view_candidate_profile'),
    #admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/validate_annonce/<int:annonce_id>/', views.validate_annonce, name='validate_annonce'),
    path('admin_dashboard/delete_annonce/<int:annonce_id>/', views.delete_annonce, name='delete_annonce'),
    path('admin_dashboard/change_user_status/<int:user_id>/', views.change_user_status, name='change_user_status'),
    path('admin_dashboard/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),


]
