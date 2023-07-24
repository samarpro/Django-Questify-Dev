from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50, unique=True,error_messages={
            'blank': 'This field cannot be blank. Please provide Institution code.',
            'invalid': 'Please enter a valid value for this field.',
            'unique': 'Provided code is already in use. Try new one',})


    def __str__(self):
        return self.username
