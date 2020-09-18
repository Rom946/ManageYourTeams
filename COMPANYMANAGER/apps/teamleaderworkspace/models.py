from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from apps.teamleaderworkspace.managers import *
from django.core.validators import MaxValueValidator, MinValueValidator 
from apps.users.models import Profile
from django.urls import reverse
import math
from datetime import datetime
from PIL import Image

from multiselectfield import MultiSelectField


class FeedBack(models.Model):
    feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)
    teamleader = models.ForeignKey(User, on_delete=models.CASCADE)
    date_work = models.DateField()

    def __str__(self):
        return 'Feedback from ' + str(self.teamleader) + ' - ' + str(self.date_work) 

    class Meta:
        ordering = ['teamleader']


class Tech(models.Model):
    name =  models.CharField(max_length=200)
    selectedby = models.ManyToManyField(User)
    profile = models.ForeignKey(Profile, null=True, blank = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WasteCategory(models.Model):
    name = models.CharField(max_length = 20)
    description = models.TextField(max_length=2000, null=True, blank=True)
    available_for_workshop = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def info(self):
        return self.description



class Location(models.Model):
    
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name 

    def info(self):
        return str(self.description)

    class Meta:
        ordering = ['name']


class Reference(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    surface = models.FloatField(default=0)
    abbreviation = models.CharField(max_length=5, null=True, blank=True) 
    possible_locations = models.ManyToManyField(Location)
    possible_waste = models.ManyToManyField(WasteCategory)
    available_for_workshop = models.BooleanField(default = False)
    cost = models.FloatField(default=0)
    image = models.ImageField(default='train.png', upload_to='reference_pics')

    def __str__(self):
        return self.name    
    
    def save(self, *args, **kwargs):
        super(Reference, self).save(*args, **kwargs) #run parent class
        #get image path
        img = Image.open(self.image.path)

        #resize profile picture
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def location(self):
        loc = []
        for location in self.possible_locations:
            loc =+ location+', '
        return loc

class Quantity(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    
    TC1 = models.IntegerField(default=0)
    TC2 = models.IntegerField(default=0)
    M1 = models.IntegerField(default=0)
    M2 = models.IntegerField(default=0)
    M3 = models.IntegerField(default=0)
    M4 = models.IntegerField(default=0)

    def __str__(self):
        return 'Quantity for ' + str(self.reference) 


class Part(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)    
    selectedby = models.ManyToManyField(User)
    references = models.ManyToManyField(Reference)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=200)
    selectedby = models.ManyToManyField(User)
    part = models.ManyToManyField(Part)
    
    def __str__(self):
        return self.name

class Train(models.Model):
    name = models.CharField(max_length=200)
    selectedby = models.ManyToManyField(User)
    cars = models.ManyToManyField(Car)
    date_started = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-name']

#middle-man model to link parts to cars and train
class Job(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    date_started = models.DateField(auto_now_add=True)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    last_work = models.DateField(auto_now=True)

    def __str__(self):
        return self.train.name + ' - ' + self.car.name + ' - ' + self.part.name + ' - ' + self.team_leader.username

    class Meta:
        ordering = ['-train']

class Waste(models.Model):
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE)
    qty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    category = models.ForeignKey(WasteCategory, on_delete = models.CASCADE, null = True, blank = True)
    tech = models.ForeignKey(Tech, on_delete = models.CASCADE, null = True, blank = True)
    job_waste = models.ForeignKey(Job, on_delete = models.CASCADE, null = True, blank = True)
    date_waste = models.DateField(auto_now = True, blank = True, null = True)
    location = models.ManyToManyField(Location, blank = True)

    ncr_responsible = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True, default = None)

    def __str__(self):
        return str(self.reference) + ' ' + str(self.category)

    def state(self):
        return str(self.reference)+ ': ' + str(qty) + ' Wasted'


#middle-man model to link assigned teams
class WorkByTech(models.Model):
    work = models.ManyToManyField(Job)
    tech = models.ForeignKey(Tech, on_delete=models.CASCADE)
    date_work = models.DateField(auto_now=True)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    manager = TechWorkHistoryManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.date_work) +': ' + self.tech.name + ' with ' + self.team_leader.username.title()

        

