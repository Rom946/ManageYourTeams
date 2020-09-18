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

from .forms import * 
from .models import *
#from .tables import *

from apps.users.models import Profile
from apps.common.decorators import ajax_required
from apps.teamleaderworkspace.models import *
from apps.teamleaderworkspace.forms import FeedbackForm

from django.db.models import Count

import traceback
import json
import re
import datetime 
from collections import ChainMap

def homepage(request):
    
    return render(request, 'workshopworkspace/workshophome.html',  {'title': 'My Workspace', 'profile' : Profile.objects.get(user = request.user),})


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

        #UPDATE STOCK REFERENCES WORKSHOP
        recap = WorkshopJob.objects.get(team_leader_id=request.user.id, date_work = datetime.date.today()).package.all()
        for package in recap:
            if not package.had_stock_update:
                stock_history, created_history = StockHistoryWorkshop.objects.get_or_create(reference = package.reference)
                if not created_history:
                    try:
                        last_stock_qty = stock_history.stock.last().qty 
                    except Exception as e:
                        print(e)
                        last_stock_qty = 0
                stock, created = StockWorkshop.objects.get_or_create(reference = package.reference, date_record = datetime.date.today())
                
                #created a new stock object
                if created:
                    #created a stock history object => first time stock is updated
                    if created_history:
                        print('created a new stock history object')
                        stock.qty = package.qty
                        stock.save()
                        stock_history.stock.add(stock)
                    
                    #get last stock qty and update  
                    else:
                        print('found a stock history...')
                        print('last stock %s' %stock_history.stock.last())
                        print('last stock qty: %s' %last_stock_qty)
                        stock.qty = last_stock_qty + package.qty
                        stock.save()
                
                #update stock
                else:
                    print('found an existing stock for today.. Updating')
                    stock.qty += package.qty
                    stock.save()                

                package.had_stock_update = True
                package.save()
                print('******STOCKS UPDATED******')


        context = {
            'title' : 'My workspace',
            'profile' : Profile.objects.get(user = request.user),

        }

        return render(request, 'workshopworkspace/workshophome.html', context)
    else:
        messages.error(request, 'You must give a feedback')
        #redirect to feedback
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



