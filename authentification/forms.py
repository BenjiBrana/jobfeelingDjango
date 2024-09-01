from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from Agence.models import Metier

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'inputStyle w-full',
        'placeholder': 'Adresse e-mail'
    }))
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'inputStyle w-full',
        'autocomplete': 'new-password',
        'placeholder': 'Mot de passe'
    }))
    password2 = forms.CharField(label='Confirmation mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'inputStyle w-full',
        'autocomplete': 'new-password',
        'placeholder': 'Confirmation mot de passe'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Ajout des attributs aux champs de nom et prénom
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Prénom', 'class': 'inputStyle w-full'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nom', 'class': 'inputStyle w-full'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'inputStyle w-full',
        'placeholder': 'Adresse e-mail',
        'autocomplete': 'email',
        'id': 'id_email'  # Assurez-vous que cet ID correspond à celui utilisé dans votre JS
    }))
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'inputStyle w-full',
        'autocomplete': 'new-password',
        'id': 'new-password'  # Assurez-vous que cet ID correspond à celui utilisé dans votre JS
    }))
    password2 = forms.CharField(label='Confirmation mot de passe', widget=forms.PasswordInput(attrs={
        'class': 'inputStyle w-full',
        'autocomplete': 'new-password',
        'id': 'new-password'  # Assurez-vous que cet ID correspond à celui utilisé dans votre JS
    }))

    class Meta:
        model = Profile
        fields = ['user_type']

class ProfileUpdateForm(forms.ModelForm):
    metier = forms.ModelChoiceField(queryset=Metier.objects.all(), required=False)

    class Meta:
        model = Profile
        fields = ['ville', 'metier', 'description', 'photo', 'nom_entreprise', 'numero_siret']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        if photo:
            if photo.size > 1 * 1024 * 1024:
                raise forms.ValidationError("La taille de l'image ne doit pas dépasser 1 Mo.")
            try:
                img = Image.open(photo)
                img.verify()
                if img.format not in ["JPEG", "PNG", "GIF"]:
                    raise forms.ValidationError("Le format de l'image doit être JPEG, PNG ou GIF.")
            except Exception as e:
                raise forms.ValidationError("Le fichier téléchargé n'est pas une image valide.")
        return photo
