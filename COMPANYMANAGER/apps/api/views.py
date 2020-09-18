from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter



from django.contrib.auth.models import User, Group
from apps.teamleaderworkspace.models import *
from apps.workshopworkspace.models import *
from apps.general.models import Post
from apps.users.models import Profile

from .serializers import *



class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.

    Source: https://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
    Modified to not error out on non-existing fields
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        print(self.kwargs)
        for field in self.lookup_fields:
            if self.kwargs.get(field):  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


#CUSTOM FILTERS
class WasteNigelFilter(FilterSet):
    #filter by reference id
    reference_id = NumberFilter(name='reference__id', lookup_expr= 'exact')
    #filter by train id
    job_waste_id__train_id = NumberFilter(name='job_waste__train__id', lookup_expr= 'exact')

    class Meta:
        model = Waste
        fields = {
            'reference_id',
            'job_waste_id__train_id'
        }

class WasteWorkshopFilter(FilterSet):
    #filter by reference id
    reference_id = NumberFilter(name='reference__id')
    #filter by category id
    category_id = NumberFilter(name='category__id')

    class Meta:
        model = WasteWorkshop
        fields = {
            'reference_id',
            'category_id'
        }




#VIEWSETS API
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedbackSerializer

class StockHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockHistory.objects.all()
    serializer_class = StockHistorySerializer
    


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]


    search_fields = ['=reference__id']

    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('id')


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

class StockHistoryWorkshopViewSet(viewsets.ModelViewSet):
    queryset = StockHistoryWorkshop.objects.all()
    serializer_class = StockHistoryWorkshopSerializer

class StockWorkshopViewSet(viewsets.ModelViewSet):
    queryset = StockWorkshop.objects.all()
    serializer_class = StockWorkshopSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['=reference__id']

    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('id')

class StockFilmHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockFilmHistory.objects.all()
    serializer_class = StockFilmHistorySerializer

class StockFilmViewSet(viewsets.ModelViewSet):
    queryset = StockFilm.objects.all()
    serializer_class = StockFilmSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['=film__id']

    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('id')

class WorkshopJobViewSet(viewsets.ModelViewSet):
    queryset = WorkshopJob.objects.all()
    serializer_class = WorkshopJobSerializer

class WorkDoneViewSet(viewsets.ModelViewSet):
    queryset = WorkDone.objects.all()
    serializer_class = WorkDoneSerializer

class ProgressOnTrainViewSet(viewsets.ModelViewSet):
    queryset = ProgressOnTrain.objects.all()
    serializer_class = ProgressOnTrainSerializer

class WorkByTechViewSet(viewsets.ModelViewSet):
    queryset = WorkByTech.objects.all()
    serializer_class = WorkByTechSerializer

class WasteViewSet(viewsets.ModelViewSet):
    queryset = Waste.objects.all()
    serializer_class = WasteSerializer
    
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['=reference__id']
    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('id')

class WasteWorkshopViewSet(viewsets.ModelViewSet):
    queryset = WasteWorkshop.objects.all()
    serializer_class = WasteWorkshopSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['=reference__id']

    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('id')

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class FilmReelViewSet(viewsets.ModelViewSet):
    queryset = FilmReel.objects.all()
    serializer_class = FilmReelSerializer

class ReferenceAppliedViewSet(viewsets.ModelViewSet):
    queryset = ReferenceApplied.objects.all()
    serializer_class = ReferenceAppliedSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    