class FeedbackWorkshopViewClass(View):

    #delete package from package id
    def DeletePackage(self, package_id):
        package = Package.objects.get(id = package_id)

        package.delete()

        response_data = {
            'success' : True,
            'result' : 'Deleted package ' + str(package_id)
        }
        return response_data


    #give feedback forms and packages codes created today
    def get(self, request, *args, **kwargs):
        #check if there is a feedback object
        feedback = FeedBack.objects.filter(teamleader_id = request.user.id, date_work = datetime.date.today())

        if feedback:
            feedback = FeedBack.objects.get(teamleader_id = request.user.id, date_work = datetime.date.today())
            feedback_form = FeedbackForm(instance = feedback)
        else:
            feedback_form = FeedbackForm()

        print(datetime.date.today())
        packages_code = WorkshopJob.objects.get(date_work = datetime.date.today(), team_leader_id = request.user.id).package.all()

        film_reel_form = FinishReelForm()

        context = {
            'title' : 'Feedback',
            'profile' : Profile.objects.get(user = request.user),
            'film_reel_form' : film_reel_form,
            'feedback' : feedback_form,
            'packages_code': packages_code
        }
        return render(request, 'workshopworkspace/feedback_workshop.html', context)
    

    #give feedback forms and packages codes created today
    #handle ajax calls to edit/delete packages and finish reels
    def post(self, request, *args, **kwargs):
        data = request.POST
        
        print(data)
        
        #check if there is an action to perform
        try: 
            if data['action']:
                action = True
                pass
        except:
            action = False

        if action:

            #user indicate a film reel as finished. Incrementation handled in signals.py
            if data['action'] == 'finish film reel':
                ids = data.getlist('reel_ids[]')
                films = []
                for id in ids:
                    film_single = FilmReel.objects.get(id = id)
                    film_single.finished = True
                    film_single.save()
                    films.append(str(film_single))
                
                #display selected finished reels
                response_data = {
                    'success' : True,
                    'result' : 'The following films are now finished: %s' %str((' - ').join(films))
                }

            #user edit a package
            if data['action'] == 'edit':
                package = Package.objects.get(id = int(data.get('package_id')))
                
                waste_choices = []
                wastes = package.waste.all()
                for waste in wastes:
                    waste_choices.append([waste.id, str(waste), False, False])

                packer_choices = []
                packers = Packer.objects.all()
                for packer in packers:
                    if packer.employee.user.username == package.packer.employee.user.username:
                        packer_choices.append([packer.id, packer.employee.user.username, True, True]) 
                    else:
                        packer_choices.append([packer.id, packer.employee.user.username, False, False]) 
                
                cutter_choices = []    
                cutters = Cut.objects.all()
                for cutter in cutters:
                    if cutter.employee.user.username == package.cut.employee.user.username:
                        cutter_choices.append([cutter.id, cutter.employee.user.username, True, True]) 
                    else:
                        cutter_choices.append([cutter.id, cutter.employee.user.username, False, False]) 

                film_choices = []    
                films = FilmReel.objects.filter(finished = False)
                for film in films:
                    if film in package.film_reel.all():
                        film_choices.append([film.id, str(film), True, True]) 
                    else:
                        film_choices.append([film.id, str(film), False, False]) 

                response_data = {
                    'success' : True,
                    'date_creation' : str(package.date_creation),
                    'reference' : str(package.reference),
                    'film_reels' : film_choices,
                    'qty' : package.qty,
                    'cutter_choices' : cutter_choices,
                    'packer_choices' : packer_choices,
                    'waste_choices' : waste_choices
                }

            #user modifying waste
            elif data['action'] == 'load waste':
                waste = WasteWorkshop.objects.get(id = int(data.get('waste_id')))
                waste_category_choices = []    
                waste_categories = WasteCategory.objects.filter(available_for_workshop=True)
                for category in waste_categories:
                    if str(category.name) == str(waste.category.name):
                        waste_category_choices.append([category.id, category.name, True, True]) 
                    else:
                        waste_category_choices.append([category.id, category.name, False, False]) 
                
                waste_qty = waste.qty

                response_data = {
                    'success' : True,
                    'waste_category' : waste_category_choices,
                    'waste_qty' : waste_qty
                }


            elif data['action'] == 'save':
                package_id = data.get('package_id')
                cutter = Cut.objects.get(id = int(data.get('cutter')))
                packer = Packer.objects.get(id = int(data.get('packer')))
                qty = int(data.get('qty'))
                waste_id = data.get('waste')
                waste_qty = data.get('waste_qty')
                waste_category = data.get('waste_category')

                package = Package.objects.get(id = int(package_id))
                print('Editing ' + str(package))
                wastes = package.waste.all()
                print(wastes)
                #change cutter in waste if changed
                if str(cutter)!=str(package.cut):
                    for waste in wastes:
                        print(waste.employee.user.username)
                        print(waste.employee.user.id)
                        print(package.cut.employee.user.username)
                        print(package.cut.employee.user.id)
                        if waste.employee.user.id == package.cut.employee.user.id:
                            print('Changing waste for ' + str(cutter.employee.user) + '...')

                            waste.employee = cutter.employee
                            waste.save()

                            break 


                #change packer in waste if changed
                if str(packer)!=str(package.packer):
                    for waste in wastes:
                        if waste.employee.user.id == package.packer.employee.user.id :
                            print('Changing waste for ' + str(packer.employee.user) + '...')

                            waste.employee = packer.employee
                            waste.save()

                            break

                package.cut = cutter
                package.packer = packer
                if package.had_stock_update:
                    stock_difference_qty = package.qty - qty
                    stock = StockWorkshop.objects.get(date_record = datetime.date.today(), reference = package.reference)
                    #if nothing changed => stock_difference_qty = 0
                    stock.qty = stock.qty - stock_difference_qty 
                    stock.save()
                else:
                    package.had_stock_update = True
                package.qty = qty

                package.save()
                reference = package.reference

                if json.loads(waste_id):
                    if waste_qty != '' or waste_qty != 0:
                        waste = WasteWorkshop.objects.get(id = int(waste_id))
                        waste_category = WasteCategory.objects.get(id = int(waste_category))
                        
                        waste.qty = int(waste_qty)
                        waste.category = waste_category
                        if package.had_stock_update:
                            stock_difference_waste_qty = waste.qty - int(waste_qty)
                            stock.save()
                        waste.save()
                
                package.encode(request)
                print('New code: ' + str(package))


                response_data = {
                    'success' : True,
                    'result' : 'Package has been edited',
                    'code' : str(package)
                }

            elif data['action'] == 'delete':
                print('Deleting..')
                response_data = self.DeletePackage(data.get('package_id'))

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        #coming from mywork.html
        else:
            #check if there is a feedback object
            feedback = FeedBack.objects.filter(teamleader_id = request.user.id, date_work = datetime.date.today())
            print(feedback)
            if feedback:
                feedback = FeedBack.objects.get(teamleader_id = request.user.id, date_work = datetime.date.today())
                feedback_form = FeedbackForm(instance = feedback)
            else:
                feedback_form = FeedbackForm()

            #display all the packages created today by the user
            try:
                packages_code = WorkshopJob.objects.get(date_work = datetime.date.today(), team_leader_id = request.user.id).package.all()
            except:
                packages_code = False
            print(packages_code)

            film_reel_form = FinishReelForm()

            context = {
                'title' : 'Feedback',
                'profile' : Profile.objects.get(user = request.user),
                'feedback' : feedback_form,
                'film_reel_form' : film_reel_form,
                'packages' : packages_code
            }
            return render(request, 'workshopworkspace/feedback_workshop.html', context)


