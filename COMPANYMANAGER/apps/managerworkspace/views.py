from django.http import JsonResponse
from django.core import serializers
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

from django_tables2 import SingleTableView
from django_tables2.config import RequestConfig
from crispy_forms.helper import FormHelper
from crispy_forms.utils import render_crispy_form
import requests

from .forms import * 
from .models import *
#from .tables import *

from apps.users.models import Profile
from apps.common.decorators import ajax_required
from apps.teamleaderworkspace.models import *
from apps.workshopworkspace.models import *
from config import settings
import os
from django.db.models import Count

import traceback
import json
import re
import datetime 
from collections import ChainMap

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions



class DashboardViewClass(View):
    def isNum(self, data):
        try:
            int(data)
            return True
        except ValueError:
            return False

    def get_stats_by_tech(self, tech, period = 0):
        if period ==  0:
            references_applied = ReferenceApplied.objects.filter(date_work = datetime.date.today())
        else:
            from_date = datetime.date.today() - datetime.timedelta(days=period)
            references_applied = ReferenceApplied.objects.filter(date_work__lte=datetime.date.today(), date_work__gt=from_date)
        
        references_choice = []
        cost = 0
        count = 0
        surface = 0
        wasted = 0
        wasted_cost = 0

        if references_applied:
            for reference in references_applied:  
                if str(reference.tech) == str(tech):
                    ref_tuple = [reference.reference.id, reference.reference.name]
                    if ref_tuple not in references_choice:
                        references_choice.append(ref_tuple)

                    #cost calculation
                    try:
                        cost_applied = reference.reference.price * reference.qty
                        cost = cost + float(cost_applied)
                        #nb of ref applied
                        count = count+ reference.qty
                    except Exception as E:
                        cost_applied = 0
                        print('l77 %s ' %E)

                    #waste 
                    waste_list = reference.waste.all()
                    for waste_applied in waste_list:
                        this_waste = waste_applied.qty
                        
                        try:
                            this_waste_cost = this_waste * reference.reference.price
                        except Exception as E:
                            this_waste_cost = 0
                            print('l89 %s ' %E)
                        
                        wasted_cost = wasted_cost + this_waste_cost
                        wasted = wasted + this_waste

                    #surface
                    try:
                        surface_applied = reference.reference.surface * reference.qty
                    except Exception as E:
                            surface_applied = 0
                            print('l100 %s ' %E)
                    surface = surface + float(surface_applied)

            name=tech
            #in case object Tech
            try : 
                name = name.name
            except Exception as e:
                print(e)    
   
            tech_data = {
                'name' : name,
                'count' : count,
                'cost' : round(cost, 2),
                'wasted' : wasted,
                'wasted_cost' : round(wasted_cost, 2),
                'surface' : round(surface, 2),
                'references_choice' : references_choice,
            }


            return tech_data
        
        else:
            return False

    def get_stats_today(self):
        overall_cost_today = 0
        overall_cost_waste_today = 0
        overall_cost_references_today = 0
        
        team_list = []
        tech_data_today = []

        work_done_today = WorkDone.manager.today()
        work_by_tech_today = WorkByTech.manager.today()
        print(work_done_today)
        print(work_by_tech_today)
        

        #get team list of all the tech who worked today
        for work in work_by_tech_today:
            if work.tech not in team_list:
                team_list.append(work.tech)


            
        #get cost, nb of ref applied, surface , waste
        for tech in team_list:
            tech_data = self.get_stats_by_tech(tech)
            print(tech_data)
            overall_cost_references_today = overall_cost_references_today + tech_data['cost']
            overall_cost_waste_today = overall_cost_waste_today + tech_data['wasted_cost']
            tech_data_today.append(tech_data)

        overall_cost_today = overall_cost_references_today + overall_cost_waste_today


        costs = {
                'overall_cost_references_today' : round(overall_cost_references_today, 2),
                'overall_cost_waste_today' : round(overall_cost_waste_today, 2),
                'overall_cost_today' : round(overall_cost_today, 2)
        }
        
        data = [tech_data_today, costs]
        return data

    def get_stats_interval(self, period):
        
        overall_cost_period = 0
        overall_cost_references_period = 0
        overall_cost_waste_period = 0
        team_list = []
        tech_data_week = []
        #work_done_week = ReferenceApplied.objects.filter(date_work=from_date)

        #references = ReferenceApplied.objects.filter(date_work__lte=datetime.date.today(), date_work__gt=from_date).\
        #    values('reference').annotate(count=Count('name'))

        
        from_date = datetime.date.today() - datetime.timedelta(days=period)
        work_by_tech_period = WorkByTech.objects.filter(date_work__lte=datetime.date.today(), date_work__gt=from_date)

        #get team list of all the tech who worked today
        for work in work_by_tech_period:
            if work.tech not in team_list:
                team_list.append(work.tech)


            
        #get cost, nb of ref applied, surface , waste
        for tech in team_list:
            try:
                tech_data = self.get_stats_by_tech(tech, period)
                overall_cost_references_period = overall_cost_references_period + tech_data['cost']
                overall_cost_waste_period = overall_cost_waste_period + tech_data['wasted_cost']
                tech_data_week.append(tech_data)
            except Exception as e:
                print(e)

        overall_cost_period = overall_cost_references_period + overall_cost_waste_period
        

        costs = {
                'overall_cost_references_period' : round(overall_cost_references_period, 2),
                'overall_cost_waste_period' : round(overall_cost_waste_period, 2),
                'overall_cost_period' : round(overall_cost_period, 2)
        }
        
        data = [tech_data_week, costs]
        return data


    def get(self, request, *args, **kwargs):
        '''
        Progress on train, car done, part done
        nb of references applied by tech
        Cost today
        
        '''
        jobs = Job.objects.all()
        
        ProgressOnPart.manager.update_progress(jobs)
        ProgressOnCar.manager.update_progress(jobs)
        ProgressOnTrain.manager.update_progress(jobs)


        performance_form = PerformanceForm()
        
        try:
            data_today = self.get_stats_today()
            print('got data today')
            print(data_today)

            tech_data_today = data_today[0]
            costs_today = data_today[1]
        except Exception as e:
            print(e)
            tech_data_today = False
            costs_today = {}
            costs_today['overall_cost_today'] = 0
            costs_today['overall_cost_waste_today'] = 0
            costs_today['overall_cost_references_today'] = 0

        try:
            percentage_waste_today = costs_today['overall_cost_waste_today']/costs_today['overall_cost_today'] *100
            percentage_waste_today = round(percentage_waste_today, 2)
        except Exception as e:
            print(e)
            percentage_waste_today = 0

        '''
        Week cost - Month cost - Year cost
        KPIS FOR PERF
        '''

        try:
            data_week = self.get_stats_interval(7)
            print('got data week')

            tech_data_week = data_week[0]
            costs_week = data_week[1]
        except Exception as e:
            print(e)
            tech_data_week = False
            costs_week= {}
            costs_week['overall_cost_period'] = 0
            costs_week['overall_cost_waste_period'] = 0
            costs_week['overall_cost_references_period'] = 0

        try:
            percentage_waste_week = costs_week['overall_cost_waste_period']/costs_week['overall_cost_period'] *100
            percentage_waste_week = round(percentage_waste_week, 2)
        except Exception as e:
            print(e)
            percentage_waste_week = 0

        #tech_data_month = self.get_stats_month()
        #tech_data_year = self.get_stats_year()
        stocks = StockHistory.objects.all()
        workshop_jobs = WorkshopJob.objects.filter(date_work = datetime.date.today())      
        if not workshop_jobs.exists():
            workshop_jobs = False

        
        stocks_w_references = StockHistoryWorkshop.objects.all()
        stocks_film = StockFilmHistory.objects.all()
        print(stocks_w_references)


        progress_on_train = ProgressOnTrain.objects.all()

        referencesapplied = ReferenceApplied.objects.filter(date_work = datetime.date.today()).order_by('tech')

        ncrs = Quality.objects.all()

        context = {
                'title': 'My Workspace',
                'profile' : Profile.objects.get(user = request.user),

                'tech_data_today' : tech_data_today,
                'overall_cost_today' : costs_today['overall_cost_today'],
                'percentage_waste_today' : percentage_waste_today,
                'waste_cost_today' : costs_today['overall_cost_waste_today'],
                'ref_cost_today': costs_today['overall_cost_references_today'],
                
                'tech_data_week' : tech_data_week,
                'overall_cost_week' : costs_week['overall_cost_period'],
                'percentage_waste_week' : percentage_waste_week,
                'waste_cost_week' : costs_week['overall_cost_waste_period'],
                'ref_cost_week': costs_week['overall_cost_references_period'],

                'stocks' : stocks,
                'workshop_jobs' : workshop_jobs,
                'stocks_w_references' : stocks_w_references,
                'stocks_film': stocks_film,
                'progresses' : progress_on_train,
                'performance_form' : performance_form,

                'referencesapplied' : referencesapplied,

                'ncrs' : ncrs,
            }    

        print(datetime.date.today())

        return render(request, 'managerworkspace/dashboard.html',  context)

    def get_reference_details(self, reference):
        print(reference)
        locations_choice = []
        wastes_choice = []
        
        locations = reference.locations.all()
        possible_locations = reference.reference.possible_locations.all()
        wastes = reference.waste.all()
        


        for location in possible_locations:
            if location in locations:
                locations_choice.append([location.id, location.name, True])
            else: 
                locations_choice.append([location.id, location.name, False])

        for waste in wastes:
            wastes_choice.append([waste.id, waste.category.name])

        response_data = {
            'tech' : reference.tech.name,
            'reference' : reference.reference.name,
            'qty' : reference.qty,
            'job' : str(reference.job),
            'locations' : locations_choice,
            'wastes' : wastes_choice,
        }

        return response_data

    def get_job(self, job_str):
        #get job
        job_split = job_str.split('-')
        train = job_split[0].strip()
        car = job_split[1].strip()
        part = job_split[2].strip()

        #get objects
        jobs = Job.objects.filter(train__name = train, car__name=car, part__name=part)
        for obj in jobs:
            if str(obj) == job_str:
                return obj


    def GetProgressDetails(self, progress_id):
        data_dict = {}
        to_exclude = 0
        progress_on_part = ProgressOnPart.objects.get(id = progress_id)
        title = 'Details on ' + progress_on_part.train.name + ' - ' + progress_on_part.car.name + ' - ' + progress_on_part.part.name
        
        jobs = progress_on_part.jobs.all()

        for job in jobs:
            references = ReferenceApplied.objects.filter(job = job)
            for reference in references:

                qty_needed = Quantity.objects.get(reference = reference.reference)
                if progress_on_part.car.name == 'TC1':
                    total_qty_to_apply = qty_needed.TC1
                elif progress_on_part.car.name == 'TC2':
                    total_qty_to_apply = qty_needed.TC2
                elif progress_on_part.car.name == 'M1':
                    total_qty_to_apply = qty_needed.M1
                elif progress_on_part.car.name == 'M2':
                    total_qty_to_apply = qty_needed.M2
                elif progress_on_part.car.name == 'M3':
                    total_qty_to_apply = qty_needed.M3
                elif progress_on_part.car.name == 'M4':
                    total_qty_to_apply = qty_needed.M4

                applied = reference.qty
                try:
                    surface_covered = applied * reference.reference.surface
                except:
                    surface_covered = 0
                    applied = 0

                to_apply = total_qty_to_apply
                if to_apply != 0:

                    if reference.reference.name not in data_dict:
                        surface_to_cover = to_apply * reference.reference.surface

                        if surface_covered != 0:
                            progress_reference = surface_covered/surface_to_cover*100

                            if round(progress_reference) >= 100:
                                completed = True
                                progress_reference = 100
                            else:
                                completed = False
                        else:
                            surface_covered = 0
                            progress_reference = 0
                            completed = False

                        data_dict[reference.reference.name] = {
                            'to_apply' : to_apply,
                            'surface_to_cover' : round(surface_to_cover, 2),
                            'applied' : applied,
                            'surface_covered' : round(surface_covered, 2),
                            'progress' : round(progress_reference, 2),
                            'completed' : completed
                        } 
                    else:
                        if applied != 0:
                            data_dict[reference.reference.name]['applied'] += applied
                            data_dict[reference.reference.name]['surface_covered'] += round(surface_covered, 2)
                            try:
                                data_dict[reference.reference.name]['progress'] = round(data_dict[reference.reference.name]['surface_covered']/data_dict[reference.reference.name]['surface_to_cover']*100, 1)
                            except:
                                pass
                            if data_dict[reference.reference.name]['progress'] >= 100 : 
                                data_dict[reference.reference.name]['progress'] = 100
                                data_dict[reference.reference.name]['completed'] = True
                


                

        to_complete = 0
        completed_count = 0
        for key,val in data_dict.items():
            completed = val['completed']
            if completed == True:
                completed_count +=1
            
        
        references = progress_on_part.part.references.all()
        for reference in references:
            try:
                qty_needed = Quantity.objects.get(reference = reference)
                if progress_on_part.car.name == 'TC1':
                    total_qty_to_apply = qty_needed.TC1
                elif progress_on_part.car.name == 'TC2':
                    total_qty_to_apply = qty_needed.TC2
                elif progress_on_part.car.name == 'M1':
                    total_qty_to_apply = qty_needed.M1
                elif progress_on_part.car.name == 'M2':
                    total_qty_to_apply = qty_needed.M2
                elif progress_on_part.car.name == 'M3':
                    total_qty_to_apply = qty_needed.M3
                elif progress_on_part.car.name == 'M4':
                    total_qty_to_apply = qty_needed.M4

                qty_total = total_qty_to_apply
                if qty_total > 0 :
                    to_complete += 1
                    if reference.name not in data_dict:
                        data_dict[reference.name] = {
                                'to_apply' : qty_total,
                                'surface_to_cover' : round(qty_total * reference.surface, 2),
                                'applied' : 0,
                                'surface_covered' : 0,
                                'progress' : 0,
                                'completed' : False
                            } 
            except Exception as e:
                print(e)


        completed_string = 'Completed : ' + str(completed_count) + ' / ' + str(to_complete)

        response_data = {
            'success': True,
            'title' : title,
            'completed' : completed_string,
            'data_list' : data_dict
        }

        return response_data
    

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data['action'])

        if data['action'] == 'get reference details':
            print(data)
            jobs_list = []
            response_data = []
            reference_id = int(data['reference_id'])
            tech_name = data['tech_name']
            tech = Tech.objects.get(name = tech_name)
            date = data['date']
            if date == 'today':
                date = datetime.datetime.today()
                reference = ReferenceApplied.objects.get(reference_id = reference_id, tech_id = tech.id, date_work=datetime.date.today())
                has_job = False  
                response_data = self.get_reference_details(reference)
                date_work = datetime.date.today()

            elif date == 'week':
                date = datetime.date.today() - datetime.timedelta(days=7)
                
                if int(data['job']) == 0:
                    references = ReferenceApplied.objects.filter(reference_id = reference_id, tech = tech, date_work__lte=datetime.date.today(), date_work__gt=date)
                    for reference in references:
                        jobs_choice = [reference.job.id, str(reference.job)]
                        if jobs_choice not in jobs_list:
                            jobs_list.append(jobs_choice)
                    has_job = True
                    date_work = False

                else:
                    job = Job.objects.get(id = int(data['job']))
                    reference = ReferenceApplied.objects.get(reference_id = reference_id, job=job , tech = tech, date_work__lte=datetime.date.today(), date_work__gt=date)
                    has_job = False  
                    date_work = reference.date_work
                    response_data = self.get_reference_details(reference)


            print(jobs_list)
            print(response_data)

            context = {
                'success' : True,
                'data' : response_data,
                'has_job' : has_job,
                'jobs_list' : jobs_list,
                'date' : str(date_work)
            }
        
        elif data['action'] == 'get waste qty':
           
            waste_id = int(json.loads(data['waste_id'])[0])  

            waste = Waste.objects.get(id = waste_id)

            waste_qty = waste.qty

            context = {
                'success' : True,
                'waste_qty' : waste_qty
            }

        elif data['action'] == 'save changes':
            print(data)
            locations = data['locations']
            qty = data['qty']
            job = data['job']
            tech = data['tech']
            date = data['date']
            reference = data['reference']
            try:
                waste_qty = data['waste_qty']
                waste_id = data['waste_id']
            except Exception as e:
                print(e) 
            
            job = self.get_job(job)
            tech = Tech.objects.get(name = tech)
            reference = Reference.objects.get(name = reference)
            print(reference)

            if date == 'today':
                date_today = datetime.datetime.today() 
                reference_applied = ReferenceApplied.objects.get(reference = reference, job = job, tech = tech, date_work = date_today)
                print(reference_applied)
            elif date == 'week':
                date_today = datetime.datetime.today() 
                from_date = datetime.date.today() - datetime.timedelta(days = 7)
                reference_applied = ReferenceApplied.objects.get(reference_id = reference.id, job_id = job.id, tech_id = tech.id, date_work__lte = date_today, date_work__gte = from_date)
                print(reference_applied)
            
            try:    
                waste = Waste.objects.get(id = waste_id)
                if waste:
                    waste.qty = waste_qty
                    waste.save()
            except Exception as e:
                print(e)


            if locations == '':
                context = {
                    'success' : False,
                    'error' : 'You didnt select a location.'
                }
            else:
                print('Updating ' + str(reference_applied.reference))
                reference_applied.qty = qty
                reference_applied.locations.clear()

                locations_list = locations.split(',')
                print(locations_list)
                for location in locations_list:
                    print(type(location))
                    print(location)
                    if self.isNum(location):#to fix
                        location_obj = Location.objects.get(id = location)
                        reference_applied.locations.add(location_obj)
                        
                    

                # append data to context 
                if date == 'week':
                    tech_data = self.get_stats_by_tech(tech, 7)
                elif date == 'today':
                    tech_data = self.get_stats_by_tech(tech)
                print(tech_data)

                reference_applied.save()

                context = {
                    'success' : True,
                    'tech_data' : tech_data,
                }

        elif data['action'] == 'get progress details':
            print('Getting progress details')
            progress_id = int(data.get('progress_id'))
            context = self.GetProgressDetails(progress_id)
            print(context)

        elif data['action'] == 'recalculate progress':
            progress_id = int(data.get('progress_id'))

            progress = ProgressOnTrain.objects.get(id = progress_id)
            progress.up_to_date = False
            progress.save()

            context = {
                'success' : True
            }

        else:
            context = {
                'success' : False,
                'error' : 'Action unknown... contact IT services'
            }

        return HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )





