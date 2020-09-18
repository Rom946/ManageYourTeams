from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView, 
    UpdateView,
    FormView
)
from apps.common.mixins import InjectFormMediaMixin

from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from crispy_forms.helper import FormHelper
from crispy_forms.utils import render_crispy_form

from .forms import *
from .models import *
from .tables import *

from apps.users.models import Profile
from apps.workshopworkspace.models import StockHistoryWorkshop, StockWorkshop, Package
from apps.common.decorators import ajax_required

import traceback
import json
import re
from datetime import datetime 
import time
from collections import ChainMap





#VIEWS THAT RENDER A TEMPLATE
@login_required
def homepage(request):
    
    #reset the selected values..
    ResetSelection(request, Tech, Train, Car, Part)

    return render(request, 'teamleaderworkspace/teamleaderhome.html',  {'title': 'My Workspace', 'profile' : Profile.objects.get(user = request.user)})
    

@login_required
def Timetable(request):
    context = {
        'profile' : Profile.objects.get(user = request.user),
        'title': 'Time Table'
    }
    return render(request, 'teamleaderworkspace/Timetable.html', context)


def StockUpdate(reference_applied, qty):
    print('Updating stock...')
    wastes = reference_applied.waste.all()

    difference_qty = 0
    difference_qty = reference_applied.qty - int(qty)
    
    reference_applied.qty = int(qty)

    reference_applied.save()
    

    stock = StockHistory.objects.get(reference = reference_applied.reference).stock.last()
    stock.qty = stock.qty + difference_qty 
    stock.save()




@require_http_methods(['POST'])
@login_required
def SubmitFeedback(request):
    print(request.POST)    

    form = FeedbackForm(request.POST)
    if form.is_valid():
        messages.success(request, 'Work data entered for today! Thank you')
        feedback = form.fields['feedback']
        rating = form.fields['rating']
        feedback_obj = form.save(request)
        print(feedback_obj)

        #update stock
        recap = WorkDone.manager.all_references_applied_by_teamleader_today(request.user.id)
        for reference_applied in recap:
            job = reference_applied.job
            progress_part, created = ProgressOnPart.objects.get_or_create(train = job.train, car = job.car, part = job.part)
            progress_part.up_to_date= False
            progress_car, created = ProgressOnCar.objects.get_or_create(train = job.train, car = job.car)
            progress_car.up_to_date= False
            progress_train, created = ProgressOnTrain.objects.get_or_create(train = job.train)
            progress_train.up_to_date= False

            progress_part.save()
            progress_car.save()
            progress_train.save()

            if not reference_applied.had_stock_update:
                stock_history, created_history = StockHistory.objects.get_or_create(reference = reference_applied.reference)
                if not created_history:
                    try:
                        last_stock_qty = stock_history.stock.last().qty
                    except Exception as e:
                        print(e)
                        last_stock_qty = 0
                stock, created = Stock.objects.get_or_create(reference = reference_applied.reference, date_record = datetime.today())
                wastes_qty = 0
                wastes = reference_applied.waste.all()
                for waste in wastes:
                    wastes_qty = wastes_qty + waste.qty

                #created a new stock object
                if created:
                    #created a stock history object
                    if created_history:
                        stock.qty = - reference_applied.qty - wastes_qty
                    
                    #get last stock qty and update  
                    else:
                        stock.qty = last_stock_qty - reference_applied.qty - wastes_qty
                
                #update stock
                else:
                    stock.qty = last_stock_qty - reference_applied.qty - wastes_qty
                

                stock.save()
                print(stock)        
                print(stock_history)  
                reference_applied.had_stock_update = True 
                reference_applied.save()  
            
            package = Package.objects.filter(references_applied__id = reference_applied.id)
            
            print(package)
            for p in package:
                tracking_code = p.code + '+' + reference_applied.code()
                tracking_code, created = TrackingCode.objects.get_or_create(code = tracking_code)  
                if created:
                    tracking_code.reference_applied = reference_applied
                    tracking_code.package_id = p.id
                    tracking_code.save()
                    print('New Tracking code: %s' %tracking_code)
                else:
                    print('Updating Tracking code: %s' %tracking_code)
                    tracking_code.reference_applied = reference_applied
                    tracking_code.package_id = p.id
                    tracking_code.save()
                    print('New Tracking code: %s' %tracking_code)

                


        context = {
            'title' : 'My workspace',
            'profile' : Profile.objects.get(user = request.user) 
        }

        return render(request, 'teamleaderworkspace/teamleaderhome.html', context)
    else:
        messages.error(request, 'You must give a feedback')
        #redirect to feedback
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


