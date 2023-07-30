from django.db import models
from validator.models import CustomUser

# Create your models here.


def default_images_dict():
    return {}

class AdminInfo(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    # defining all other necessary fields
    FOR_CLASS = models.IntegerField(default=0,null=False,)
    INSNAME = models.CharField(max_length=250) # not ins code
    FULLMARKS = models.IntegerField()
    PASSMARKS = models.IntegerField()
    FILENAME = models.FileField(upload_to="WordFiles",max_length=250,null=True,default=None)
    ADDTEXT = models.CharField(max_length=500)
    IMAGES_DICT = models.JSONField(default=default_images_dict) # type: ignore
    Start_time = models.DateTimeField(blank=True,null=True)
    End_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.INSNAME} -- {self.user}"