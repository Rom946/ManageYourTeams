from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import Profile

'''
User is sender
signal fired when something is saved
we want a profile created for each user
'''

@receiver(post_save, sender=User) #when a user is saved, send this signal to the receiver
def create_profile(sender, instance, created, **kwargs):

    if not created:
        return
    Profile.objects.create(user=instance) #create a new profile for logged in user


@receiver(post_save, sender=User) #when a user is saved, send this signal to the receiver
def save_profile(sender, instance, **kwargs):
    instance.profile.save() #save the new profile for the user currently logged in
    