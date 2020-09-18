from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import *
from apps.general.models import *


from apps.workshopworkspace.models import StockHistoryWorkshop

        
#handle deletion for reference applied => remove from stock and remove wastes
@receiver(pre_delete) 
def update_stock_on_delete(sender, instance, *args, **kwargs):
    if sender == ReferenceApplied:
        if instance.had_stock_update:
            stock_history = StockHistory.objects.get(reference = instance.reference)
            stock = stock_history.stock.all().last()
            if instance.waste.all():
                waste_qty = 0
                wastes = instance.waste.all()
                for waste in wastes:
                    waste_qty += waste.qty
                    waste.delete()
            else:
                waste_qty = 0


            stock.qty = stock.qty + instance.qty + waste_qty
            stock.save()


    #reset stock and delete waste if NCR deleted
    if sender == Quality:
        if instance.had_stock_update:
            print('stock update and deleting waste')
            
            stock_history = StockHistory.objects.get(reference = instance.reference_to_replace)
            stock = stock_history.stock.all().last()
            
            stock.qty += 1

            stock.save()

            waste = instance.waste

            instance.waste = None
            instance.replacement = False
            instance.save()

            try:
                waste.delete()
            except Exception as e:
                print(e)

            
    


#update progresses if feedback saved/created
@receiver(post_save, sender=FeedBack) 
def create_post(sender, instance, created, **kwargs):
    
    title = 'Feedback - ' + str(instance.date_work)
    
    if created:
        print('creating a new post...')
        return Post.objects.create(author=instance.teamleader, date_posted = instance.date_work, content = instance.feedback, title = title) #create a new post for logged in user
    else:
        print('update feedback post')    
        post, c = Post.objects.get_or_create(author=instance.teamleader, date_posted = instance.date_work, title = title)
        post.content = instance.feedback
        post.save()
        return post

    workdone = WorkDone.objects.get(team_leader = instance.teamleader, date_work = instance.date_work)
    jobs = workdone.work.all()
    for job in jobs:
        progress_on_part = ProgressOnPart.objects.get(train = job.train, car = job.car, part = job.part)
        if progress_on_part.up_to_date == True:
            progress_on_part.up_to_date = False
            progress_on_part.save()

        progress_on_car = ProgressOnCar.objects.get(train = job.train, car = job.car)
        if progress_on_car.up_to_date == True:
            progress_on_car.up_to_date = False
            progress_on_car.save()

        progress_on_train = ProgressOnPart.objects.get(train = job.train)
        if progress_on_train.up_to_date == True:
            progress_on_train.up_to_date = False
            progress_on_train.save()
    


#handle stock history when user creates a new stock 
@receiver(post_save, sender=Stock)
def create_stock(sender, instance, created, **kwargs):

    if created:
        stock_history , create= StockHistory.objects.get_or_create(reference = instance.reference)
        stock_history.stock.add(instance)

        stock_history.last_update = datetime.today()
        stock_history.save()
    else:
        stock_history = StockHistory.objects.get(reference = instance.reference)
        if stock_history.qty_per_train == 0:
            print('fix qty per train')
            quantity, created_qty = Quantity.objects.get_or_create(reference = instance.reference)
            if not created_qty:
                stock_history.qty_car_single.add(quantity)
                stock_history.fix_qty_per_train()


#if a new quantity is saved for a reference, adds it to the stock history
@receiver(post_save, sender=Quantity)
def add_qty(sender, instance, created, **kwargs):

    stock_history, created_stock = StockHistory.objects.get_or_create(reference = instance.reference)
    workshop_stock_history, created_stock_workshop = StockHistoryWorkshop.objects.get_or_create(reference = instance.reference)
        
    if created_stock:
        stock_history.qty_car_single.add(instance)
    if created_stock_workshop:
        workshop_stock_history.qty_car_single.add(instance)
        
    stock_history.fix_qty_per_train()
    workshop_stock_history.fix_qty_per_train()



#update progress on part
@receiver(post_save, sender=ProgressOnPart)
def UpdateProgressOnPart(sender, instance, created, **kwargs):
    #populate jobs if created
    if created:
        jobs = Job.objects.filter(train = instance.train, car = instance.car, part = instance.part)
        for job in jobs:
            instance.jobs.add(job)
        progress = instance.set_progress_on_part()

        progress_on_car = ProgressOnCar.objects.get(train = instance.train, car = instance.car)
        progress_on_car.progress_on_part.add(instance)
    
        return progress

        
#update progress on car
@receiver(post_save, sender=ProgressOnCar)
def UpdateProgressOnCar(sender, instance, created, **kwargs):

    if created:
        progress_on_train = ProgressOnTrain.objects.get(train = instance.train)
        progress_on_train.progress_on_car.add(instance)
        
        jobs = Job.objects.filter(train = instance.train, car = instance.car)
        for job in jobs:
            instance.jobs.add(job)


        parts = instance.car.part.all()
        for part in parts:
            progress_on_part = ProgressOnPart.objects.create(train = instance.train, car = instance.car, part = part)
            instance.progress_on_part.add(progress_on_part)
            progress_on_train.progress_on_part.add(progress_on_part)
        

        progress_on_train.save()

        progress = instance.set_progress_on_car()
        return progress