class ReferenceApplied(models.Model):
    qty = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True)
    locations = models.ManyToManyField(Location)
    date_work = models.DateField(null=True, blank=True)
    job = models.ForeignKey(Job, on_delete = models.CASCADE, null=True, blank=True)
    waste = models.ManyToManyField(Waste)
    tech = models.ForeignKey(Tech, on_delete = models.CASCADE, null=True, blank=True)
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE, null=True, blank=True)
    last_work = models.DateField(auto_now_add=True, null=True, blank=True)
    had_stock_update = models.BooleanField(default = False)

    def __str__(self):
        return str(self.date_work) +': ' + str(self.reference) + ' Applied by ' + str(self.tech) + ' (Job: ' + str(self.job) + ')'

    def ref(self):
        return str(self.reference)

    def info(self):
        return str(self.reference.id) + '-' + str(self.tech.id) + '-' + str(self.job.id) 

    def code(self):
        return str(self.date_work) +'/ ' + str(self.reference) + '/' + str(self.tech) + '/' + str(self.job) + '/' +self.location()


    
    def location(self):
        loc = []
        for location in self.locations.all():
            loc.append(location.name)
        return '-'.join(loc)
    

    def quantity(self):
        return str(self.qty)

    def wasted(self):
        waste_qty = 0
        for waste in self.waste.all():
            waste_qty += waste.qty
        return waste_qty
        


    def wasted_category(self):
        waste_cat = []
        for waste in self.waste.all():
            waste_cat.append(waste.category.name)
        return '-'.join(waste_cat)

    def wasted_location(self):
        waste_locations = []
        for waste in self.waste.all():
            for loc in waste.location.all():
                if loc.name not in waste_locations:
                    waste_locations.append(loc.name)
        return '-'.join(waste_locations)

    



class WorkDone(models.Model):
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ManyToManyField(Job)
    date_work = models.DateField(null=True, blank=True)
    references_applied = models.ManyToManyField(ReferenceApplied) 
    
    objects = models.Manager()
    manager = TeamLeaderWorkHistoryManager()

    def __str__(self):
        return self.team_leader.username + ' - ' + str(self.date_work)  

    class Meta:
        ordering = ['-id']



