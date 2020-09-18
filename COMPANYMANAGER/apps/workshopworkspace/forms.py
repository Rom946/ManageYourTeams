from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder, MultiField, Button
from crispy_forms.bootstrap import FormActions
from django.forms import ValidationError

from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_starfield import Stars
from bootstrap_datepicker_plus import DateTimePickerInput


from apps.teamleaderworkspace.models import *
from .models import *

from datetime import datetime

class PackageNumberForm(forms.ModelForm):
    
    film_reel = forms.ChoiceField()
    reference = forms.ChoiceField()
    qty = forms.IntegerField()
    waste_qty = forms.IntegerField()
    waste_category = forms.ChoiceField()
    involved = forms.ChoiceField()

    class Meta:
        model = Package
        exclude = ['team_leader', 'code', 'waste', 'had_stock_update', 'available_at_office', 'finished', 'references_applied']

    def __init__(self, *args, **kwargs):
        super(PackageNumberForm, self).__init__()
        self.helper = FormHelper()
        self.fields['date_creation'].widget = DateTimePickerInput(
            format='%Y-%m-%d',
            options={
                "format": "YYYY-MM-DD", # moment date-time format
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            },
            attrs={
                "required" : True,
            })
        self.fields['reference'].widget = forms.Select(attrs={
            'label' : 'References in the package',
            'id': 'id_reference', 
            'required': True, 
            'placeholder': 'Select a reference ..',
        })

        self.fields['qty'].widget.attrs = {'placeholder':'Number of references created' ,'required':'', 'min': '1', 'initial':'1'}
        self.fields['waste_qty'].widget.attrs = {'placeholder':'Number of references wasted' ,'required':'', 'min': '0', 'initial':'0'}
        self.fields['film_reel'].widget.attrs = {'required':''} 
        CHOICES = []
        films = FilmReel.objects.filter(finished=False)
        for film in films:
            CHOICES.append((film.id, film))
        self.fields['film_reel'].choices = CHOICES

        CHOICES = []
        refs = Reference.objects.filter(available_for_workshop=True)
        for ref in refs:
            CHOICES.append((ref.id, ref.name))
        self.fields['reference'].choices = CHOICES

        CHOICES = []
        categories = WasteCategory.objects.filter(available_for_workshop=True)
        for category in categories:
            CHOICES.append((category.id, category.name))
        self.fields['waste_category'].choices = CHOICES

        CHOICES = [
            (0, 'Cutter'),
            (1, 'Packer'),
            (2, 'Team leader'),
            (3, 'Team'),
            (4, 'Supplier'),
            (5, 'Other')
        ]
        self.fields['involved'].choices = CHOICES


        savebtn = self.helper.add_input(Submit('submit', 'Save', css_id = 'savebtn'))
        continuebtn = self.helper.add_input(Button('continue', 'Continue', css_class = 'btn btn-success', css_id = 'continuebtn', onclick = 'Continue(event);'))
        

class AddNewEmployeeForm(forms.Form):    
    
    name = forms.CharField(max_length=200)
    as_ = forms.ChoiceField()
    

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.helper = FormHelper()
        self.fields['name'].widget = forms.TextInput(attrs = {
            'id': 'add', 
            'required': True, 
            'pattern':'(\w+ \w+)',
            'title':'Enter Characters Only ',
            'placeholder': 'Type the full name..'
        })

        self.fields['as_'].widget = forms.Select(attrs={
            'id': 'as', 
            'required': True, 
            'placeholder': 'Select a position ..' 
        })
        self.fields['as_'].choices = [(0, 'Cutter'), (1, 'Packer')]
        self.helper.add_input(Submit('submit', 'Add', css_class='btn-primary'))


class AddNewReelForm(forms.Form):    
    
    film_name = forms.ChoiceField()
    film_reel_number = forms.CharField(max_length=200)
    

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.helper = FormHelper()
        self.fields['film_reel_number'].widget = forms.TextInput(attrs = {
            'id': 'reel_nb', 
            'required': True, 
            'placeholder': 'Type the full reel number..'
        })

        self.fields['film_name'].widget = forms.Select(attrs={
            'id': 'film', 
            'required': True, 
            'placeholder': 'Select a film ..' 
        })

        film_choices = []
        films = Film.objects.all()
        for film in films:
            film_choices.append((film.id, film.name))

        self.fields['film_name'].choices = film_choices
        self.helper.add_input(Submit('submit', 'Add', css_class='btn-primary'))


class FinishReelForm(forms.Form):    
    
    film_reel = forms.ChoiceField()
    

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['film_reel'].widget = forms.Select(attrs={
            'id': 'film_reel', 
            'required': True, 
            'data-placeholder': 'Select a reel ..',
            'multiple':True
        })

        film_choices = []
        films = FilmReel.objects.filter(finished = False)
        for film in films:
            film_choices.append((film.id, str(film)))

        self.fields['film_reel'].choices = film_choices
        self.helper.add_input(Submit('submit', 'Declare these film reels finished', css_class='btn-primary'))