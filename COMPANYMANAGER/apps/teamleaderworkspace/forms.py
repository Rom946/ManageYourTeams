from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, ButtonHolder, MultiField, Button
from crispy_forms.bootstrap import FormActions
from django.forms import ValidationError
from django.urls import reverse_lazy


from django_select2.forms import Select2MultipleWidget, Select2Widget
from django_starfield import Stars
from bootstrap_datepicker_plus import DateTimePickerInput

from .models import *
from apps.workshopworkspace.models import Package
from datetime import datetime

#form to choose team, train(s), car(s) and part(s) worked on
class MyWorkForm(forms.Form):

    team_id=forms.ChoiceField(label='Who worked with you today', widget=forms.Select(attrs={"class":"form-control", "multiple":"true",'placeholder':'Select a team..', 'required':True, 'id':'team-list'}))
    train_id=forms.ChoiceField(label='Select the train(s) you worked on today', widget=forms.Select(attrs={"class":"form-control", "multiple":"true", 'placeholder':'Select a train..', 'required': True}))
    car_id=forms.ChoiceField(label='Select the car(s) you worked on today', widget=forms.Select(attrs={"class":"form-control","multiple":"true", 'placeholder':'Select a car..', 'required': True}))
    part_id=forms.ChoiceField(label='Select the part(s) you worked on today', widget=forms.Select(attrs={"class":"form-control","multiple":"true", 'placeholder':'Select a part..', 'required': True}))


    def __init__(self, *args, **kwargs):
        super().__init__()

        #prepare lists
        train_list=[]
        car_list=[]
        part_list=[]
        team_list=[]
        
        #get elements
        try:
            trains=Train.objects.all()
            for train in trains:
                train_single=(train.id,train.name)
                train_list.append(train_single)
        except:
            train_list=[]
        #set fields
        self.fields['train_id'].choices=train_list

        try:
            cars=Car.objects.all()
            for car in cars:
                car_single=(car.id,car.name)
                car_list.append(car_single)
        except:
            car_list=[]
        self.fields['car_id'].choices=car_list

        try:
            parts=Part.objects.all()
            for part in parts:
                part_single=(part.id,part.name)
                part_list.append(part_single)
        except:
            part_list=[]
        self.fields['part_id'].choices=part_list

        try:
            team=Tech.objects.all()
            for teammate in team:
                teammate_single=(teammate.id,teammate.name)
                team_list.append(teammate_single)
        except:
            team_list=[]
        self.fields['team_id'].choices=team_list
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Continue', css_class='btn-primary'))

    def SetLayout(self):
        self.helper = FormHelper()
        
        self.helper.layout = Layout(
            Column(
                Row(
                    self.fields['train_id'],
                    self.fields['car_id'],
                    self.fields['part_id'],
                ),
                Row(
                    self.fields['team_id'],
                ),
            ),
            Submit
        )
        

#add a new tech (mywork.html)
class AddNewTechForm(forms.ModelForm):    
    class Meta:
        model = Tech
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'addtech_id', 
                'required': True, 
                'pattern':'(\w+ \w+)',
                'title':'Enter Characters Only ',
                'placeholder': 'Type the full name..'
            })
        }
        validator = RegexValidator("(\w+ \w+)", "The name should contains only letters.")

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add', css_class='btn-primary'))

#Form to affect team to jobs
class AffectationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user_id=kwargs.pop("user_id")
        self.helper = FormHelper()
        self.helper.form_tag = False

        super().__init__()

        #prepare lists
        train_list=[]
        car_list=[]
        part_list=[]
        team_list=[]
        
        #get elements
        try:
            trains=Train.objects.filter(selectedby__id=self.user_id)
            print(trains)
            for train in trains:
                train_single=(train.id,train.name)
                train_list.append(train_single)
        except Exception as e:
            print(e)
            train_list=[]
        #set fields
        self.fields['train_id'].choices=train_list

        try:
            cars=Car.objects.filter(selectedby__id=self.user_id)
            for car in cars:
                car_single=(car.id,car.name)
                car_list.append(car_single)
        except:
            car_list=[]
        self.fields['car_id'].choices=car_list

        try:
            parts=Part.objects.filter(selectedby__id=self.user_id)
            for part in parts:
                part_single=(part.id,part.name)
                part_list.append(part_single)
        except:
            part_list=[]
        self.fields['part_id'].choices=part_list

        try:
            team=Tech.objects.filter(selectedby__id=self.user_id)
            for teammate in team:
                teammate_single=(teammate.id,teammate.name)
                
                team_list.append(teammate_single)
        except:
            team_list=[]
        self.fields['team_id'].choices=team_list

        

    train_id=forms.ChoiceField(label='Select a train', widget=forms.Select(attrs={"class":"form-control select", 'placeholder':'Select a train..', 'required': True}))
    car_id=forms.ChoiceField(label='Select a car', widget=forms.Select(attrs={"class":"form-control select",'placeholder':'Select a car..', 'required': True}))
    part_id=forms.ChoiceField(label='Select a part', widget=forms.Select(attrs={"class":"form-control select",'placeholder':'Select a part..', 'required': True }))
    team_id=forms.ChoiceField(label='Select the team who worked on it', widget=forms.Select(attrs={"class":"form-control select select-team", "multiple":"true",'placeholder':'Select a team..'}))


    def clean(self):
        super(MyWorkForm, self).clean()
        # This method will set the `cleaned_data` attribute

        train = self.cleaned_data.get('train_id')
        car = self.cleaned_data.get('car_id')
        part = self.cleaned_data.get('part_id')
        team = self.cleaned_data.get('team_id')
        print(team)
        data = {
            'train':train,
            'car':car,
            'part':part,
            'team':team
        }

        return data
        