#Workshop work reporting
class MyWorkViewClass(View):
    
    #get packages done today
    def GetInfoDoneToday(self, request):
        package = Package.objects.filter(team_leader_id = request.user.id, date_creation = datetime.datetime.today())
        if package.exists():
            return package
        else:
            return False

    #give the 2 forms to front 
    def get(self, request, *args, **kwargs):
        recap = self.GetInfoDoneToday(request)
        form = PackageNumberForm(initial={'date_creation': datetime.date.today()})
        form2 = AddNewEmployeeForm()
        form3 = AddNewReelForm()
        context = {
            'title' : 'My work today',
            'profile' : Profile.objects.get(user = request.user),
            'recap' : recap,
            'form' :  form,
            'form2' : form2,
            'form3' : form3
        }

        return render(request, 'workshopworkspace/workshop_work.html', context)

    #add a new tech, returns a tuple (tech.id , tech.name) to append in js
    def AddNewTech(self, request):
        data = request.POST
        newtechname = data['tech'].title()
        response_data = {}
        print('new employee: '+newtechname)
        print(type(newtechname))
        #create new user+profile and tech
        first_name = newtechname.split(' ')[0]
        last_name = newtechname.split(' ')[1]
        username = first_name+last_name
        print(data)

        #check if profile already exists
        if Profile.objects.filter(user__username=username).exists():
            profile = Profile.objects.get(user__username = username)
            
            position = int(data['as'])
            
            if position == 0:
                if Cut.objects.filter(employee = profile).exists():
                    response_data['result'] = 'This name already exists'
                    response_data['success'] = False
                else: 
                    obj = Cut.objects.create(employee = profile)
                    response_data['success'] = True
                    response_data['result'] = 'Added a new teammate successfully!'
                    response_data['tech'] = (str(obj.id), newtechname) 
                    response_data['position'] = position

            elif position == 1:
                if Packer.objects.filter(employee = profile).exists():
                    response_data['result'] = 'This name already exists'
                    response_data['success'] = False
                else:
                    obj = Packer.objects.create(employee = profile)
                    response_data['success'] = True
                    response_data['result'] = 'Added a new teammate successfully!'
                    response_data['tech'] = (str(obj.id), newtechname) 
                    response_data['position'] = position

        #profile doesnt exist
        else:
            user = User.objects.create(username = username, password=User.objects.make_random_password(), first_name = first_name, last_name = last_name)
            profile = Profile.objects.get(user = user)
            #create tech object
            
            position = int(data['as'])
            if position == 0:
                obj = Cut.objects.create(employee = profile)
            elif position == 1:
                obj = Packer.objects.create(employee = profile)

            response_data['success'] = True
            response_data['result'] = 'Added a new teammate successfully!'
            response_data['tech'] = (str(obj.id), newtechname) 
            response_data['position'] = position
            
        return response_data
    
    #add a new film reel, returns a tuple (filmreel.id , filmreel.reel_number) to append in js
    def AddNewFilmReel(self, request):
        data = request.POST
        film_id = data.get('film').title()
        reel_number = data.get('reel_nb')
        response_data = {}
        print('new film reel for: '+ film_id)
        print('film number : %s' % reel_number)

        film = Film.objects.get(id = film_id)
        film_reel, created = FilmReel.objects.get_or_create(film = film, date_received = datetime.date.today(), reel_number = reel_number)
        
        if not created:
            film_reels = FilmReel.objects.filter(film = film, date_received = datetime.date.today())
            k=1
            for obj in film_reels: 
                reel_number_reformat = reel_number + '-%s' %k
                film_reel, sub_created = FilmReel.objects.get_or_create(film = film, date_received = datetime.date.today(), reel_number = reel_number_reformat)
                if sub_created :
                    break
                else:
                    k+=1

        response_data = {
            'success' : True,
            'result' : 'Added a new film reel number %s successfully!' %str(film_reel),
            'film_reel' : (str(film_reel.id), str(film_reel)) 
        }
            
        return response_data

    #save data sent via ajax and return data table data
    def SaveData(self, request):
        try:
            data = request.POST
            print(data)
            date_creation = data.get('date_creation')
            film_reel_nbs = data.getlist('film_reel_nbs[]')
            print(film_reel_nbs)
            print(date_creation)
            
            qty = int(data.get('qty'))
            cutter_id = int(data.get('cutter'))
            packer_id = int(data.get('packer'))
            reference = int(data.get('references'))
            waste_qty = data.get('waste_qty')
            if waste_qty != '-':
                waste_qty = int(waste_qty)
            else: waste_qty = 0
            waste_category = data.get('waste_category')
            involved = data.get('involved')
            if involved != '-':
                involved = int(involved)


            #get objs
            cutter = Cut.objects.get(id = cutter_id)       
            packer = Packer.objects.get(id = packer_id)
            reference = Reference.objects.get(id=reference)

            
            package = Package.objects.create(team_leader_id = request.user.id, date_creation = date_creation, cut = cutter, packer = packer, reference=reference, qty = qty)
            job, job_created = WorkshopJob.objects.get_or_create(date_work = datetime.date.today(), team_leader_id = request.user.id)
            
            #indicate the used film reels as started
            film_list = []
            for reel_id in film_reel_nbs:
                print(reel_id)
                film_reel = FilmReel.objects.get(id = int(reel_id))
                film_reel.started = True
                film_reel.save()
                package.film_reel.add(film_reel)
                film_list.append(film_reel.film.id)

            #create package tracking number
            package.encode(request)
            print('waste')
            print(waste_qty)
            #determine who's fault if waste
            if waste_qty != 0:
                print('involved')
                print(involved)
                waste_category = WasteCategory.objects.get(id = waste_category)
                #cutter
                if involved == 0:
                    print('getting cutter')
                    involved = cutter.employee
                #packer
                elif involved == 1:
                    print('getting packer')
                    involved = packer.employee
                #teamleader
                elif involved == 2:
                    print('getting teamleader')
                    teamleader = Profile.objects.get(user_id = request.user.id)
                    involved = teamleader
                #team
                elif involved == 3:
                    print('getting team')
                    teamleader = Profile.objects.get(user_id = request.user.id)
                    involved = [cutter.employee, packer.employee, teamleader]
                #supplier
                elif involved == 4:
                    print('getting supplier')
                    print(film_list)
                    for film_id in film_list:
                        involved = []
                        film = Film.objects.get(id=film_id)
                        supplier = film.supplier
                        supplier, supplier_created = User.objects.get_or_create(username=supplier)
                        supplier, supplier_created = Profile.objects.get_or_create(user=supplier)
                        involved.append(supplier)
                #other
                elif involved == 5:
                    print('getting other')
                    other, other_created = User.objects.get_or_create(username = 'other')
                    other, other_created = Profile.objects.get_or_create(user = other)
                    involved = other

                waste_list = []
                try:
                    for inv in involved:
                        waste, waste_created = WasteWorkshop.objects.get_or_create(date_waste = date_creation, reference = reference, category = waste_category, employee = inv)
                        waste_list.append(waste)

                except Exception as err:
                    print(err)
                    waste, waste_created = WasteWorkshop.objects.get_or_create(date_waste = date_creation, reference = reference, category = waste_category, employee = involved)
                    waste_list.append(waste)

                for waste in waste_list:
                    waste.qty = waste.qty + waste_qty
                    waste_qty = waste.qty
                    waste.save()
                    package.waste.add(waste)
            
            package.save()
            #build package number
            package.encode(request)

            #add the package to WorkDone
            job.package.add(package)
            print('New package created! Package number: ' + str(package))
            
            #build a list of involved people for waste
            if involved!='-':
                try:
                    print(involved)
                    involved_list = []
                    for inv in involved:
                        if inv.user.first_name == '' or inv.user.last_name=='':
                            inv = inv.user.username
                        else:
                            inv = inv.user.first_name + ' ' + inv.user.last_name
                        involved_list.append(inv)
                        
                        print(inv)
                    print(involved)
                    involved = (', ').join(involved_list)
                except Exception as er:
                    print(er)
                    if involved.user.first_name == '' or involved.user.last_name=='':
                        involved = involved.user.username
                    else:
                        involved = involved.user.first_name + ' ' + involved.user.last_name
                        

            response_data = {
                'success' : True,
                'date_creation' : date_creation,
                'package_id' : package.id,
                'film_name' : str(package.get_list_reel_nbs()),
                'cutter' : str(cutter),
                'packer' : str(packer),
                'reference' : str(reference),
                'waste_qty' : str(waste_qty),
                'waste_category' : str(waste_category),
                'involved' : involved,
                'code' : str(package)
            }
        except Exception as e :
            print(str(e) + ' - ' + str(type(e)))
            response_data = {
                'success' : False,
                'result' : 'Oops. Something went wrong! Please contact IT services.'
            }
        print(response_data)
        return response_data

    #delete package from package id
    def DeletePackage(self, package_id):
        print(package_id)
        package = Package.objects.get(id = int(package_id))
        wastes = package.waste.all()
        try:
            if package.had_stock_update:
                stock = StockWorkshop.objects.get(reference = package.reference, date_record = datetime.date.today())
                wastes_qty = 0
                for waste in wastes:
                    wastes_qty = wastes_qty + waste.qty
                stock.qty = stock.qty - package.qty
                
                '''
                #update film stock
                stock_film = StockFilm.objects.get(film = package.film_name, date_record = datetime.date.today())
                #layout_plan = LayoutPlan.objects.get(film = package.film_name, reference = package.reference)
                film_qty = (package.qty + wastes_qty)/layout_plan.nb_of_ref_possible
                stock_film.qty = stock_film.qty + film_qty
                stock_film.save()
                '''
                stock.save()
                stock.save()
        except Exception as e:
            print(e)
        package.delete()
        for waste in wastes:
            waste.delete()


        response_data = {
            'success' : True,
            'result' : 'Deleted package ' + str(package_id)
        }
        return response_data

    #actions: save, delete, continue 
    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data.get('action'))

        #add a new employee
        if data.get('action') == 'add':
            print('Add a new tech..')
            response_data = self.AddNewTech(request)
            print(response_data)

        #add a new reel number
        elif data.get('action') == 'add reel nb':
            print('Add a new film reel..')
            response_data = self.AddNewFilmReel(request)
            print(response_data)

        #user clicked save => save the data
        elif data.get('action') == 'save':
            print('Saving data..')
            response_data = self.SaveData(request)
            
        #user deleted a package he previously entered    
        elif data.get('action') == 'delete':
            print('Deleting..')
            response_data = self.DeletePackage(data.get('package_id'))

        #user hit continue
        elif data.get('action') == 'continue':

            #user created at least one package => redirection
            if WorkshopJob.objects.filter(team_leader_id = request.user.id, date_work = datetime.date.today()).exists():
                response_data = {
                    'success' : True,
                    'result' : 'You are being redirected..'
                }
            #user didnt create any package => error
            else:
                response_data = {
                    'success' : False,
                    'result' : "You didn't create a package..."
                }
        
        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )



