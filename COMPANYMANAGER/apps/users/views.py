from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserProfileForm
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def register(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            profile_form = UserProfileForm(request.POST)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                profile = profile_form.save(commit=False)
                profile.user = user 
                profile.user

                profile.save()

                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('general:home')
        else:
            form = UserRegisterForm()
            profile_form = UserProfileForm()

        context = {
            'form' : form,
            'profile_form' : profile_form
        }
        return render(request, 'users/register.html', context)
    
    else:
        return redirect('general:home')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'{request.user.username}, your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)






#types of message
#messages.debug
#messages.info
#messages.success
#messages.warning
#messages.error