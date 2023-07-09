from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AdminInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # defining all other necessary fields
    INSNAME = models.CharField(max_length=250)
    FULLMARKS = models.IntegerField()
    PASSMARKS = models.IntegerField()
    FILENAME = models.FileField(upload_to="WordFiles",max_length=250,null=True,default=None)
    ADDTEXT = models.CharField(max_length=500)