class ChartViewClass(View):
    def get(self, request, *args, **kwargs):

        form = GraphForm()
        stocks_nigel = StockHistory.objects.all()
        stocks_workshop = StockHistoryWorkshop.objects.all()
        stocks_film = StockFilmHistory.objects.all()
        trains = Train.objects.all()
        categories_waste = WasteCategory.objects.all()
        techs = Tech.objects.all()
        locations = Location.objects.all()

        context = {
            'title' : 'Charts',
            'stocks_nigel' : stocks_nigel,
            'stocks_workshop' : stocks_workshop,
            'stocks_film' : stocks_film,
            'trains' : trains,
            'categories' : categories_waste,
            'techs' : techs,
            'locations' : locations
        }
        return render(request, 'managerworkspace/charts.html', context)

    def post(self, request, *args, **kwargs):

        pass



class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        stock_labels = []
        stock_data = []

        stocks_history = StockHistory.objects.all()
    
        for stock in stocks_history:
            try:
                stock_data.append(stock.stock.last().qty)
                stock_labels.append(stock.reference)
            except Exception as e:
                print(e)

        stocks = {
            "labels": json.dumps(stock_labels),
            "data": json.dumps(stock_data),
        }   


        data = {
            'stocks' : stocks
        }


        return Response(stocks)




class HighlightsClassView(View):
    def get(self, request, *args, **kwargs):
        '''
        #build api url
        profiles_api_url = 'http://' + request.META['HTTP_HOST'] + '/api/v1/profiles'
        #get data
        data_profiles = requests.get(profiles_api_url)
        profiles = data_profiles.json()

        #print(profiles)
        '''

        context = {
            'title': 'Highlights',
        }

        return render(request, 'managerworkspace/highlights.html', context)
