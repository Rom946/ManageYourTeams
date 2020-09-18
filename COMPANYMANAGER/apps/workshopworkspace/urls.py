from django.urls import path, re_path
from . import views
from apps.teamleaderworkspace.models import Slash
from apps.workshopworkspace.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
   path('workshophome/', views.homepage, name='workshophome'),
  
   path('Mywork/', login_required(MyWorkViewClass.as_view()), name='Mywork'),
   path('Feedback/', login_required(FeedbackWorkshopViewClass.as_view()), name='Feedback'),
   path('Feedback/SubmitFeedback', views.SubmitFeedback, name = 'SubmitFeedback')

]


'''
   path('mywork/', views.mywork, name='mywork'),
   path('mywork/addtech', views.addtech, name='addtech'),
   path('mywork/AddNewEmployee',views.AddNewEmployee, name='AddNewEmployee'),
   path('mywork/RemoveTech', views.RemoveTech, name='RemoveTech'),
   path('mywork/AddPart', views.AddPart, name='AddPart'),
   path('mywork/RemovePart', views.RemovePart, name='RemovePart'),
   path('mywork/SelectedTrain', views.SelectedTrain, name='SelectedTrain'),
   path('mywork/SelectedCar', views.SelectedCar, name='SelectedCar'),
'''