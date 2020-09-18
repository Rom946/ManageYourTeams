from django.db import models


import datetime


'''
Queries on WorkByTech model
'''
class TechQuerySet(models.QuerySet):

    #get all the work done by date for all the techs
    def get_all_work_by_date(self, date):
        work = []
        query = self.filter(date_work=date)
        for obj in query:
            work.append(obj.work.all())
        return work


    #get all the work done by date by a specific tech
    def get_tech_work_by_date(self, tech_id, date):
        work = []
        query = self.filter(tech_id=tech_id, date_work=date)
        for obj in query:
            work.append(obj.work.all())
        return work


    #get data for today 
    def get_data_by_date(self, date):
        data = []
        query = self.filter(date_work=date)
        for obj in query:
            data.append(obj)
        return data

    #get data for a specific team leader
    def get_tech_data_by_date(self, tech_id, date):
        data = []
        query = self.filter(tech_id=tech_id, date_work=date)
        for obj in query:
            data.append(obj)
        return data

     


#handle queries related to tech work (WorkByTech model)
class TechWorkHistoryManager(models.Manager):
    date_today = datetime.date.today()

    def get_queryset(self):
        return TechQuerySet(self.model, using=self._db)

    #get an employee work by date
    def tech_work_by_date(self, tech_id, date):
        return self.get_queryset().get_tech_work_by_date(tech_id, date)

    #get an employee work done today
    def tech_work_today(self, tech_id):
        return self.tech_work_by_date(tech_id, self.date_today)


    #get all the work done by date
    def work_by_date(self, date):
        return self.get_queryset().get_all_work_by_date(date)
    
    #get all the work done today
    def work_today(self):
        return self.work_by_date(self.date_today)


    #get all data by date
    def data_by_date(self, date):
        return self.get_queryset().get_data_by_date(date)

    #get all data for today
    def today(self):
        return self.data_by_date(self.date_today)


    #get data for a specific tech by date
    def data_by_tech(self, tech_id, date):
        return self.get_queryset().get_tech_data_by_date(tech_id, date)

    #get data for a specific tech for today
    def today_by_tech(self, tech_id):
        return self.data_by_tech(tech_id, self.date_today)




'''
Queries on WorkDone model
'''
class TeamLeaderQuerySet(models.QuerySet):
    
    #get all work done by a specific team leader by date
    def get_teamleader_work_by_date(self, team_leader_id, date):
        work = []
        query = self.filter(team_leader_id=team_leader_id, date_work=date)
        for obj in query:
            work.append(obj.work.all())
        return work


    #get all work done by date 
    def get_all_work_by_date(self, date):
        work = []
        query = self.filter(date_work=date)
        for obj in query:
            work.append(obj.work.all())
        return work


    #get data by date 
    def get_data_by_date(self, date):
        data = []
        query = self.filter(date_work=date)
        for obj in query:
            data.append(obj)
        return data

    #get data for a specific team leader
    def get_teamleader_data_by_date(self, team_leader_id, date):
        data = []
        query = self.filter(team_leader_id=team_leader_id, date_work=date)
        for obj in query:
            data.append(obj)
        return data

    def get_references_applied_by_teamleader_by_date(self, team_leader_id, date):
        query = self.get(team_leader_id=team_leader_id, date_work=date)
        print(query)
        return query.references_applied.all()




#handle queries related to team leaders work (WorkDone model)
class TeamLeaderWorkHistoryManager(models.Manager):

    date_today = datetime.date.today()
    
    def get_queryset(self):
        return TeamLeaderQuerySet(self.model, using=self._db)

    #get a team leader work by date
    def teamleader_work_by_date(self, team_leader_id, date):
        return self.get_queryset().get_teamleader_work_by_date(team_leader_id, date)

    #get a team leader work done today
    def teamleader_work_today(self, team_leader_id):
        return self.teamleader_work_by_date(team_leader_id, self.date_today)
    

    #get all the work done by date
    def work_by_date(self, date):
        return self.get_queryset().get_all_work_by_date(date)

    #get all the work done today
    def work_today(self):
        return self.work_by_date(self.date_today)

    #get all data by date
    def data_by_date(self, date):
        return self.get_queryset().get_data_by_date(date)

    #get all data for today
    def today(self):
        return self.data_by_date(self.date_today)

    #get data for a specific team leader by date
    def data_by_teamleader(self, team_leader_id, date):
        return self.get_queryset().get_teamleader_data_by_date(team_leader_id, date)

    #get data for a specific team leader for today
    def today_by_teamleader(self, team_leader_id):
        return self.data_by_teamleader(team_leader_id, self.date_today)

    
    def all_references_applied_by_teamleader_today(self, team_leader_id):
        return self.get_queryset().get_references_applied_by_teamleader_by_date(team_leader_id, datetime.date.today())




class ProgressPartQuerySet(models.QuerySet):
    
    #get all work done by a specific team leader by date
    def update_progress(self, jobs):
       
       #get progress part
        for job in jobs:
            progress_part = self.get(train = job.train, car = job.car, part = job.part)
            if not progress_part.up_to_date:
                progress_part.update_progress()


        return progress_part
 
   
class ProgressPartManager(models.Manager):

    date_today = datetime.date.today()
    
    def get_queryset(self):
        return ProgressPartQuerySet(self.model, using=self._db)

    #get a team leader work by date
    def update_progress(self, jobs):
        return self.get_queryset().update_progress(jobs)


class ProgressCarQuerySet(models.QuerySet):
    
    #get all work done by a specific team leader by date
    def update_progress(self, jobs):
       
       #get progress part
        for job in jobs:
            progress_car = self.get(train = job.train, car = job.car)
            if not progress_car.up_to_date:
                progress_car.update_progress()

        return progress_car
 
   
class ProgressCarManager(models.Manager):

    date_today = datetime.date.today()
    
    def get_queryset(self):
        return ProgressCarQuerySet(self.model, using=self._db)

    #get a team leader work by date
    def update_progress(self, jobs):
        return self.get_queryset().update_progress(jobs)


class ProgressTrainQuerySet(models.QuerySet):
    
    #get all work done by a specific team leader by date
    def update_progress(self, jobs):
       
        for job in jobs:
            progress_train = self.get(train = job.train)
            if not progress_train.up_to_date:
                progress_train.update_progress()

        return progress_train
 
   
class ProgressTrainManager(models.Manager):

    date_today = datetime.date.today()
    
    def get_queryset(self):
        return ProgressTrainQuerySet(self.model, using=self._db)

    #get a team leader work by date
    def update_progress(self, jobs):
        return self.get_queryset().update_progress(jobs)