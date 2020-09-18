from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from apps.users.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator 
from apps.teamleaderworkspace.models import Reference, WasteCategory, ReferenceApplied, Quantity
from PIL import Image


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    relationship_date_created = models.DateField()
    rating = models.IntegerField(default = 5)
    def __str__(self):
        return self.name

class Printer(models.Model):
    name = models.CharField(max_length=200)
    relationship_date_created = models.DateField()
    rating = models.IntegerField(default = 5)
    def __str__(self):
        return self.name

class Film(models.Model):
    name = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE)
    price = models.FloatField(default = 0)
    L = models.FloatField(default = 0)
    H = models.FloatField(default = 0)
    image = models.ImageField(default='photographic-film.png', upload_to='film_pics')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Film, self).save(*args, **kwargs) #run parent class
        #get image path
        img = Image.open(self.image.path)

        #resize profile picture
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def surface(self):
        return str(self.L * self.H)

class Cut(models.Model):
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee.user.first_name) +' '+ str(self.employee.user.last_name)


class Packer(models.Model):
    employee = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employee.user.first_name) +' '+ str(self.employee.user.last_name)

class WasteWorkshop(models.Model):
    employee = models.ForeignKey(Profile, on_delete = models.CASCADE )
    date_waste = models.DateField(auto_now = True, null = True, blank = True)
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE)
    qty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    category = models.ForeignKey(WasteCategory, on_delete = models.CASCADE, null = True, blank = True)
    

    def __str__(self):
        return str(self.date_waste) + ': ' + str(self.reference) + ' - ' + str(self.employee.user) 

class FilmReel(models.Model):
    film = models.ForeignKey(Film, on_delete = models.CASCADE)
    reel_number = models.CharField(max_length = 200, blank=True, null=True, default = '')
    date_received = models.DateField(blank=True, null=True)
    finished = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    def __str__(self):
        return str(self.film) + ' - ' + str(self.reel_number) + ' - ' + str(self.date_received)

class Package(models.Model):
    code = models.CharField(max_length=200, null= True, blank=True)
    date_creation = models.DateField(null=True, blank=True)
    team_leader = models.ForeignKey(User, on_delete= models.CASCADE)
    film_reel = models.ManyToManyField(FilmReel)
    qty = models.IntegerField(default = 0)
    cut = models.ForeignKey(Cut, on_delete=models.CASCADE)
    packer = models.ForeignKey(Packer, on_delete = models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE, null = True, blank=True)
    waste = models.ManyToManyField(WasteWorkshop, blank=True)
    had_stock_update = models.BooleanField(default = False)
    references_applied = models.ManyToManyField(ReferenceApplied, blank = True)
    finished = models.BooleanField(default = False)
    available_at_office = models.BooleanField(default = True)

    def get_list_reel_nbs(self):
        nbs = self.film_reel.all()
        string_nbs = ''
        for nb in nbs:
            string_nbs = string_nbs + nb.reel_number +'-' 
        reel_nbs = '.'.join(string_nbs.split('-'))
        return reel_nbs

    def encode(self, request):
        
        reel_nbs = self.get_list_reel_nbs()
        self.code = str(self.id) + '/' + str(self.date_creation) + '/' + str(request.user.username) + '/' + str(self.film_reel.first().film) + '/' + reel_nbs + '/'+ str(self.cut) + '/' + str(self.packer) + '/' + str(self.reference) + '/' + str(self.qty)
        self.save()
        return self.code

    def __str__(self):
        if self.code:
            return self.code
        else:    
            return str(self.id) + '/' + str(self.date_creation) + '/' + str(self.cut) + '/' + str(self.packer) + '/' + str(self.reference) + '/' + str(self.qty)
    

class WorkshopJob(models.Model):
    package = models.ManyToManyField(Package)
    date_work = models.DateField()
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date_work) + ' ' + str(self.team_leader)


class StockFilm(models.Model):
    film = models.ForeignKey(Film, on_delete = models.CASCADE)
    date_record = models.DateField(auto_now=True)
    qty = models.IntegerField(default = 0)


    def __str__(self):
        return str(self.date_record) + ': ' + str(self.film)
        
    def get_absolute_url(self):
        return reverse('general:stock-film-detail', kwargs={'pk': self.pk})

    def price(self):
        price = self.film.price * self.qty 
        return round(price, 2)

class StockFilmHistory(models.Model):
    film = models.ForeignKey(Film, on_delete = models.CASCADE)
    stock = models.ManyToManyField(StockFilm)
    last_update = models.DateField(auto_now_add=True)


    qty_per_train = models.FloatField(default = 0)

    def __str__(self):
        return str(self.film) + ' - Last update: ' + str(self.last_update)
    
    def get_absolute_url(self):
        return reverse('general:stock-film-detail', kwargs={'pk': self.pk})

    
    def stock_per_train(self):
            
        stock_per_train = 0
        try:
            stock_per_train = round(self.stock.last().qty/self.qty_per_train, 1)
        except:
            stock_per_train = 0
        
        return stock_per_train
    


class LayoutPlan(models.Model):
    film = models.ForeignKey(Film, on_delete = models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete = models.CASCADE)
    nb_of_ref_possible = models.IntegerField(default = 1)
    
    def __str__(self):
        return str(self.film) + ' - ' + str(self.reference)

class StockWorkshop(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.PROTECT)
    qty = models.IntegerField(default=0)
    date_record = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.reference) + ' - ' + str(self.date_record)
    
    def get_absolute_url(self):
        return reverse('general:stock-workshop-detail', kwargs={'pk': self.pk})


    def price(self):
        price = self.reference.price * self.qty
        return round(price, 2)

class StockHistoryWorkshop(models.Model):
    reference = models.ForeignKey(Reference, on_delete = models.PROTECT)
    stock = models.ManyToManyField(StockWorkshop)
    last_update = models.DateField(auto_now_add=True)
    qty_per_train = models.IntegerField(default = 0)
    qty_car_single = models.ManyToManyField(Quantity, blank = True)
    

    def __str__(self):
        return str(self.reference) + ' - Last update: ' + str(self.last_update)   
    
    def get_absolute_url(self):
        return reverse('general:stock-workshop-detail', kwargs={'pk': self.pk})

    
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