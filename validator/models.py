from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
def default_portals_dict():
    return {}
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, unique=True,error_messages={
            'blank': 'This field cannot be blank. Please provide Institution code.',
            'invalid': 'Please enter a valid value for this field.',
            'unique': 'Provided code is already in use. Try new one',})
    active_portals = models.JSONField(default=default_portals_dict,null=True)

    def __str__(self):
        return self.username
