from django.urls import path

from .views import *
from config import settings

from rest_framework.routers import DefaultRouter, SimpleRouter

#Dev - show API 
if settings.DEBUG:
    router = DefaultRouter()
#Prod
else:
    router = SimpleRouter()

router.register('feedback', FeedbackViewSet, basename='Feedbacks')
router.register('stockhistorynigel', StockHistoryViewSet, basename='Stock Histories Nigel')
router.register('stocknigel', StockViewSet, basename='Stocks Nigel')
router.register('stockhistoryworkshop', StockHistoryWorkshopViewSet, basename='Stock Histories Workshop')
router.register('stockworkshop', StockWorkshopViewSet, basename='Stock Workshop')
router.register('stockfilm', StockFilmViewSet, basename='Stock Films')
router.register('stockfilmhistory', StockFilmHistoryViewSet, basename='Stock Films Histories')
router.register('workdone', WorkDoneViewSet, basename='Work Dones Nigel')
router.register('workshopjobs', WorkshopJobViewSet, basename='Workhop Jobs ')
router.register('progressontrain', ProgressOnTrainViewSet, basename='Progresses on trains ')
router.register('workbytech', WorkByTechViewSet, basename='Works done by Techs')
router.register('wastenigel', WasteViewSet, basename='Wasted references at Nigel')
router.register('wasteworkshop', WasteWorkshopViewSet, basename='Wasted references at workshop')
router.register('package', PackageViewSet, basename='Packages')
router.register('filmreel', FilmReelViewSet, basename='Film Reels')
router.register('referenceapplied', ReferenceAppliedViewSet, basename='References Applied at Nigel')
router.register('reference', ReferenceViewSet, basename='References')
router.register('profiles', ProfileViewSet, basename='Profile')

urlpatterns = router.urls