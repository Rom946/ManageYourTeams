from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder, MultiField, Button
from crispy_forms.bootstrap import FormActions
from django.forms import ValidationError

from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_starfield import Stars


from apps.teamleaderworkspace.models import *
from .models import *

import datetime 



class PerformanceForm(forms.Form):

    select_a_period = forms.BooleanField(initial = False)

    team_leader = forms.ChoiceField()

    team = forms.ChoiceField()
    all_team = forms.BooleanField(initial = True)

    from_date = forms.DateField()

    to_date = forms.DateField(initial = datetime.date.today())

    query = forms.ChoiceField()

    train = forms.ChoiceField()
    all_trains = forms.BooleanField(initial = True)

    car = forms.ChoiceField()
    all_cars = forms.BooleanField(initial = True)

    part = forms.ChoiceField()
    all_parts = forms.BooleanField(initial = True)

    location = forms.ChoiceField()
    all_locations = forms.BooleanField(initial = True)

    reference = forms.ChoiceField()
    all_references = forms.BooleanField(initial = True)

    tracking_code = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(PerformanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['from_date'].label = 'From'
        self.fields['to_date'].label = 'To'
        self.fields['select_a_period'].label = 'Select a period'

        
        choices = [
            (0, 'Global Performance'),
            (1, 'Nigel Performance'),
            (2, 'Workshop Performance'),
            (3, 'Waste evaluation'),
            (4, 'NCR'),
            (5, 'Get details on a job'),
        ]
        
        self.fields['query'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select an action ..'
            },
            choices = choices
        )



        choices = []
        trains = Train.objects.all()

        for train in trains:
            choices.append((train.id, train.name))
        self.fields['train'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select train(s) ..',
                'multiple':True
            },
            choices = choices
        )


        choices = []
        cars = Car.objects.all()

        for car in cars:
            choices.append((car.id, car.name))
        self.fields['car'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select car(s) ..',
                'multiple':True
            },
            choices = choices   
        )


        choices = []
        parts = Part.objects.all()

        for part in parts:
            choices.append((part.id, part.name))
        self.fields['part'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select part(s) ..',
                'multiple':True
            },
            choices = choices)


        
        choices = []
        teamleaders = Profile.objects.filter(position = 'TL')

        for profile in teamleaders:
            choices.append((profile.id, profile.name))
        self.fields['team_leader'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select team leader(s) ..',
                'multiple':True
            },
            choices = choices
        )
        
        
        choices = []
        team = Profile.objects.filter(position = 'TN')

        for profile in team:
            choices.append((profile.id, profile.name))
        self.fields['team'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select an employee or a team ..',
                'multiple':True
            },
            choices = choices
        )

        self.fields['reference'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Select reference(s) ..',
                'multiple':True
            }
        )

        self.fields['location'].widget = forms.Select(attrs={
            'required': True, 
            'data-placeholder': ' Select location(s) ..',
            'multiple':True
        })


        choices = []
        tracking_codes = TrackingCode.objects.all()

        for tracking_code in tracking_codes:
            choices.append((tracking_code.id, tracking_code.useful_with_teamleader()))
        self.fields['tracking_code'].widget = forms.Select(
            attrs={
                'required': True, 
                'data-placeholder': ' Search tracking code(s) ..',
                'multiple':True
            },
            choices = choices
        )

        

        self.helper.layout = Layout(
            'query',
            'select_a_period',
            Row(
                'from_date',
                'to_date'
            ),
            'tracking_code',
            'team_leader',
            'all_team',
            'team',
            Row(
                Column(
                    'all_trains',
                    'train'
                ),
                Column(
                    'all_cars',
                    'car'
                ),
                Column(
                    'all_parts',
                    'part',
                ),
                Column(
                    'all_references',
                    'reference'
                ),
                Column(
                    'all_locations',
                    'location'
                )
            ),
            self.helper.add_input(Submit(('performancebtn'), 'Search'))
        )


class GraphForm(forms.Form):

    # user select x and y axis
    x_axis = forms.ChoiceField()
    y_axis = forms.ChoiceField()
    
    #possible choices for x/y axis
    period = forms.DateField()
    stock_nigel = forms.ChoiceField()
    stock_workshop = forms.ChoiceField()
    stock_film = forms.ChoiceField()
    teamleader = forms.ChoiceField()
    employee = forms.ChoiceField()
    train = forms.ChoiceField()
    car = forms.ChoiceField()
    part = forms.ChoiceField()
    reference = forms.ChoiceField()
    all_wastes = forms.ChoiceField()
    waste_workshop = forms.ChoiceField()
    waste_nigel = forms.ChoiceField()
    waste_film = forms.ChoiceField()
    location = forms.ChoiceField()
    package = forms.ChoiceField()
    sales = forms.ChoiceField()

    #possibility for the user to select all the elements (all periods/all employees....)
    x_select_all = forms.BooleanField(initial = False)
    y_select_all = forms.BooleanField(initial = False)


    def __init__(self, *args, **kwargs):
        super(GraphForm, self).__init__(*args, **kwargs)
        
        choices = [
            (0, 'period'),
            (1, 'Stock Nigel'),
            (2, 'Workshop Performance'),
            (3, 'Waste evaluation'),
            (4, 'NCR'),
            (5, 'Get details on a job'),
        ]