#FEEDBACK.HTML VIEWS
class FeedBackViewClass(View):
    
    def get(self, request, *args, **kwargs):
        data = request.POST

        user_id = request.user.id
        user_name = request.user.username
        tables = []
        #get all refs applied
        recap = WorkDone.manager.all_references_applied_by_teamleader_today(user_id)
        
        #check if there is a feedback object
        feedback = FeedBack.objects.filter(teamleader_id = user_id, date_work = datetime.today())

        if feedback:
            feedback = FeedBack.objects.get(teamleader_id = user_id, date_work = datetime.today())
            feedback_form = FeedbackForm(instance = feedback)
        else:
            feedback_form = FeedbackForm()

        context = {
            'title'     : 'Feedback', 
            'profile'   : Profile.objects.get(user = request.user),
            'recap'     : recap,
            'feedback'  : feedback_form
        }

        return render(request, 'teamleaderworkspace/feedback_teamleader.html', context)

    def post(self, request, *args, **kwargs):
        print('*****************Feedback*******************')       
        data = request.POST

        user_id = request.user.id
        user_name = request.user.username
        
        #arriving from References View -- same as get
        if len(data)==1:
            tables = []
            #get all refs applied
            recap = WorkDone.manager.all_references_applied_by_teamleader_today(user_id)
            
            #check if there is already a feedback object
            feedback = FeedBack.objects.filter(teamleader_id = user_id, date_work = datetime.today())
            if feedback:
                feedback = FeedBack.objects.get(teamleader_id = user_id, date_work = datetime.today())
                feedback_form = FeedbackForm(instance = feedback)
            else:
                feedback_form = FeedbackForm()
            context = {
                'title':'Feedback', 
                
                'profile' : Profile.objects.get(user = request.user),
                'recap': recap,
                'feedback' : feedback_form
            }

            return render(request, 'teamleaderworkspace/feedback_teamleader.html', context)

        else:
            print(data['action'])
            print(data)
            reference = data['reference']
            job = data['job']
            tech = data['tech']
            qty = data['qty']

            #get job
            job_split = job.split('-')
            train = job_split[0].strip()
            car = job_split[1].strip()
            part = job_split[2].strip()

            #get objects
            job = Job.objects.filter(train__name = train, car__name=car, part__name=part, team_leader_id = user_id)
            tech = Tech.objects.filter(name = tech)
            reference = Reference.objects.get(name = reference)

            #get ref applied
            reference_applied = ReferenceApplied.objects.get(reference = reference, job = job[0], tech = tech[0], date_work = datetime.today())

            if data['action'] == 'get locations':
                locations_list=[]
                for location in reference.possible_locations.all():
                    location_tuple = (location.id, location.name)
                    locations_list.append(location_tuple)

                response_data = {
                    'success' : True,
                    'locations' : locations_list
                }

            elif data['action'] == 'edit':
                
                locations = data['locations']
                if locations == '' or qty == '':
                    response_data = {
                    'success' : False,
                    'error' : 'You didnt modify a value.'
                    }
                else:
                    print('Updating ' + str(reference_applied.reference))
                    reference_applied.locations.clear()
                    #override last stock update
                    if reference_applied.had_stock_update:
                        StockUpdate(reference_applied, qty)

                    locations_list = locations.split(',')
                    locations_string = ''
                    for location in locations_list:
                        location_obj = Location.objects.get(id = location)
                        locations_string = locations_string + ' - ' + location_obj.name
                        reference_applied.locations.add(location_obj)

                    reference_applied.save()

                    

                    response_data = {
                        'success' : True,
                        'locations-string' : locations_string
                    }

            elif data['action'] == 'delete':  
                reference_applied.delete()
                response_data = {
                    'success' : True
                }
            
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )


