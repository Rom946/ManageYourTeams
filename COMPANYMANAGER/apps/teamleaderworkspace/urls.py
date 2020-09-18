from django.urls import path, re_path
#from .views import ()
from . import views
from apps.teamleaderworkspace.models import Slash
from apps.teamleaderworkspace.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
   path('teamleaderhome/', views.homepage, name='teamleaderhome'),

   path('teamleaderhome/Timetable', views.Timetable, name='Timetable'),
  
   path('teamleaderhome/Mywork/', login_required(MyWorkViewClass.as_view()), name='Mywork'),


   path('Affectation/', login_required(AffectationViewClass.as_view()), name='Affectation'),
   
   path('References/', login_required(EmployeeReferencesViewClass.as_view()), name='EmployeeReferences'),
   
   path('Feedback/', login_required(FeedBackViewClass.as_view()), name='Feedback'),
   path('Delivery/', login_required(ReceiveDeliveryViewClass.as_view()), name='ReceiveDelivery'),
   path('Feedback/SubmitFeedback', views.SubmitFeedback, name = 'SubmitFeedback'),
  
   #Quality NCRs
    path('quality/', QualityListView.as_view(), name='quality'),
    path('quality/<int:pk>/', QualityDetailView.as_view(), name='quality-detail'),
    path('quality/new/', QualityCreateView.as_view(), name='quality-create'),
    path('quality/<int:pk>/update/', QualityUpdateView.as_view(), name='quality-update'),
    path('quality/<int:pk>/delete/', QualityDeleteView.as_view(), name='quality-delete'),

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