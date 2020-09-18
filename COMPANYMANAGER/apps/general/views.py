from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from .models import Post
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.teamleaderworkspace.models import *
from apps.workshopworkspace.models import *

from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView, 
    UpdateView
)



#post view (home)
def home(request):
    print('Home')
    profile = Profile.objects.get(user = request.user)
    print(profile.get_position())
    context = {
        'profile' : profile,
        'posts': Post.objects.all()
    }
    return render(request, 'general/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'general/index.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4
    
class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        #set current logged in user as author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        #set current logged in user as author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #make sure the current user can edit the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    #make sure the current user can edit the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
class UserPostListView(ListView):
    model = Post
    template_name = 'general/user_posts.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



#inventory

def inventory(request):

    context = {
        'title' : 'Inventory',
    }

    return render(request, 'general/inventory.html', context)

#inventory stock nigel
class StockNigelListView(ListView):
    model = StockHistory
    template_name = 'general/inventory/stocknigel.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'stockhistorynigel'
    ordering = ['-last_update']
    paginate_by = 20
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_queryset(self):
        
        qs = super().get_queryset()

        try:
            qs = qs.filter(id=self.kwargs['id'], stock__isnull = False)
        except KeyError as e:
            print(e)
            # will land here if 'id' is not present, so we return all
            # instances and do not filter anything
            pass

        return qs
        
class StockNigelDetailView(DetailView):
    model = Stock
    
class StockNigelCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    fields = ['qty']
    
class StockNigelUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock    
    fields = ['qty']

class StockNigelDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    success_url = '/inventory/stocknigel/'


#inventory stock workshop
class StockWorkshopListView(ListView):
    model = StockHistoryWorkshop
    template_name = 'general/inventory/stockworkshop.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'stockhistoryworkshop'
    ordering = ['-last_update']
    paginate_by = 20

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_queryset(self):
        
        qs = super().get_queryset()

        try:
            qs = qs.filter(id=self.kwargs['id'])
        except KeyError as e:
            print(e)
            # will land here if 'id' is not present, so we return all
            # instances and do not filter anything
            pass

        return qs

class StockWorkshopDetailView(DetailView):
    model = StockWorkshop
    
class StockWorkshopCreateView(LoginRequiredMixin, CreateView):
    model = StockWorkshop
    fields = ['qty']

class StockWorkshopUpdateView(LoginRequiredMixin, UpdateView):
    model = StockWorkshop
    fields = ['qty']
    
class StockWorkshopDeleteView(LoginRequiredMixin, DeleteView):
    model = StockWorkshop
    success_url = '/inventory/stockworkshop/'


#inventory stock film
class StockFilmListView(LoginRequiredMixin, ListView):
    model = StockFilmHistory
    template_name = 'general/inventory/stockfilm.html'#looking for template naming convention : <app>/<model>_<viewtype>.html
    context_object_name = 'stockhistoryfilm'
    ordering = ['-last_update']
    paginate_by = 20
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_queryset(self):
        
        qs = super().get_queryset()

        try:
            qs = qs.filter(id=self.kwargs['id'])
        except KeyError as e:
            print(e)
            # will land here if 'id' is not present, so we return all
            # instances and do not filter anything
            pass

        return qs
   
class StockFilmDetailView(LoginRequiredMixin, DetailView):
    model = StockFilm
    
class StockFilmCreateView(LoginRequiredMixin, CreateView):
    model = StockFilm
    fields = ['qty']

class StockFilmUpdateView(LoginRequiredMixin, UpdateView):
    model = StockFilm
    fields = ['qty']

class StockFilmDeleteView(LoginRequiredMixin, DeleteView):
    model = StockFilm
    success_url = '/inventory/stockfilm/'