class Stock(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    date_record = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('general:stock-nigel-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.reference) + ' - ' + str(self.date_record)

    def price(self):
        price = self.reference.price * self.qty
        return round(price, 2)




class StockHistory(models.Model):
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE)
    stock = models.ManyToManyField(Stock)
    last_update = models.DateField(auto_now=True)

    qty_per_train = models.IntegerField(default = 0)
    qty_car_single = models.ManyToManyField(Quantity)

    def get_absolute_url(self):
        return reverse('general:stock-nigel-detail', kwargs={'pk': self.pk})



    def fix_qty_per_train(self):
        quantities = self.qty_car_single.all()
        qty_total = 0
        for qty in quantities:
            qty_total = qty.TC1 + qty.TC2 + qty.M1 + qty.M2 + qty.M3 + qty.M4
            
        self.qty_per_train = qty_total
        self.save()

        return self.qty_per_train

    def __str__(self):
        return str(self.reference) + ' - Last update: ' + str(self.last_update)

    def stock_per_TC_car(self):
        stock_per_TC_car = 0
        try:
            qtys = self.qty_car_single.all()
            qty_total = 0
            for qty in qtys:
                qty_total = qty.TC1 + qty.TC2
                if qty_total == 0:
                    stock_per_TC_car = '-'
                else:
                    stock_per_TC_car = round(self.stock.last().qty/qty_total,1)
                
        except:
            stock_per_TC_car = 0

        return stock_per_TC_car
    
    def stock_per_M_car(self):
        stock_per_M_car = 0
        try:
            qtys = self.qty_car_single.all()
            qty_total = 0
            for qty in qtys:
                qty_total = qty.M1 + qty.M2 + qty.M3 + qty.M4
                if qty_total == 0:
                    stock_per_M_car = '-'
                else:
                    stock_per_M_car = round(self.stock.last().qty/qty_total,1)
        except:
            stock_per_M_car = 0

        return stock_per_M_car

    def stock_per_train(self):
        
        stock_per_train = 0
        try:
            stock_per_train = round(self.stock.last().qty/self.qty_per_train,1)
        except:
            stock_per_train = 0
        
        return stock_per_train

class ProgressOnPart(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)
    part = models.ForeignKey(Part, on_delete = models.CASCADE)

    progress_on_part = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default = 0)
    finished_date = models.DateField(null=True, blank=True)

    finished = models.BooleanField(default = False)
    jobs = models.ManyToManyField(Job)

    up_to_date = models.BooleanField(default = False)
    last_update = models.DateField(auto_now = True)


    objects =  models.Manager()
    manager = ProgressPartManager()

    def __str__(self):
        return 'Progress on ' + str(self.train) + ' - ' + str(self.car) + ' - ' + str(self.part)
 
    def update_progress(self):
        jobs = Job.objects.filter(train = self.train, car = self.car, part = self.part)
        for job in jobs:
            if job not in self.jobs.all():
                self.jobs.add(job)
        self.set_progress_on_part()
        return True

    def set_progress_on_part(self):
        jobs = self.jobs.all()
        total_qty_applied = 0

        data = {}
        for job in jobs:
            reference_applied = ''
            reference_applied = ReferenceApplied.objects.filter(job=job)
            
            for reference in reference_applied:
                if reference.qty:
                    try:
                        qty_needed, created = Quantity.objects.get_or_create(reference = reference.reference)
                        
                        if created:
                            total_qty_to_apply = 0
                        elif self.car.name == 'TC1':
                            total_qty_to_apply = qty_needed.TC1
                        elif self.car.name == 'TC2':
                            total_qty_to_apply = qty_needed.TC2
                        elif self.car.name == 'M1':
                            total_qty_to_apply = qty_needed.M1
                        elif self.car.name == 'M2':
                            total_qty_to_apply = qty_needed.M2
                        elif self.car.name == 'M3':
                            total_qty_to_apply = qty_needed.M3
                        elif self.car.name == 'M4':
                            total_qty_to_apply = qty_needed.M4
                        surface_to_cover = reference.reference.surface * total_qty_to_apply
                        total_qty_applied = reference.qty
                        surface_covered = reference.reference.surface * total_qty_applied
                        try:
                            progress_reference = round(surface_covered/surface_to_cover, 2)

                            if progress_reference>1:
                                progress_reference = 1
                        except:
                            progress_reference = 0

                        if reference.reference not in data:
                            data[reference.reference] = {
                                'to_cover' : surface_to_cover,
                                'covered' : surface_covered, 
                                'progress' : progress_reference
                            }
                        else:
                            data[reference.reference]['covered'] = data[reference.reference]['covered'] + surface_covered
                            progress_reference = round(data[reference.reference]['covered']/surface_to_cover, 2)
                            if progress_reference > 1:
                                progress_reference = 1
                                
                            data[reference.reference]['progress'] = progress_reference*100
                    except Exception as e:
                        print(e)
        
        print (data)

        progress_total = 0
        references = self.part.references.all()
        surface_to_cover_part = 0
        for reference in references: 
            qty_needed, created = Quantity.objects.get_or_create(reference = reference)
                    
            if created:
                total_qty_to_apply = 0
            elif self.car.name == 'TC1':
                total_qty_to_apply = qty_needed.TC1
            elif self.car.name == 'TC2':
                total_qty_to_apply = qty_needed.TC2
            elif self.car.name == 'M1':
                total_qty_to_apply = qty_needed.M1
            elif self.car.name == 'M2':
                total_qty_to_apply = qty_needed.M2
            elif self.car.name == 'M3':
                total_qty_to_apply = qty_needed.M3
            elif self.car.name == 'M4':
                total_qty_to_apply = qty_needed.M4

            surface_to_cover_part += total_qty_to_apply * reference.surface

        for ref in data:
            try:
                    progress_total = progress_total + data[ref]['covered'] 
            except Exception as e:
                print(e)
                progress_total = 0

        try: 
            progress_part = progress_total/surface_to_cover_part*100
            if progress_part > 100:
                progress_part = 100
        except:
            progress_refs = 0 
            progress_part = 0
        
        self.progress_on_part = round(progress_part, 2)
        if progress_part >= 100:
            self.progress_on_part
            self.finished = True
            self.finished_date = datetime.today()

        
        self.up_to_date = True
        self.save()
        print('Progress on part %s' %self.progress_on_part)

        return self.progress_on_part