#REFERENCE_AFFECTATION VIEWS
class EmployeeReferencesViewClass(View):

    #return all data done by techs today
    def get_tech_data(self, data):
        response_data = []
        #get each tech working today
        for obj in data:
            work = []
            count = 1
            tech = obj.tech
            work.append(tech)
            print('Today, '+str(tech)+' worked on: ')
            #get data for each tech
            tech_data = WorkByTech.manager.today_by_tech(tech.id)
            print(tech_data)
            #get work done by each tech
            for t_data in tech_data:
                tech_jobs = t_data.work.all()
                #get elements each tech worked on 
                
                for job in tech_jobs:
                    job_data = []
                    print('Job '+ str(count)+': ')
                    print('on train: '+str(job.train))
                    print('on car: '+str(job.car))
                    print('on part: '+str(job.part))
                    job_data.append(job.train)
                    job_data.append(job.car)
                    job_data.append(job.part)
                    work.append(job_data)
                    count+=1
        
        response_data.append(work)
        '''
        data [tech][job]
        [job][0] = train
        [job][1] = car
        [job][2] = part
        '''
        print(work)
        print(response_data)
        return response_data

    #return first tech jobs
    def get_first_tech_jobs(self, data):
        first_tech_jobs = data[0]
        return first_tech_jobs.work.all()

    #return first tech name
    def get_first_tech(self, data):
        first_tech = data[0].tech
        return first_tech

    #return team list of techs who were working today
    def get_team_list(self, data):
        #get each tech working today
        team_list = []
        for obj in data:
            try:
                tech = obj.tech
                team_list.append(tech.name)
            except Exception as e:
                print(e)
        return team_list 

    def get_team_list_evolution(self, data):
        print(data)
        team_list_evolution = []
        date_today = datetime.today()
        team_list = self.get_team_list(data)
        for tech in data:
            print(tech.tech)
            jobs = tech.work.all()
            print(jobs)
            job_done = 0
            index= 0
            jobs_to_do = []
            for job in jobs:
                ref_done = 0
                ref_applied = ReferenceApplied.objects.filter(last_work = date_today, tech_id = tech.tech.id, job = job)
                ref_applied_complete = ReferenceApplied.objects.filter(last_work = date_today, tech_id = tech.tech.id, job = job, qty__gt=0)
                
                #check if qty is given for the ref
                if ref_applied:
                    if len(ref_applied_complete) < len(ref_applied):
                        jobs_to_do.append(job)
                        
                        index=index+1
                    else:
                        print(str(job) + ' Done')
                        job_done = job_done+1
                else:
                    jobs_to_do.append(job)
                    index=index+1

            ks = []
            print('nb of job to do : ' + str(len(jobs_to_do)))
            print('jobs done : ' + str(job_done))
            #remove tech from the list if all the jobs are done
            if (job_done==len(jobs)) or (jobs_to_do==0 and job_done!=0):
                for person in team_list:
                    print(person)
                    if str(tech.tech.name) == str(person):
                        print('All jobs are done for today for ' + str(tech))
                        tech_done = person
                        if tech_done not in team_list_evolution:
                            team_list_evolution.append(tech_done)
                            break
        return team_list_evolution

    #get a profile in Profile model
    def get_profile(self, username):
        print('getting profile for '+str(username))
        try: 
            username = username.name
        except Exception as e:
            print(e)
        username = username.split(' ')
        username = username[0] + username[1]
        profile = get_object_or_404(Profile, user__username=username)
        print(profile)
        return profile

    def get_previous_tech(self, current_tech, team_list):
        #get current tech index in team_list
        index = 0
        for tech in team_list:
            if tech == current_tech:
                try:
                    return team_list[index-1]
                except Exception as e:
                    print(e)
            index=index+1
        
        return team_list[len(team_list)-1]

    def get_next_tech(self, current_tech, team_list):
        #get current tech index in team_list
        index=0
        try:
            print('Get next tech from : ' + str(current_tech))
            for tech in team_list:
                try:
                    tech = tech.name
                    current_tech = current_tech.name
                except Exception as e:
                    print(e)

                if str(tech) == str(current_tech):
                    try:
                        print('match')
                        print(tech)
                        return team_list[index+1]
                    except Exception as e:
                        print(e)
                        return team_list[0]
                index=index+1
        except Exception as e:
            print(e)
        

    #get references forms for a tech
    def GetForms(self, form_type, tech, request):
        print('******GetForms*******')
        data = {}
        date_today = datetime.today()
        team_list_evolution = []
        total_techs = 0
        #get all jobs done today by each tech 
        done_today_techs = WorkByTech.objects.filter(team_leader_id = request.user.id, date_work = date_today)
        #get team list
        team_list = self.get_team_list(done_today_techs)
        
        print('team list:')
        print(team_list)
        total_techs = len(team_list)
        print(len(team_list))
        #get work done today by the tech
        done_today = WorkByTech.objects.get(tech_id = tech.id , date_work = date_today, team_leader_id = request.user.id)
        print(done_today)
        forms = []
        tech_done = ''
        index = 0
        #get jobs
        jobs = done_today.work.all()
        print(jobs)
        job_done=0
        jobs_to_do = []
        for job in jobs:
            ref_done = 0
            ref_applied = ReferenceApplied.objects.filter(last_work = date_today, tech_id = tech.id, job = job)
            ref_applied_complete = ReferenceApplied.objects.filter(last_work = date_today, tech_id = tech.id, job = job, qty__gt=0)
            print('ref_applied:')
            print(ref_applied)
            print('ref complete')
            print(ref_applied_complete)
            #check if qty is given for the ref
            if ref_applied:
                if len(ref_applied_complete) < len(ref_applied):
                    #create a new form for each job
                    form = ReferencesForm()
                    form.CreateNewForm(request, job, index, tech)
                    jobs_to_do.append(job)
                    #create list with all form for first tech
                    if form_type == 'ajax':
                        forms.append(form.as_p())
                    elif form_type == 'render':
                        forms.append(form)
                    index=index+1
                else:
                    print(str(job) + ' Done')
                    job_done = job_done+1
            else:
                form = ReferencesForm()
                form.CreateNewForm(request, job, index, tech)
                jobs_to_do.append(job)
                #create list with all form for first tech
                if form_type == 'ajax':
                    forms.append(form.as_p())
                elif form_type == 'render':
                    forms.append(form)
                index=index+1

        team_list_evolution = self.get_team_list_evolution(done_today_techs)
                
            
        if team_list_evolution:
            print(team_list_evolution)
            #Update team list
            for done in team_list_evolution:
                k=0
                for person in team_list:
                    if str(done) == str(person) :
                        print(team_list[k])
                        team_list.pop(k)
                        break
                    k = k+1
                
                
        print('********teamlist**********')
        print(ReferenceApplied.objects.filter(qty__gt=0, date_work = datetime.today()))
        print(team_list)
        print(team_list_evolution)

        
        data['tech_done'] = tech_done
        data['total_techs'] = total_techs
        data['forms'] = forms
        data['team_list'] = team_list
        data['team_list_evolution'] = team_list_evolution

        return data

    #get a new tech reference forms. return context for HttpResponse or render
    #render => form_type = 'render'
    #httpResponse => form_type = 'ajax'
    def ChangeTech(self, form_type, request, tech):
        print('*********ChangeTech**********')
        username = request.user.username
        user_id = request.user.id

        #get tech            
        tech = Tech.objects.get(name=tech)
        print(tech)
        
        #Get forms for this tech
        try:
            new_data = self.GetForms(form_type, tech, request)
        except Exception as e:
            print(e)
        #tech_done = new_data['tech_done'])
        total_techs = new_data['total_techs']
        team_list_evolution = new_data['team_list_evolution']
        print('techs done:')        
        print(team_list_evolution)
        
        #if there are still tech data uncompleted
        if new_data['team_list']:
            team_list = new_data['team_list']
            print('uncompleted:')
            print(team_list)
            #get previous and next tech
            next_tech = self.get_next_tech(tech, team_list)
            previous_tech = self.get_previous_tech(tech, team_list)
            print(previous_tech)
            #if false => first tech
            if previous_tech:
                if form_type ==  'ajax':
                    print('Ajax call')
                    #previous_tech = previous_tech.name
            else: 
                if form_type == 'ajax':
                    previous_tech = team_list[len(team_list)-1]
                    print('Ajax call')
                    #previous_tech = team_list[len(team_list)-1].name
                else:
                    previous_tech = team_list[len(team_list)-1]

            #if false => last tech
            if next_tech:
                if form_type == 'ajax':
                    pass
                    #next_tech = next_tech.name
            else:
                if form_type == 'ajax':
                    next_tech = team_list[0]
                    #next_tech = team_list[0].name
                else: 
                    next_tech = team_list[0]
            
            print(previous_tech)
            print(next_tech)

            profile = self.get_profile(tech)
            print(profile)

            profile_image_url = profile.image.url
            profile_name = profile.user.first_name.title() + ' ' + profile.user.last_name.title()

           
            uncompleted = ''
            for t in team_list:
                uncompleted = uncompleted + ' ' + str(t)
            print(uncompleted)
            completed = 0
            completed = len(team_list_evolution)


            #send back form 
            if new_data['forms']:
                forms = new_data['forms']
                print('forms created : ' + str(len(forms)))
                print('**************************')
                
                action = 'load'
                print(action)
                if form_type == 'ajax':
                    response_data = {
                        'success' : True,
                        'forms' : forms,
                        'next_tech' : next_tech,
                        'previous_tech' : previous_tech,
                        'profile_image' : profile_image_url,
                        'profile_name'  : profile_name,
                        'action' : action,
                        'uncompleted' : uncompleted,
                        'completed' : completed,
                        'total_tech' : total_techs 
                    }
                elif form_type == 'render':
                    response_data = {
                        'title':'References',
                        'success' : True,
                        'tech': tech,
                        'forms' : forms,
                        'team_list' : team_list,
                        'profile' : profile,
                        'previous_tech' : previous_tech,
                        'next_tech' : next_tech,
                        'completed' : completed,
                        'action' : action,
                        'total_tech' : total_techs
                    }

            #load next tech info
            else:                    
                action = 'load next tech'
                print(action)

                if form_type == 'ajax':
                    response_data = {
                        'success' : True,
                        'next_tech' : next_tech,
                        'previous_tech' : previous_tech,
                        'profile_name' : profile_name,
                        'profile_image' : profile_image_url,
                        'action' : action,
                        'uncompleted' : uncompleted,
                        'completed' : completed,
                        'total_tech' : total_techs 
                    }
                elif form_type == 'render':
                    response_data = {
                        'success' :  True,
                        'next_tech' : next_tech,
                        'action' : action
                    }
        #no data to show anymore
        else:
            response_data = {
                'success' : False,
                'error' : 'Data is completed'
            }

        return response_data

    #check if a tech is done or not
    def CheckTechStatus(self, request, tech):
        print('CheckTechStatus..')
        print(tech)
        validation = []
        try:
            jobs = WorkByTech.objects.get(tech = tech, team_leader_id=request.user.id, date_work = datetime.today()).work.all()
        except Exception as e:
            print(e)

        k=0
        for job in jobs:
            print(job)
            reference_applied = ReferenceApplied.objects.filter(tech=tech, job=job, date_work = datetime.today())

            if reference_applied:
                for reference in reference_applied:
                    print(reference)
                    if reference.qty:
                        k=k+1
                    else:
                        print('Quantity not entered for '+ str(job) + ' - ' + str(reference))
                        validation.append('uncomplete')
                        break

                if k==len(reference_applied):
                    validation.append('complete')

            else: 
                print('no references selected for ' + str(job))
                validation.append('uncomplete')
                break
        
        for valid in validation:
            if 'uncomplete' in valid:
                return 'uncomplete'

        
        return 'complete'
        

    #check if all the techs are done
    def CheckGlobalStatus(self, request):
        print('CheckGlobalStatus..')
        done_today_techs = WorkByTech.objects.filter(team_leader_id = request.user.id, date_work = datetime.today())
        #data = self.get_tech_data(done_today_techs)
        team_list = self.get_team_list(done_today_techs)
        print(team_list)
        team_list_evolution = self.get_team_list_evolution(done_today_techs)
        print(team_list_evolution)
        if len(team_list_evolution) == len(team_list):
            return 'complete'
        else: 
            return 'uncomplete'
       
    #GET method - Form init for 1st tech
    def get(self, request, *args, **kwargs):
        team_list_evolution = []
        context = {}
        date_today = datetime.today()
        data = []
        status = self.CheckGlobalStatus(request)
        print(status)
        if status == 'uncomplete':
            #get all jobs done today by each tech 
            done_today_techs = WorkByTech.objects.filter(team_leader_id = request.user.id, date_work = datetime.today())

            print('all techs work today:')
            print(done_today_techs)

            #get all tech data (in a list)
            data = self.get_tech_data(done_today_techs)
            print('Done Today by techs:')

            print(data)
            team_list = self.get_team_list(done_today_techs)
        
            #get first tech
            first_tech = self.get_first_tech(done_today_techs)
            print('first tech:')
            print(first_tech)

            #get forms for the first tech
            new_data = self.GetForms('render', first_tech, request)

            #if there are forms
            if new_data['forms']:
                forms = new_data['forms']
                team_list = new_data['team_list']
                team_list_evolution = new_data['team_list_evolution']
                completed = len(team_list_evolution)
                print('completed' + str(team_list_evolution))
                print(team_list)
                #get first tech profile
                first_tech_profile = self.get_profile(first_tech.name)

                previous_tech = self.get_previous_tech(first_tech, team_list)
                
                print('previous tech: ' + str(previous_tech))

                next_tech = self.get_next_tech(first_tech, team_list)
                
                print('next tech: ' + str(next_tech))



                '''
                passing: 
                title of the page
                First Tech name : first_tech.name
                Jobs done today by 1st tech with user(team leader): first_tech_jobs
                Form for 1st tech : form
                Team list with tech names who worked under the logged team leader: team__list
                Tech profile infos (from User model) : tech_profile
                Previous tech in team_list : previous_tech
                Next tech in team_list : next_tech
                Previous tech profile : previous_tech_profile
                Next tech profile : next_tech_profile
                Number of completed infos: completed
                '''
                context = {
                    'title':'References',
                    'tech': first_tech,
                    'forms' : forms,
                    'team_list' : team_list,
                    'profile' : first_tech_profile,
                    'previous_tech' : previous_tech,
                    'next_tech' : next_tech,
                    'completed' : completed,
                    'total_tech' : new_data['total_techs']
                }
            #change tech to find forms or 404
            else: 
                
                next_tech = self.get_next_tech(first_tech, team_list)
                print(str(first_tech) + ' Jobs informations have already been given. ') 
                context['action'] = 'load next tech'
                j=0
                while context['action']=='load next tech':
                    print('Loading forms for next tech: ' + str(next_tech))
                    
                    #get the next tech
                    context = self.ChangeTech('render', request, next_tech)
                    if context['success'] == False:
                        context = {
                            'complete':True
                        }
                        break
                    next_tech = context['next_tech']
                    if j==30:
                        HttpResponseRedirect('../Feedback')
                        break

                    j=j+1
                        
        elif status == 'complete':
            context = {
                'title' : 'References',
                'profile' : Profile.objects.get(user = request.user),
                'complete':True
            }
        
        
        return render(request, 'teamleaderworkspace/references_affectation.html', context)


    def get_job(self, data, request):
        train = data['train']
        car = data['car']
        part = data['part']
        job = Job.objects.get(train__name = train, car__name = car, part__name = part, team_leader_id = request.user.id)
        return job

    def get_references(self, job):
        references_list = job.part.references.all() 
        return references_list


    def create_info_form(self, references_applied):
        form = ReferenceInfoForm()
        form.CreateNewForm(references_applied)
        return form

    def get_object_reference_applied(self, form_instance):
        date_today = datetime.today()
        infos = []
        infos = form_instance.split('-')
        reference_id = infos[0]
        tech_id = infos[1]
        job_id = infos[2]

        reference_applied,created = ReferenceApplied.objects.get_or_create(reference_id = reference_id, tech_id = tech_id, job_id = job_id, date_work=date_today)
            
        return reference_applied

    def validate_form(self, request, form_instance, reference_applied, form_data):
        print('form is valid!')
        date_today = datetime.today()   
        infos = []
        package_list = []
        infos = form_instance.split('-')
        reference_id = infos[0]
        tech_id = infos[1]
        job_id = infos[2]

        #get form data
        try:
            for data in form_data:
                if data['name'] == 'package':
                    print(data['value'])
                    if data['value'] != 'Nothing':
                        package = Package.objects.get(id=data['value'])
                        package.references_applied.add(reference_applied)
                        package_list.append(package)
                        print('Added reference for package %s' %package)


                #get qty
                elif data['name'] == 'qty':
                    qty = int(data['value'])
                    reference_applied.qty =+ qty

                #get locations 
                elif data['name'] == 'locations':
                    reference_applied.locations.add(int(data['value']))
                            
                #get waste qty
                elif data['name'] == 'waste_qty':
                    waste_qty = int(data['value'])

                
                #get waste category
                if data['name'] == 'waste_category':
                    waste_category = int(data['value'])
                    #get waste category object
                    waste_category = WasteCategory.objects.get(id = waste_category)
                    #get or create an object waste with the ref and category
                    waste, created = Waste.objects.get_or_create(reference = reference_applied.reference, category = waste_category, tech = reference_applied.tech, job_waste = reference_applied.job)
                    print('waste:')
                    print(waste)
                    
                    if created :
                        print('new waste for : ' + str(reference_applied.reference))
                        waste.qty = waste_qty
                        reference_applied.waste.add(waste)

                    else : 
                        print('updating waste for: ' + str(waste))
                        print(str(waste.qty)) 
                        waste.qty = waste.qty + waste_qty
                    
                    waste.save()
                
                #get waste location
                elif data['name'] == 'waste_location':
                    waste_location = int(data['value'])
                    #get waste category object
                    location = Location.objects.get(id = waste_location)
                    #get or create an object waste with the ref and category
                    waste, created = Waste.objects.get_or_create(reference = reference_applied.reference, category = waste_category, tech = reference_applied.tech, job_waste = reference_applied.job)
                    print('waste:')
                    print(waste)
                    
                    if created :
                        print('new waste for : ' + str(reference_applied.reference))
                        reference_applied.waste.add(waste)

                    else : 
                        print('updating waste for: ' + str(waste))

                    waste.location.add(waste_location)
                    print(str(waste.location.all())) 



                else:
                    print('unrecognized data : ' + str(data))

            reference_applied.save()
            to_withdraw = qty
            for package in package_list:
                if to_withdraw > 0:
                    if package.qty > 0:
                        i=0
                        while(i < qty and package.finished == False and to_withdraw > 0):
                            package.qty = package.qty - 1
                            package.save()
                            
                            i += 1
                            to_withdraw = to_withdraw - 1

                            if package.qty == 0:
                                package.finished = True
                                package.save()
                            
            
            if to_withdraw > 0:
                print('%s pieces more than expected' %to_withdraw)
                pass
                
        
            #check updated model
            print('model updated:')
            print('qty: ' + reference_applied.quantity())
            print('waste: ' + str(reference_applied.waste.all()))
            #print('locations: ' + str(reference_applied.locations))
            print(reference_applied.location())
            for waste in reference_applied.waste.all():
                print('Wasted for '+ str(reference_applied.reference) +': ' + str(waste.qty))
            
            work = WorkDone.objects.get(team_leader = request.user , work = job_id , date_work = date_today)
            work.references_applied.add(reference_applied)
            work.save()

            return work
        except Exception as e: 
            print(e)
            return False
    
    def post(self, request, *args, **kwargs):
        date_today = datetime.today()
        response_data = {}

        status = self.CheckGlobalStatus(request)
        print(status)
        if status == 'completed' :
            return HttpResponseRedirect('teamleaderworkspace/feedback')
        #get all data
        data = request.POST 
        print('data:')
        print(data)
        print('ACTION: ')
        print(data['action'])
        #user selected some references
        if data['action'] == 'select references':
        
            #get tech
            print(data['tech'])
            tech = Tech.objects.get(name=data['tech'])

            #get job
            job = self.get_job(data, request)
            print('job')
            print(job)

            #get references catalog for this job
            print('references catalog')
            references_catalog = self.get_references(job)
            print(references_catalog)

            #get form
            print('form')
            form = json.loads(data['form_data'])
            print(form)
            print('**********')
            
            if form!=None:
                m=0
                new_info_forms = []
                references_form = []
                references_applied = []
                instances = []
                for obj in form:
                    #get selected references id
                    if 'reference' in obj['name']:
                        reference_id = obj['value']
                        references_form.append(reference_id)
                        

                        for ref in references_catalog:
                            if int(reference_id) == ref.id:
                                print('match!')
                                print(ref)
                                
                                #create new record for ReferenceApplied 
                                reference_applied, created = ReferenceApplied.objects.get_or_create(tech=tech, job=job, reference=ref)
                                #create
                                if created:
                                    print('New record added')
                                    reference_applied.date_work = date_today
                                    reference_applied.save()
                                    print(reference_applied)

                                #update
                                else:
                                    if reference_applied:
                                        print('updating ReferenceApplied for : '+ str(reference_applied))
                                        print(str(reference_applied.last_work))
                                    else: 
                                        #error
                                        response_data = {
                                            'error' : 'No references found',
                                            'success' : False
                                        }
                                        return HttpResponse(
                                            json.dumps(response_data),
                                            content_type="application/json"
                                            )

                                #create a new form for each reference
                                new_info_form = ReferenceInfoForm(instance=reference_applied).as_p()
                                new_info_forms.append(new_info_form)
                                print(reference_applied.info())
                                instances.append(str(reference_applied.info()))
                                references_applied.append(str(reference_applied.reference))
                                m=m+1
                                print('matches for now: ' + str(m))
                '''
                print('references from form')
                print(references_form)
                print('nb of matches : ' + str(m))
                '''
                print('nb of forms created: '+str(len(new_info_forms)))
                
                
                #prepare response
                response_data = {
                    'instances' : instances,
                    'success' : True,
                    'forms' : new_info_forms,
                    'references' : references_applied
                }
               
            else:
                response_data = {
                    'success' : False,
                    'error' : 'An error occured. Please contact IT services.'
                }
        
        #user saved a reference
        elif data['action'] == 'save informations' :
            
            form_instance = data['instance']
            print('Receiving data for form '+str(form_instance))

            #get reference_applied object
            reference_applied = self.get_object_reference_applied(form_instance)    
            print('updating..')
            print(reference_applied)
            
            #get form
            form_data = json.loads(data['form_data'])

            if form_data:
                #validate the form
                work_done = self.validate_form(request, form_instance, reference_applied, form_data)
                #return to next view
                form_id = data['instance']
                #nb_of_ref_applied = len(work_done.references_applied.all())
                #references_to_apply = len(ReferenceApplied.objects.filter(last_work = date_today))
                tech = data['tech']
                tech = Tech.objects.get(name = tech)
                tech_status = self.CheckTechStatus(request, tech)
                if tech_status == 'complete':
                    print(str(tech) + ' ' + tech_status)
                    
                #Check if all the data have been completed
                global_status = self.CheckGlobalStatus(request)

                response_data = {
                    'success' : True,
                    'form_id' : form_id,
                    'global_status' : global_status,
                    'tech_status' : tech_status
                }

                #display status
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )

            #error - form is empty
            else:
                print('form invalid')

                response_data = {
                    'success' : False,
                    'error' : 'An error occured. Please contact IT services' 
                }

            
        elif data['action'] == 'change tech':
            #get user
            response_data = self.ChangeTech('ajax', request, data['tech'])

        

        #display status
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