#update progress on train        
@receiver(post_save, sender=ProgressOnTrain)
def UpdateProgressOnTrain(sender, instance, created, **kwargs):
    #populate jobs if created
    if created:
        jobs = Job.objects.filter(train = instance.train)
        for job in jobs:
            instance.jobs.add(job)

        cars = Car.objects.all()
        for car in cars:
            progress_on_car = ProgressOnCar.objects.create(train = instance.train, car = car)
            instance.progress_on_car.add(progress_on_car)
            
    
        progress = instance.set_progress_on_train()
        return progress
            

#a new train was created => add cars to it
@receiver(post_save, sender=Train)       
def create_train(sender, instance, created, **kwargs):
    #populate jobs if created
    if created:
        progress_on_train = ProgressOnTrain.objects.create(train = instance)
        cars = Car.objects.all()
        for car in cars:
            instance.cars.add(car)
        
        
#a new car was created => add parts to it
#add the new car to all the trains
@receiver(post_save, sender=Car)       
def create_car(sender, instance, created, **kwargs):

    #populate jobs if created
    if created:
        trains = Train.objects.all()
        for train in trains:
            train.cars.add(instance)
        
        parts = Part.objects.all()
        for part in parts:
            instance.part.add(part)

#a new part was created => add it to all cars
@receiver(post_save, sender=Part)       
def create_part(sender, instance, created, **kwargs):
    #populate jobs if created
    if created:
        cars = Car.objects.all()
        for car in cars:
            car.part.add(instance)


#a ncr was saved => update stock and wastes
@receiver(post_save, sender=Quality)       
def update_StocksAndWastes(sender, instance, created, **kwargs):
    #populate jobs if created
    
    if not instance.had_stock_update:
        if instance.replacement:
            print('Updating stocks and wastes...')

            #get reference applied object comporting the default
            try:
                reference_applied = ReferenceApplied.objects.get(job__train = instance.train, job__car = instance.car, job__part = instance.part, reference = instance.reference_to_replace, locations__id = instance.location.id)
            except Exception as error:
                print(error)
                try:
                    reference_applied = ReferenceApplied.objects.filter(job__train = instance.train, job__car = instance.car, job__part = instance.part, reference = instance.reference_to_replace, locations__id = instance.location.id).distinct()
                    reference_applied = ReferenceApplied.objects.get(id = reference_applied.id )
                except Exception as e:
                    print(e)
                    reference_applied = None

            print(reference_applied)
            
            if reference_applied is not None:
                waste, created_waste = Waste.objects.get_or_create(reference = instance.reference_to_replace, date_waste = datetime.today(), job_waste = reference_applied.job, location__id = instance.location.id)
            else:
                waste, created_waste = Waste.objects.get_or_create(reference = instance.reference_to_replace, date_waste = datetime.today(), job_waste = None, location__id = instance.location.id)

            #if the situation is not a NCR against Gibela => assign the tech who applied the reference as responsible
            if 'gibela' not in instance.situation.name.lower():
                if reference_applied is not None:   
                    tech = Tech.objects.get(id = reference_applied.tech.id)
                    instance.responsible = tech.profile
                    print('%s responsible' %tech.name)
                    tech_profile = tech.profile
                #reference applied not found
                else: 
                    tech = None
                    responsible = None
                    tech_profile = None
                
                #update waste
                waste.tech = tech
                waste.category = instance.default_type
                waste.ncr_responsible = tech_profile
            #assign Gibela as responsible
            else:
                print('Gibela responsible')
                user, created_user = User.objects.get_or_create(username='Gibela')
                user_profile = Profile.objects.get(user = user)
                instance.responsible = user_profile
                category, created_category = WasteCategory.objects.get_or_create(name = 'Gibela')
                
                waste.tech = None
                waste.category = category
                instance.default_type = category
                waste.ncr_responsible = user_profile
            

            if created_waste:
                waste.qty = 1
            else:
                waste.qty += 1

            waste.location.add(instance.location)
            
            waste.save()

            #handle stock update
            stock_history = StockHistory.objects.get(reference = instance.reference_to_replace)
            stock, created_stock = Stock.objects.get_or_create(reference = instance.reference_to_replace, date_record = datetime.today())
                

            if created_stock:
                if stock_history.stock.last():
                    stock.qty = stock_history.stock.last().qty - 1
                else: 
                    stock.qty = -1
            else:
                stock.qty -= 1
            
            stock.save()

            instance.had_stock_update = True
            instance.waste = waste
            instance.save()

