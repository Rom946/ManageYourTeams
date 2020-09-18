from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import *
from apps.teamleaderworkspace.models import StockHistory

import datetime

    




@receiver(post_save, sender=StockWorkshop) #when a user is saved, send this signal to the receiver
def add_to_workshop_stock_history(sender, instance, created, **kwargs):

    if created:
        stock_history, create = StockHistoryWorkshop.objects.get_or_create(reference = instance.reference)
        stock_history.stock.add(instance)
        stock_history.last_update = datetime.date.today()
        stock_history.save()
    else:
        stock_history = StockHistoryWorkshop.objects.get(reference = instance.reference)
        if stock_history.qty_per_train == 0:
            print('fix qty per train')
            quantity, created_qty = Quantity.objects.get_or_create(reference = instance.reference)
            if not created_qty:
                stock_history.qty_car_single.add(quantity)
                stock_history.fix_qty_per_train()


@receiver(post_save, sender=StockFilm) #when a user is saved, send this signal to the receiver
def add_to_stock_history(sender, instance, created, **kwargs):

    if created:
        stock_history , create= StockFilmHistory.objects.get_or_create(film = instance.film)
        stock_history.stock.add(instance)
        stock_history.last_update = datetime.date.today()
        stock_history.save()
    


@receiver(post_save, sender=FilmReel) #when a user is saved, send this signal to the receiver
def add_to_stock(sender, instance, created, **kwargs):
    print('add to stock function')
    if created:
        print('Adding to stock..')
        stock_film_history, stock_history_created = StockFilmHistory.objects.get_or_create(film = instance.film)
        if not stock_history_created:
            try:
                last_stock_qty = stock_film_history.stock.last().qty
            except Exception as e:
                print(e)
                last_stock_qty = 0
        stock_film, created_stock = StockFilm.objects.get_or_create(film = instance.film, date_record = datetime.date.today())
        #get film stock history
        print(stock_film)
        if created_stock:
            if stock_history_created:  
                stock_film.qty = 1
                stock_film_history.stock.add(stock_film)
            else:
                print('updating stock qty from last stock qty')
                stock_film.qty = last_stock_qty + 1
        else: 
            stock_film.qty += 1
         
        stock_film.save()
        print(stock_film.qty)
    else:
        if instance.finished == True:
            film = instance.film
            stock_film_history, stock_history_created = StockFilmHistory.objects.get_or_create(film = instance.film)
            if not stock_history_created:
                try:
                    last_stock_qty = stock_film_history.stock.last().qty
                except Exception as e:
                    print(e)
                    last_stock_qty = 0
            stock_film, stock_created = StockFilm.objects.get_or_create(film = film, date_record = datetime.date.today())
            print('Update film stock for %s' %str(stock_film))
            film_qty_used = 1

            if stock_created:
                print('new stock object created')
                #created a stock history object
                if stock_history_created:
                    print('creating a new stock history object')
                    stock_film.qty = - film_qty_used
                    stock_film.save()
                    stock_film_history.stock.add(stock_film)
                
                #get last stock qty and update  
                else:
                    print('updating stock qty from last stock qty')
                    stock_film.qty = last_stock_qty - film_qty_used
                    stock_film.save()
                    stock_film_history.stock.add(stock_film)
            
            #update stock
            else:
                print('updating stock from actual stock')
                stock_film.qty = stock_film.qty - film_qty_used
                stock_film.save()



@receiver(pre_delete) #when a user is saved, send this signal to the receiver
def Cancel_from_stock(sender, instance, *args, **kwargs):
    if sender == FilmReel:
        print('Removing from stock..')
        stock_film, created_stock = StockFilm.objects.get_or_create(film = instance.film, date_record = datetime.date.today())
        if created_stock:
            stock_history, created_stock_history = StockFilmHistory.objects.get_or_create(film = instance.film)
            last_qty = stock_history.stock.last().qty
            stock_film.qty = last_qty - 1
            stock_history.stock.remove(stock_film)
        else: 
            stock_film.qty = stock_film.qty - 1
            
        stock_film.save()
    
    
    elif sender == Package:
        if instance.had_stock_update == True:
            print('Removing %s from stock' %instance)
            if instance.available_at_office == True:
                stock_history, created_stock_history = StockHistoryWorkshop.objects.get_or_create(reference = instance.reference)
            else:
                stock_history, created_stock_history = StockHistory.objects.get_or_create(reference = instance.reference)
            
            stock = stock_history.stock.all().last()
            wastes = instance.waste.all()
            for waste in wastes:
                waste.delete()

            stock.qty = stock.qty - instance.qty
            stock.save()
    
    elif sender == StockWorkshop:
        instance.stockhistoryworkshop_set.clear()
        history = StockHistoryWorkshop.objects.get(reference = instance.reference)
        history.stock.remove(instance)
        for stock in history.stock.all():
            print(stock)