#AFFECTATION.HTML VIEWS
class AffectationViewClass(View):
   
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        affectation_form = AffectationForm(user_id=user_id)
        print(user_id)
        context = {
            'profile' : Profile.objects.get(user = request.user),
            'title':'Affectation',
            'affectation_form':affectation_form
        }
        return render(request, 'teamleaderworkspace/affectation.html', context)


    def post(self, request, *args, **kwargs):
        #prepare response
        response_data = {}
        response_data['error']=''
        response_data['message']=''
        date_today=datetime.today()


        #get status
        status = request.POST.get('status')
        print(status)
        
        #get user
        user = request.user
        user_id = user.id
        username = user.username
        
        if status=='save':
            #form validation
            train_valid = False;
            car_valid = False;
            part_valid = False;
            team_valid = False;

            errors = {}
            errors['team'] = ''
            errors['done'] = ''

            #get form elements
            affected_train_id = request.POST.get('train')
            affected_car_id = request.POST.get('car')
            affected_part_id = request.POST.get('part')
            team_ids = request.POST.get('team')

            print(team_ids)
            print(affected_train_id)
            print(affected_car_id)
            print(affected_part_id)

            if team_ids!='[]' and affected_train_id!='None' and affected_car_id!='None' and affected_part_id!='None':
                #get elements
                if affected_train_id.isdigit():
                    train = Train.objects.get(id=affected_train_id)
                else:
                    errors['train'] = 'You must select a train' 
                
                if affected_car_id.isdigit():
                    car = Car.objects.get(id=affected_car_id)
                else:
                    errors['car'] = 'You must select a car' 

                if affected_part_id.isdigit():
                    part = Part.objects.get(id=affected_part_id)
                else:
                    errors['part'] = 'You must select a part' 
                    
                if Job.objects.filter(team_leader = user, train=train, car=car, part=part).exists():
                    work = Job.objects.get(team_leader=user, train=train, car=car, part=part)
                    print('This selection has already been done')
                    errors['done'] = 'This selection has already been done'

                else:
                    print('Creating ..')
                    work = Job.objects.create(team_leader=user, train=train, car=car, part=part)
                    

                #get all affected cars for this train
                objs = Job.objects.all().filter(team_leader=user)
                train_obj = objs.filter(train=train)
                print(train_obj)

                print('Cars affected to '+train.name+': ')
                for obj in train_obj:
                    car_in_train = obj.car 
                    print(car_in_train)
                    car_obj = objs.filter(train=train, car=car_in_train)
                    print('Parts affected to '+ str(car_in_train) + ': ')
                    for obj in car_obj:
                        part = obj.part
                        print(part)
            
                #regex to find team ids
                pattern = "(\d*)"
                results = re.findall(pattern, team_ids)
                #affect teams to parts
                exists = 0
                index = 0
            
                for id in results:
                    if id.isdigit():
                        index=index+1
                        if Tech.objects.all().filter(id=id).exists():
                            tech = Tech.objects.get(id=id)
                            response_data[id] = str(tech.name)

                            if WorkByTech.objects.filter(team_leader=user, work=work, tech=tech, date_work=date_today).exists():
                                print(tech.name + ' has already been added..')
                                exists=exists+1
                            elif WorkByTech.objects.filter(team_leader=user, tech=tech, date_work=date_today).exists():
                                print('Adding work data to '+tech.name+'..')
                                tech_work = WorkByTech.objects.get(team_leader=user, tech=tech, date_work=date_today)
                                tech_work.work.add(work)
                                tech_work.save()
                                
                            else:
                                print('Creating '+tech.name+' work data space')
                                tech_work = WorkByTech.objects.create(date_work=date_today, team_leader=user, tech=tech)
                                tech_work.work.add(work)
                                tech_work.save()
                print('index = ' + str(index) + '\r\n' + 'exists = ' + str(exists))
                if index==exists:
                    errors['team'] = 'Teammates already affected to this part'
            else:
                errors['notselected'] = 'You must select at least 1 teammate'

            #if teams are already selected and the work is already done
            if errors['team'] and errors['done']:
                pass
            else:
                errors['team'] = ''
                errors['done'] = ''

            #prepare error to json
            for key,error in errors.items():
                if error!='':
                    response_data['error'] = response_data['error'] + error + ','
                    print(error)


            #form validation
            if response_data['error']=='':
                response_data['success'] = True

                #form is valid, update WorkDone
                #work -> train, car, part 
                print('Updating WorkDone for '+ username +'..')
                done_today, created = WorkDone.objects.get_or_create(team_leader=user, date_work = date_today)
                #store the work
                done_today.work.add(work) 
                response_data['job_id'] = work.id

                print(done_today.date_work)

            #display errors
            else:
                response_data['success'] = False 

            #display status
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        
        elif status=='continue': 
            date_today = datetime.today()

            #init vars
            parts_tech=[]
            affected_trains=[]
            affected_cars=[]
            affected_parts=[]
            affected_techs=[]
            error=[]

            #check if done today and selected are equal
            try:
                #Get work done today 
                done_today = WorkDone.objects.get(team_leader=user ,date_work=date_today.strftime('%Y-%m-%d'))
                work_by_tech = WorkByTech.objects.filter(team_leader=user, date_work=date_today)
                for obj in work_by_tech:
                    parts_tech.append(WorkByTech.objects.get(pk=obj.pk))

                #Get selected elements (Selected on t_infos.html)
                selected_car = Car.objects.filter(selectedby=user)
                selected_train = Train.objects.filter(selectedby=user)
                selected_part = Part.objects.filter(selectedby=user)
                selected_tech = Tech.objects.filter(selectedby=user)

                print(done_today)
                print(parts_tech)
                #if no job today or no tech affected....
                if not done_today or not parts_tech:
                    response_data['error'] = "You didn't affect any job"
                    response_data['success'] = False
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )


                #get elements done today
                work = done_today.work.all()
                print(work)
                for job in work:
                    train_done=job.train.name
                    car_done=job.car.name
                    part_done=job.part.name

                    #compare with selected elements
                    #compare trains selected with trains affected
                    for train in selected_train:
                        if train.name==train_done:
                            if train.name in affected_trains:
                                print(train.name+' already affected!')
                            else:
                                print(train.name+' affected!')
                                affected_trains.append(train.name)
                            #compare cars selected with cars affected
                            for car in selected_car:
                                if car.name==car_done:
                                    if car.name in affected_cars:
                                        print(car.name+' already affected!')
                                    else:
                                        print(car.name+' affected!')
                                        affected_cars.append(car.name)
                                    #compare parts selected with parts affected
                                    for part in selected_part:
                                        if part.name==part_done:
                                            if part.name in affected_parts:
                                                print(part.name+' already affected!')
                                            else:
                                                print(part.name+' affected!')
                                                affected_parts.append(part.name)
                                            print(train.name + ' ' + car.name + ' ' + part.name)
                                            print(job)
                                            print('Match!')
                                            job_count=+1
                                            break
                                        else: 
                                            print('You did not affect anything to '+ train.name + ' ' + car.name + ' ' + part.name)
                                    break
                                else: 
                                    print('You didnt affect anything to '+ train.name + ' ' + car.name)
                            break
                        
                #print elements and nb of jobs                        
                print(affected_trains)
                print(affected_cars)
                print(affected_parts) 
                try:
                    if job_count:
                        print('jobs done today by ' + username + ': ' + str(job_count))
                        print(train_done, car_done, part_done) 
                except Exception as e:
                    print(traceback.format_exc())
                    
                #validate trains
                if len(affected_trains) == len(selected_train):
                    print('Trains validated')
                    print(affected_trains)
                    print('The user had selected:')
                    print(selected_train)
                else:
                    for train in selected_train:
                        if train.name not in affected_trains:
                            error.append('You didnt select anything for '+ train.name)

                #validate cars
                if len(affected_cars) == len(selected_car):
                    print('Cars validated')
                    print(affected_cars)
                    print('The user had selected:')
                    print(selected_car)
                else:
                    for car in selected_car:
                        if car.name not in affected_cars :
                            error.append('You didnt select anything for '+ car.name)
                
                #validate parts
                if len(affected_parts) == len(selected_part):
                    print('Parts validated')
                    print(affected_parts)
                    print('The user had selected:')
                    print(selected_part)
                else:
                    for part in selected_part:
                        if part.name not in affected_parts:
                            error.append('You didnt select anything for '+ part.name)
            

                #team validation
                #check if each tech has been affected to at least one part
                for obj in parts_tech:
                    tech_work = obj.work.all()
                    for tw in tech_work:
                        if tw in work:
                            if obj.tech.name not in selected_tech:
                                print(obj.tech.name+' affected!')
                                affected_techs.append(obj.tech.name)
                            break
                if len(affected_techs) == len(selected_tech):
                    print('Team validated')
                    print(affected_techs)
                    print('The user had selected:')
                    print(selected_tech)
                else:
                    for tech in selected_tech:
                        if tech.name not in affected_techs:
                            error.append('You didnt select anything for '+ tech.name)


                #display errors
                if error:
                    print(error)
                    for e in error:
                        response_data['error'] = response_data['error'] + e + ','
                        response_data['success'] = False
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )


                #FORM VALID: redirect to next page
                #RESET Selected values
                else:
                    print('Work Validation passed!')
                    response_data['success'] = True
                    ResetSelection(request, Tech, Train, Car, Part)
                    #going to the next page..
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )


            #handle additionals errors
            except Exception as e:
                if str(e)=='WorkDone matching query does not exist.':
                    response_data['error'] = "You must select a job and click 'save'"
                    response_data['message'] = str(e)
                else:
                    response_data['error'] = 'Oops! Something went wrong. Please contact IT services.'
                    response_data['message'] = str(e)
                print(e)
                print(type(e))
                print(traceback.format_exc())
                response_data['success'] = False
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )

        #404  
        elif status == 'delete':
            job_id = int(request.POST.get('job_id'))
            print('Deleting job ' + str(job_id))

            team_list = request.POST.get('tech_list')
            team = team_list.split('-')
            workbytech_list = []
            workdone_list = []
            for team_id in team:
                tech = Tech.objects.get(id = team_id)
                workbytech_list.append(WorkByTech.objects.get(date_work = datetime.today(), team_leader_id = user_id, tech_id = tech.id))
                workdone_list.append(WorkDone.objects.get(date_work = datetime.today(), team_leader_id = user_id))
            try:
                job = Job.objects.get(id=job_id)

                for work in workbytech_list:
                    work.work.remove(job)
                
                for done in workdone_list:
                    done.work.remove(job)

                response_data = {
                    'success' : True,
                    'result' : 'Job deleted'
                }
            except Exception as e:
                print(e)
                reponse_data = {
                    'success' : False,
                    'result' : 'You cannot delete this job.'
                }

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        else:
            print('error..')
            return HttpResponse('404 error')
        