#Form to select References applied by each tech
class ReferencesForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #set up crispy form tags position and attributes
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.form_action = 'References'  

    #set layout for crispy form 
    def SetLayout(self, field_name):
        id = str(field_name)+'-submit'
        self.helper.layout = Layout(
            field_name,
            Submit('submit', 'Add informations', css_class = "btn btn-primary", css_id = id)
        )
        
        

    def CreateNewForm(self, request, job, index, tech): 
        print('Creating a new form for '+ str(job))  
        reference_list = {}
        reference_choices = []
        try:
            part = Part.objects.get(name=job.part)
            print(job.part)
            reference = part.references.all()

            for ref in reference:
                #create tuple
                reference_list = (ref.id, ref.name)
                #append tuple to reference_choices
                reference_choices.append(tuple(reference_list))


            field_name = 'references_%s' % (index,)
            self.fields[field_name] = forms.ChoiceField(
                label='References applied on ' + str(job.train) + ' - ' + str(job.car) + ' - ' + str(part) ,
                widget=forms.Select(
                    attrs={
                        "class":"form-control", 
                        'placeholder':'Select reference(s)..', 
                        'required': True,
                        'multiple': True,
                        "id": str(job.train) + '-' + str(job.car) + '-' + str(part) + '-' + str(tech.name),
                    }
                )
            )
            try:
                self.initial[field_name] = job.part
                self.fields[field_name].choices = reference_choices
                #self.helper.form_id = str(field_name)+'-form'
                
                

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)    

        self.SetLayout(field_name)
        # create an extra blank field
        '''
        field_name = 'references_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)
        '''
        





    def get_references_fields(self):
        for field_name in self.fields:
            if field_name.startswith('references_'):
                yield self[field_name]    

   

#Form to add references infos 
class ReferenceInfoForm(forms.ModelForm):
   
    package = forms.ChoiceField()
    locations = forms.MultipleChoiceField( widget = Select2MultipleWidget)
    waste_qty = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    waste_category = forms.MultipleChoiceField( widget = Select2MultipleWidget)
    waste_location = forms.MultipleChoiceField(widget = Select2MultipleWidget)

    class Meta:
        model = ReferenceApplied
        fields = ['qty']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_today = datetime.today()
        print('Creating a form for instance :')
        print(self.instance)
        
         #set choices
        CATEGORY_CHOICES = []
        LOCATIONS_CHOICES = []
        category_model = self.instance.reference.possible_waste.all()
        location_model = self.instance.reference.possible_locations.all()  
        #set choices for waste category
        for category in category_model:
            #create tuple
            category_tuple = (category.id, category.name)
            #append tuple to choices list
            CATEGORY_CHOICES.append(tuple(category_tuple))
        #set choices for possible locations
        for location in location_model:
            location_tuple = (location.pk, location.name)
            LOCATIONS_CHOICES.append(tuple(location_tuple))


        #set up crispy form tags position and attributes
        self.helper = FormHelper()
        try:
            #set attributes
            self.fields['locations'].widget.attrs = {'id' : self.instance, 'class' : 'form-control'}
            self.fields['qty'].widget.attrs = {'class' : 'form-control col-md-12', 'placeholder' : 'Quantity applied', 'required':'', 'min': '1', 'initial':'1'}
            self.fields['waste_qty'].widget.attrs = {'class' : 'form-control col-md-12', 'placeholder' : 'Quantity wasted', 'min':'0', 'initial' : '0'}
            self.fields['waste_category'].widget.attrs = {'class' : 'form-control'}
            self.fields['waste_location'].widget.attrs = {'class' : 'form-control'}
            
            #set choices
            self.fields['locations'].choices = LOCATIONS_CHOICES

            self.fields['waste_location'].choices = LOCATIONS_CHOICES
            self.fields['waste_category'].choices = CATEGORY_CHOICES

            choices = []
            packages = Package.objects.filter(finished=False, reference = self.instance.reference, available_at_office = False)
            

            for package in packages:
                choices.append((package.id, package.code))
            choices.append(('Nothing', "I didn't use any of these packages"))
            self.fields['package'].widget = forms.Select(attrs={
                'required': True, 
                'data-placeholder': ' Select a package ..',
                'multiple':True
            })

            if not packages.exists():
                self.fields['package'].widget = forms.Select(attrs={
                'required': False, 
                'data-placeholder': ' No packages found.',
                'disabled':True
            })
            self.fields['package'].widget.choices = choices


        except Exception as e:
            print(e)
            
