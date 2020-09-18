from django import forms 
from apps.teamleaderworkspace.models import *
from apps.workshopworkspace.models import *


class StockNigelForm(forms.ModelForm):
    reference = forms.CharField(disabled=True)

    class Meta:
        model = Stock
        fields = ['reference', 'qty']

    def clean_author(self):
        return self.instance.reference


class StockWorkshopForm(forms.ModelForm):
    reference = forms.CharField(disabled=True)

    class Meta:
        model = StockWorkshop
        fields = ['reference', 'qty']
        
    def clean_author(self):
        return self.instance.reference

class StockFilmForm(forms.ModelForm):
    film = forms.CharField(disabled=True)

    class Meta:
        model = StockFilm
        fields = ['film', 'qty']
    
    def clean_author(self):
        return self.instance.film