class ProgressOnCar(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)
    progress_on_part = models.ManyToManyField(ProgressOnPart)

    progress_on_car = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default = 0)
    finished_date = models.DateField(null=True, blank=True)
    
    finished = models.BooleanField(default = False)
    jobs = models.ManyToManyField(Job)

    up_to_date = models.BooleanField(default = False)
    last_update = models.DateField(auto_now = True)

    objects =  models.Manager()
    manager = ProgressCarManager()

    def __str__(self):
        return 'Progress on ' + str(self.train) + ' - ' + str(self.car) 

    def update_progress(self):
        jobs = Job.objects.filter(train = self.train, car = self.car)
        for job in jobs:
            if job not in self.jobs.all():
                self.jobs.add(job)
        
        self.set_progress_on_car()

        return True

    def set_progress_on_car(self):
        parts = self.car.part.all()
        surface_to_cover_car = 0
        surface_to_cover_by_part = {}
        
        #get the surface to cover on the scope according to the car
        for part in parts:
            references = part.references.all()
            surface_to_cover_part = 0
            for reference in references:
                print('getting %s' %reference)
                qty_needed, created = Quantity.objects.get_or_create(reference = reference)
                    
                if created:
                    total_qty_to_apply = 0
                elif self.car.name == 'TC1':
                    total_qty_to_apply = qty_needed.TC1
                elif self.car.name == 'TC2':
                    total_qty_to_apply = qty_needed.TC2
                elif self.car.name == 'M1':
                    total_qty_to_apply = qty_needed.M1
                elif self.car.name == 'M2':
                    total_qty_to_apply = qty_needed.M2
                elif self.car.name == 'M3':
                    total_qty_to_apply = qty_needed.M3
                elif self.car.name == 'M4':
                    total_qty_to_apply = qty_needed.M4

                surface_to_cover_part += total_qty_to_apply * reference.surface
            
            surface_to_cover_by_part[part] = surface_to_cover_part
            surface_to_cover_car += surface_to_cover_part

        progresses_on_part = self.progress_on_part.all()
        progress_total= 0
        for progress in progresses_on_part:
            try: 
                if progress.progress_on_part != 0:
                    surface_covered = surface_to_cover_by_part[progress.part] * progress.progress_on_part/100
                    progress_total = progress_total + surface_covered
            except:
                pass
        
        
        if progress_total != 0:
            self.progress_on_car = round(progress_total/surface_to_cover_car*100, 2)
            if self.progress_on_car >= 100:
                self.progress_on_car = 100
                self.finished = True
                self.finished_date = datetime.today()
        
        else:
            self.progress_on_car = 0

        self.up_to_date = True
        self.save()
        print('Progress on car %s' %self.progress_on_car)
        return self.progress_on_car
    
    
class ProgressOnTrain(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    progress_on_car = models.ManyToManyField(ProgressOnCar)
    progress_on_part = models.ManyToManyField(ProgressOnPart)

    progress_on_train = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default = 0)
    
    finished_date = models.DateField(null=True, blank=True)
    finished = models.BooleanField(default = False)
    jobs = models.ManyToManyField(Job)

    up_to_date = models.BooleanField(default = False)
    last_update = models.DateField(auto_now = True)

    objects =  models.Manager()
    manager = ProgressTrainManager()

    def __str__(self):
        return 'Progress on %s' %str(self.train)

    def update_progress(self):
        jobs = Job.objects.filter(train = self.train)
        for job in jobs:
            if job not in self.jobs.all():
                self.jobs.add(job)
        
        self.set_progress_on_train()

        return True

    def set_progress_on_train(self):
        progress_total = 1
        progresses_on_car = self.progress_on_car.all()

        cars = self.train.cars.all()
        surface_to_cover_train = 0
        surface_to_cover_by_car = {}
        for car in cars:
            parts = car.part.all()
            surface_to_cover_car = 0
            for part in parts:
                references = part.references.all()
                surface_to_cover_part = 0
                for reference in references:
                    qty_needed, created = Quantity.objects.get_or_create(reference = reference)
                    
                    if created:
                        total_qty_to_apply = 0
                    elif car.name == 'TC1':
                        total_qty_to_apply = qty_needed.TC1
                    elif car.name == 'TC2':
                        total_qty_to_apply = qty_needed.TC2
                    elif car.name == 'M1':
                        total_qty_to_apply = qty_needed.M1
                    elif car.name == 'M2':
                        total_qty_to_apply = qty_needed.M2
                    elif car.name == 'M3':
                        total_qty_to_apply = qty_needed.M3
                    elif car.name == 'M4':
                        total_qty_to_apply = qty_needed.M4

                    surface_to_cover_part += (total_qty_to_apply * reference.surface)
                
                surface_to_cover_car += surface_to_cover_car + surface_to_cover_part

            surface_to_cover_by_car[car] = surface_to_cover_car

        print(surface_to_cover_by_car)
        progress_total = 0
        for progress in progresses_on_car:
            print(progress)
            print(progress.progress_on_car)
            surface_to_cover_train += surface_to_cover_by_car[progress.car]
            try:
                surface_covered = 0
                surface_covered = surface_to_cover_by_car[progress.car] * progress.progress_on_car/100
            except Exception as e:
                print('error : %s' %e)

            progress_total = progress_total+ surface_covered
           
        
        print('progress total %s' %progress_total)
        if progress_total != 0:
            print('Surface to cover %s' %surface_to_cover_train)
            print('Surface covered %s' %progress_total)
            self.progress_on_train = round(progress_total/surface_to_cover_train*100, 2)
            if self.progress_on_train >= 100:
                self.progress_on_train = 100
                self.finished = True
                self.finished_date = datetime.today()
        else:
            self.progress_on_train = 0
        
        self.up_to_date = True
        self.save()
        print('%s' %self)
        print('%s' %self.progress_on_train)

        return self.progress_on_train
    
    
