from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StInfoModels(models.Model):
    Choice = [
        (1,"Science"),
        (2,"Management")
    ]
    # Admin Institution code
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Stream = models.IntegerField(choices=Choice)
    AdInsCode = models.CharField(max_length=10)
    # Marks Acheived
    MarksAch = models.IntegerField(null=True,default=0)