#MYWORK.HTML VIEWS
class MyWorkViewClass(View):
    def get(self, request, *args, **kwargs):
        form = MyWorkForm()   
        context = {
            'profile' : Profile.objects.get(user = request.user),
            'title': 'My work today',
            'form' : form,
            'newtechform': AddNewTechForm(),
        }
        return render(request, 'teamleaderworkspace/mywork.html', context)


    #add a new tech, returns a tuple (tech.id , tech.name) to append in js
    def AddNewTech(self, request):
        data = request.POST
        newtechname = data['tech'].title()
        response_data = {}
        print('new employee: '+newtechname)
        print(type(newtechname))

        #check if tech already exists
        if Tech.objects.filter(name=newtechname).exists():
            response_data['success'] = False
            response_data['result'] = 'This name already exists'
            
        else:
            #create new user+profile and tech
            first_name = newtechname.split(' ')[0]
            last_name = newtechname.split(' ')[1]
            username = first_name+last_name
            user = User.objects.create(username = username, password=User.objects.make_random_password(), first_name = first_name, last_name = last_name)
            profile = Profile.objects.get(user = user)
            #create tech object
            tech = Tech.objects.create(name = newtechname,  profile = profile)

            response_data['success'] = True
            response_data['result'] = 'Added a new teammate successfully!'
            response_data['tech'] = (tech.id, tech.name) #get new name id from model
            print(tech)
            
        return response_data


    def post(self, request, *args, **kwargs):
        data = request.POST
        user = request.user

        print(data)
        if len(data)==2:
            print('Add a new tech')
            response_data = self.AddNewTech(request)

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            

            team_list = data.getlist('team_id')
            train_list = data.getlist('train_id')
            car_list = data.getlist('car_id')
            part_list = data.getlist('part_id')
            
            print(team_list)
            for tech in team_list:
                print(tech)
                tech = Tech.objects.get(id = tech)
                tech.selectedby.add(user)

            for train in train_list:
                train = Train.objects.get(id = train)
                train.selectedby.add(user)

            for car in car_list:
                car = Car.objects.get(id = car)
                car.selectedby.add(user)

            for part in part_list:
                part = Part.objects.get(id = part)
                print(part)
                part.selectedby.add(user)

            return HttpResponseRedirect('/../../teamleaderworkspace/Affectation')
            