class TrackingCode(models.Model):
    code = models.CharField(max_length = 500)
    
    package_id = models.IntegerField(null = True, blank = True)
    reference_applied = models.ForeignKey(ReferenceApplied, on_delete = models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.code

    def get_package_id(self):
        return self.code.split('/')[0]

    def useful(self):
        locations = self.reference_applied.location()
        job = self.reference_applied.job
        job = (' - ').join(str(job).split(' - ')[0:3])

        return str(job) + ' - ' + str(self.reference_applied.reference) + (' - ') + str(locations) + ' - ' + str(self.reference_applied.date_work)

    def useful_with_teamleader(self):
        if self.reference_applied.job.team_leader.first_name and self.reference_applied.job.team_leader.last_name:
            return self.useful() + ' - ' + str(self.reference_applied.job.team_leader.first_name) + ' ' + str(self.reference_applied.job.team_leader.first_name)
        else:
            return self.useful() + ' - ' + str(self.reference_applied.job.team_leader.username)


class SituationNCR(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name


class ProgressNCR(models.Model):
    name = models.CharField(max_length = 200)
    image = models.ImageField(default='pending.png', upload_to ='quality_pics')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ProgressNCR, self).save(*args, **kwargs) #run parent class
        #get image path
        img = Image.open(self.image.path)

        #resize profile picture
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Quality(models.Model):
    situation = models.ForeignKey(SituationNCR, on_delete = models.CASCADE, null = True, blank = True)
    progress = models.ForeignKey(ProgressNCR, on_delete = models.CASCADE, null = True, blank = True)

    team_leader = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)

    ncr_number = models.CharField(max_length = 200, null = True, blank = True)
    tracking_code = models.ForeignKey(TrackingCode, on_delete = models.CASCADE, null = True, blank = True)
    
    train = models.ForeignKey(Train, on_delete = models.CASCADE, null = True, blank = True)
    car = models.ForeignKey(Car, on_delete = models.CASCADE, null = True, blank = True)
    part = models.ForeignKey(Part, on_delete = models.CASCADE, null = True, blank = True)
    reference_to_replace = models.ForeignKey(Reference, on_delete = models.CASCADE, null = True, blank = True)
    location = models.ForeignKey(Location, on_delete = models.CASCADE, null = True, blank = True)

    replacement = models.BooleanField(default = False)
    replaced_by = models.ManyToManyField(Tech, blank = True, default=None)

    responsible = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True, default=None)
    default_type = models.ForeignKey(WasteCategory, on_delete = models.CASCADE, null=True, blank = True)
    date_replacement = models.DateField(null = True, blank = True, default=None)

    description = models.TextField(null = True, blank = True)
    date_record = models.DateField()

    last_update = models.DateField(auto_now = True)

    waste = models.ForeignKey(Waste, on_delete = models.CASCADE, null = True, blank = True)

    had_stock_update = models.BooleanField(default = False)

    def __str__(self):
        if self.ncr_number is not None:
            title = f'{self.ncr_number} - {self.train.name} - {self.car.name} - {self.part.name} - {self.reference_to_replace} - {self.location.name} - {self.date_record}'
        else:
            title = f'{self.train.name} - {self.car.name} - {self.part.name} - {self.reference_to_replace} - {self.location.name} - {self.date_record}'
        return title

    def getTrackingCode(self):
        pass

    def get_absolute_url(self):
        return reverse('general:quality-detail', kwargs={'pk': self.pk})





#Handle dynamic rendering for def functions
class Slash(models.Model):
    slash = models.CharField(max_length=1)
    url = models.CharField(max_length=200)






