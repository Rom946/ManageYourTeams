from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('inventory', views.inventory, name='inventory'),
    #inventory nigel
    path('inventory/stocknigel/', StockNigelListView.as_view(), name='stock-nigel'),
    path('inventory/stocknigel/<int:pk>/', StockNigelDetailView.as_view(), name='stock-nigel-detail'),
    path('inventory/stocknigel/new/', StockNigelCreateView.as_view(), name='stock-nigel-create'),
    path('inventory/stocknigel/<int:pk>/update/', StockNigelUpdateView.as_view(), name='stock-nigel-update'),
    path('inventory/stocknigel/<int:pk>/delete/', StockNigelDeleteView.as_view(), name='stock-nigel-delete'),
    #inventory workshop
    path('inventory/stockworkshop/', StockWorkshopListView.as_view(), name='stock-workshop'),
    path('inventory/stockworkshop/<int:pk>/', StockWorkshopDetailView.as_view(), name='stock-workshop-detail'),
    path('inventory/stockworkshop/new/', StockWorkshopCreateView.as_view(), name='stock-workshop-create'),
    path('inventory/stockworkshop/<int:pk>/update/', StockWorkshopUpdateView.as_view(), name='stock-workshop-update'),
    path('inventory/stockworkshop/<int:pk>/delete/', StockWorkshopDeleteView.as_view(), name='stock-workshop-delete'),
    #inventory film
    path('inventory/stockfilm/', StockFilmListView.as_view(), name='stock-film'),
    path('inventory/stockfilm/<int:pk>/', StockFilmDetailView.as_view(), name='stock-film-detail'),
    path('inventory/stockfilm/new/', StockFilmCreateView.as_view(), name='stock-film-create'),
    path('inventory/stockfilm/<int:pk>/update/', StockFilmUpdateView.as_view(), name='stock-film-update'),
    path('inventory/stockfilm/<int:pk>/delete/', StockFilmDeleteView.as_view(), name='stock-film-delete'),

]