#User indicate received packages
class ReceiveDeliveryViewClass(View):
    def get(self, request, *args, **kwargs):

        form = DeliveryForm()
        
        context = {
            'title' : 'Deliveries',
            'form' : form
        }

        return render(request, 'teamleaderworkspace/delivery.html', context)

    def post(self, request, *args, **kwargs):
        
        data = request.POST
        print(data)
        
        #get list of received packages
        packages = data.getlist('package')

        for package in packages:
            #get package object
            package_obj = Package.objects.get(id = package)
            
            #get stock history for workshop
            stock_history_workshop = StockHistoryWorkshop.objects.get(reference = package_obj.reference)

            #get stock history for nigel
            stock_history, created_history = StockHistory.objects.get_or_create(reference = package_obj.reference)
            #get last stock entry for nigel
            if not created_history:
                last_qty = stock_history.stock.last().qty 
            #get stock nigel today
            stock_nigel, created = Stock.objects.get_or_create(reference = package_obj.reference, date_record = datetime.today())
            

            stock_workshop = stock_history_workshop.stock.all().last()
            print(stock_workshop)
            #first stock update for today
            if created:
                #first time a stock is created
                if created_history:
                    stock_nigel.qty = package_obj.qty
                #a stock history exists
                else:
                    stock_nigel.qty = last_qty + package_obj.qty

            #Stock has already been created for today => add to previous stock
            else:
                stock_nigel.qty += package_obj.qty

            #remove received package qty from stock workshop
            stock_workshop.qty -= package_obj.qty
            stock_nigel.save()
            stock_workshop.save()
            package_obj.available_at_office = False
            package_obj.save()
        
        messages.success(request, 'Stock updated!')

        context = {
            'title' : 'My workspace',
            'profile' : Profile.objects.get(user = request.user)
        }

        return render(request, 'teamleaderworkspace/teamleaderhome.html', context)





