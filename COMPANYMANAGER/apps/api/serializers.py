from django.contrib.auth.models import User, Group
from apps.teamleaderworkspace.models import *
from apps.workshopworkspace.models import *
from apps.general.models import Post
from apps.users.models import Profile
from django.utils.timezone import now

from datetime import date, datetime


from rest_framework import serializers

        
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = ['id', 'teamleader', 'feedback', 'rating', 'date_work']
        depth = 1

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'name']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'reference', 'qty', 'date_record']



class StockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHistory
        fields = ['id', 'reference', 'stock', 'last_update', 'qty_per_train']
        depth = 1

class StockHistoryWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHistoryWorkshop
        fields = ['id', 'reference', 'stock', 'last_update', 'qty_per_train']
        depth = 1

class StockWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockWorkshop        
        fields = ['id', 'reference', 'qty', 'date_record']


class WorkshopJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopJob        
        fields = ['id', 'package', 'team_leader', 'date_work']
        depth = 4

class WorkDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDone        
        fields = ['id', 'team_leader', 'work', 'date_work', 'references_applied']
        depth = 4


class ProgressOnTrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressOnTrain        
        fields = ['id', 'train', 'progress_on_train', 'progress_on_car', 'progress_on_part', 'finished', 'finished_date', 'jobs', 'up_to_date', 'last_update']
        depth = 2


class WorkByTechSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkByTech        
        fields = ['id', 'work', 'tech', 'team_leader', 'date_work']
        depth = 2


class WasteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Waste        
        fields = ['id', 'reference', 'qty', 'category', 'tech', 'job_waste', 'date_waste', 'location']
        depth = 2

class WasteWorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteWorkshop       
        fields = ['id', 'reference', 'qty', 'category', 'employee', 'date_waste']
        depth = 2


class StockFilmHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockFilmHistory
        fields = ['id', 'film', 'stock', 'last_update', 'qty_per_train']
        depth = 1

class StockFilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockFilm       
        fields = ['id', 'film', 'qty', 'date_record']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package       
        fields = ['id', 'code', 'date_creation', 'team_leader', 'film_reel', 'qty', 'cut', 'packer', 'reference', 'waste', 'references_applied', 'finished', 'had_stock_update', 'available_at_office']
        depth = 3

class FilmReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmReel       
        fields = ['id', 'film', 'reel_number', 'date_received', 'finished', 'started']
        depth = 1

class ReferenceAppliedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceApplied       
        fields = ['id', 'reference', 'qty', 'date_work', 'job', 'locations', 'waste', 'tech', 'last_work', 'had_stock_update']
        depth = 3

class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    days_since_joined = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    wastemonth = serializers.SerializerMethodField()
    workmonth = serializers.SerializerMethodField()
    performancemonth = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    surfaceappliedmonth = serializers.SerializerMethodField()
    costmonth = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    def get_position(self, obj):
        return obj.get_position_display()
    
    def get_email(self, obj):
        if obj.user.email == None or obj.user.email =="":
            email = 'Unknown'
        else:
            email = obj.user.email
        return email

    def get_days_since_joined(self, obj):
        return (now() - obj.user.date_joined).days

    #get formatted image url
    def get_url(self, obj):
        return obj.image.url

    #get user last name and surname if specified
    def get_fullname(self, obj):
        return obj.name()

    #calculate wasted units of this month for this user 
    def get_wastemonth(self, obj):
        #get first day of the month
        first_day_month = datetime.today().replace(day=1)
        #user is a tech
        if obj.position == 'TN' or obj.position == 'TL':
            w = Waste.objects.filter(tech__profile = obj, date_waste__gte=first_day_month).count()
        #user is in workshop
        elif obj.position == 'WS':
            w = WasteWorkshop.objects.filter(employee = obj, date_waste__gte=first_day_month).count()
        #user is a client
        elif obj.position == 'CL':
            w = Waste.objects.filter(ncr_responsible = obj, date_waste__gte=first_day_month).count()
            w += WasteWorkshop.objects.filter(employee = obj, date_waste__gte=first_day_month).count()
            
        else:
            w = 'NA'
        return w

    #get reference applied/created number
    def get_workmonth(self, obj):
        first_day_month = datetime.today().replace(day=1)
        #user is a tech
        if obj.position == 'TN' or obj.position == 'TL':
            w = ReferenceApplied.objects.filter(tech__profile = obj, date_work__gte=first_day_month).count()
        #user is in workshop
        elif obj.position == 'WS':
            cutted = Package.objects.filter(cut__employee = obj, date_creation__gte=first_day_month)
            packed = Package.objects.filter(packer__employee = obj, date_creation__gte=first_day_month)
            w = cutted.count() + packed.count()
            for cut in cutted:
                for pack in packed:
                    #user cutted and packed the same package
                    if cut.id == pack.id:
                        w = w-1
        else:
            w = 'NA'
        return w

    def get_surfaceappliedmonth(self, obj):
        first_day_month = datetime.today().replace(day=1)
        s = 0
        #user is a tech
        if obj.position == 'TN' or obj.position == 'TL':
            references_applied = ReferenceApplied.objects.filter(tech__profile = obj, date_work__gte=first_day_month)
            for applied in references_applied:
                try:
                    s += applied.qty * applied.reference.surface
                except:
                    pass
            s = round(s, 2)
        else:
            s = 'NA'
        return s

    def get_costmonth(self, obj):
        first_day_month = datetime.today().replace(day=1)
        cw = 0
        #user is a tech
        if obj.position == 'TN' or obj.position == 'TL':
            waste = Waste.objects.filter(tech__profile = obj, date_waste__gte=first_day_month)
            c = 0
            for w in waste:
                cw += w.reference.cost * w.qty

            #total cost
            c = cw + obj.salary
            c = round(c, 2)

        #user is in workshop
        elif obj.position == 'WS':
            waste = WasteWorkshop.objects.filter(employee = obj, date_waste__gte=first_day_month)
            c = 0
            for w in waste:
                cw += w.reference.cost * w.qty

            #total cost
            c = cw + obj.salary
            c = round(c, 2)

        #user is a client
        elif obj.position == 'CL':
            waste = Waste.objects.filter(ncr_responsible = obj, date_waste__gte=first_day_month)
            wasteworkshop = WasteWorkshop.objects.filter(employee = obj, date_waste__gte=first_day_month)
            c = 0
            for w in waste:
                cw += w.reference.cost * w.qty
            for w in wasteworkshop:
                cw += w.reference.cost * w.qty

            #total cost
            c = round(cw, 2)
        
        else:
            c = 'NA'

        return c

    def get_performancemonth(self, obj):
        return 'Not yet'

    class Meta:
        model = Profile       
        fields = ['url', 'days_since_joined', 'fullname', 'wastemonth', 'performancemonth', 'surfaceappliedmonth', 'costmonth', 'workmonth', 'email', 'position']
        