from django.urls import path, re_path
from django.conf.urls import url
from . import views
from apps.teamleaderworkspace.models import Slash
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
   
   path('Dashboard/', login_required(DashboardViewClass.as_view()), name='dashboard'),
   path('Charts/', login_required(ChartViewClass.as_view()), name='charts'),
   path('Highlights/', login_required(HighlightsClassView.as_view()), name='highlights'),
   url(r'^api/v1/chart/data/$', login_required(ChartData.as_view())),
]