#quality NCRs 
class QualityListView(LoginRequiredMixin, ListView):
    model = Quality
    template_name = 'teamleaderworkspace/quality.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'quality'
    ordering = ['-last_update']
    paginate_by = 20
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_queryset(self):
        
        qs = super().get_queryset()

        try:
            qs = qs.filter(id=self.kwargs['id'])
        except KeyError as e:
            print(e)
            # will land here if 'id' is not present, so we return all
            # instances and do not filter anything
            pass

        return qs
   
class QualityDetailView(LoginRequiredMixin, DetailView):
    model = Quality
    
class QualityCreateView(LoginRequiredMixin, CreateView):
    model = Quality
    form_class = QualityForm
    
    def form_valid(self, form):
        #add user to team_leader field
        form.instance.team_leader = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('teamleaderworkspace:quality')

    
    #Checking if kwargs['instance'] is None means that the code works with both CreateView and UpdateView.
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        if kwargs['instance'] is None:
            kwargs['instance'] = Quality()

        return kwargs


class QualityUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'teamleaderworkspace/quality_update.html'
    model = Quality
    form_class = QualityUpdateForm

    def form_valid(self, form):
        return super(QualityUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('teamleaderworkspace:quality')



class QualityDeleteView(LoginRequiredMixin, DeleteView):
    model = Quality
    success_url = '/teamleaderworkspace/quality/'







#CUSTOM FUNCTIONS

#reset model(s) with selected values
def ResetSelection(request, *args):
    for model in args:
        objects = model.objects.filter(selectedby__id = request.user.id)
        if objects:
            for obj in objects:
                obj.selectedby.remove(request.user)
                          
#modify the url adding a slash or not at the end
def ModifyUrl(urlname, slash):
    if Slash.objects.filter(url=urlname).exists():
        urltype = Slash.objects.get(url = urlname)
        print(urltype.slash)
        urltype.slash = slash
        urltype.save()
    else:
        Slash.objects.create(url='ReferenceTeamTable', slash=slash)

#display selected value for model(s)
def DisplaySelectedValues(*args):
    for model in args:
        if model.objects.all().filter(selected=True).exists():
            selected_objs = model.objects.all().filter(selected=True)
            print('Selected ' + model.__name__)
            for obj in selected_objs:
                print(obj)
    
