from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    salary = models.IntegerField(default = 0)
    
    class Position(models.TextChoices):
        MANAGER = 'MA', _('Manager')
        TEAMLEADER = 'TL', _('Team leader')
        TECHNICIAN = 'TN', _('Technician')
        WORKSHOP = 'WS', _('Workshop')
        CLIENT = 'CL', _('Client')
    
    position = models.CharField(max_length=2, choices=Position.choices, default=Position.TECHNICIAN)

    def __str__(self):
        return f'{self.user.username}'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs) #run parent class
        #get image path
        img = Image.open(self.image.path)

        #resize profile picture
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def get_position(self):
        return str(self.position)

    def name(self):
        if self.user.first_name and self.user.last_name:
            return str(self.user.first_name) + ' ' +str(self.user.last_name)
        else:
            return str(self.user.username)



