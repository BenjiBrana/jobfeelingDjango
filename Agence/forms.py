# Agence/forms.py
from django import forms
from .models import Annonce, Metier

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['metier', 'description', 'lieu', 'type_contrat', 'salaire']
        widgets = {
            'metier': forms.Select(attrs={'class': 'inputStyle'}),
            'description': forms.Textarea(attrs={'class': 'inputStyle'}),
            'lieu': forms.TextInput(attrs={'class': 'inputStyle'}),
            'type_contrat': forms.Select(attrs={'class': 'inputStyle'}),
            'salaire': forms.NumberInput(attrs={'class': 'inputStyle'}),
        }
        

class AnnonceSearchForm(forms.Form):
    localisation = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'inputStyle'}))
    metier = forms.ModelChoiceField(queryset=Metier.objects.all(), required=False, widget=forms.Select(attrs={'class': 'inputStyle'}))
    salaire_min = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'inputStyle'}))
    salaire_max = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'inputStyle'}))
    tri = forms.ChoiceField(choices=[('date_asc', 'Date croissante'), ('date_desc', 'Date décroissante')], required=False, widget=forms.Select(attrs={'class': 'inputStyle'}))
    type_contrat = forms.MultipleChoiceField(choices=Annonce.CONTRACT_TYPES, required=False, widget=forms.SelectMultiple(attrs={'class': 'inputStyle'}))

    def __init__(self, *args, **kwargs):
        super(AnnonceSearchForm, self).__init__(*args, **kwargs)
        
class AnnonceUpdateForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['metier', 'description', 'lieu', 'type_contrat', 'salaire']
        widgets = {
            'metier': forms.Select(attrs={'class': 'inputStyle'}),
            'description': forms.Textarea(attrs={'class': 'inputStyle'}),
            'lieu': forms.TextInput(attrs={'class': 'inputStyle'}),
            'type_contrat': forms.Select(attrs={'class': 'inputStyle'}),
            'salaire': forms.NumberInput(attrs={'class': 'inputStyle'}),
        }

    def __init__(self, *args, **kwargs):
        super(AnnonceUpdateForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs['placeholder'] = getattr(self.instance, field_name)