#Form to give feedback
class FeedbackForm(forms.ModelForm):
    
    rating = forms.IntegerField(widget=Stars)
    feedback = forms.Textarea()

    class Meta:
        model = FeedBack
        fields = ['feedback', 'rating']


    def __init__(self, *args, **kwargs):
        #set up crispy form tags position and attributes
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'SubmitFeedback'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        self.fields['feedback'].attr = {'required', True}
        

    def set_layout(self):
        id = 'feedback'
        self.helper.layout = Layout(
            Column(
                Row(
                    self.fields['feedback'],
                ),
                Row(
                    self.fields['rating'],
                ),
            ),
            Submit
        )

    def clean(self):
        super(FeedbackForm, self).clean()
        # This method will set the `cleaned_data` attribute

        feedback = self.cleaned_data.get('feedback')
        rating = self.cleaned_data.get('rating')
        if feedback == "":
            raise ValidationError("You must give a feedback")

    def save(self, request):
        user = request.user
        user_id = user.id
        date_today = datetime.today().date()
        
        feedback = self.cleaned_data.get('feedback')
        rating = self.cleaned_data.get('rating')
        
        obj, created = FeedBack.objects.get_or_create(teamleader_id = user_id, date_work = date_today)

        obj.feedback = feedback
        obj.rating = rating
        obj.save()

        return obj


class DeliveryForm(forms.Form):

    package = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        choices = []
        packages = Package.objects.filter(available_at_office=True)

        for package in packages:
            choices.append((package.id, package.code))
        self.fields['package'].widget = forms.Select(attrs={
            'id': 'id_package', 
            'required': True, 
            'data-placeholder': 'Select a package ..',
            'multiple':True
        })
        self.fields['package'].widget.choices = choices

        self.helper.add_input(Submit('submit', 'Continue', css_class='btn-primary'))
        

#handle the creation of a NCR
class QualityForm(forms.ModelForm): 
    
    #responsible = forms.ChoiceField()
    
    class Meta:
        model = Quality
        exclude = ['last_update', 'tracking_code', 'package', 'had_stock_update', 'waste']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QualityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #form setup
        self.helper.form_method = 'POST' 
        self.helper.form_action = reverse_lazy('teamleaderworkspace:quality-create')

        #self.fields['team_leader'].initial = self.request.user
        '''
        responsible_choices = []
        responsibles = Profile.objects.all()

        for responsible in responsibles:
            #create tuple
            responsible_tuple = (responsible.id, responsible.name)
            #append tuple to reference_choices
            responsible_choices.append(responsible_tuple)

        self.fields['responsible'].choices = responsible_choices
        '''

        self.fields['date_record'].widget = DateTimePickerInput(
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

        self.fields['date_replacement'].widget = DateTimePickerInput(
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



        self.helper.layout = Layout(
            Column(
                Row(
                    Column(
                        'date_record',
                        'situation',
                        'progress',
                        'description',
                    ),
                    Column(
                        'ncr_number',
                        'train',
                        'car',
                        'part',
                        'location',
                        'reference_to_replace',
                    ),
                    Column(
                        'default_type',
                        'replacement',
                        'date_replacement',
                        'replaced_by',
                    )
                )   
            ),
            Submit('submit', u'Save', css_class='btn btn-success'), 
        )
    
    
    def save(self, commit=True):
        obj = super(QualityForm, self).save(commit=False)
        print(self.cleaned_data)
        obj.save()
        
        

class QualityUpdateForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = ['progress', 'situation', 'replacement', 'date_replacement', 'replaced_by', "description"]

    def __init__(self, *args, **kwargs):
        super(QualityUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        #form setup
        self.helper.form_method = 'POST' 
        self.helper.form_action = 'teamleaderworkspace/quality/' + str(self.instance.id) + '/update/'
        
        self.fields['date_replacement'].widget = DateTimePickerInput(
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

        #disable situation field
        self.fields['situation'].disabled = True


        self.helper.layout = Layout(
            'progress',
            'situation',
            'replacement',
            'date_replacement',
            'replaced_by',
            'description',
                   
            Submit('submit', u'Update', css_class='btn btn-success'), 
        )

    def save(self, commit=True):
        obj = super(QualityUpdateForm, self).save(commit=False)
        print(self.cleaned_data)
        obj.save()
