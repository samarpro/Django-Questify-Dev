from django.db import models
from validator.models import CustomUser
# Create your models here.
class StInfoModels(models.Model):
    Choice = [
        (1,"Science"),
        (2,"Management")
    ]
    # User->Admin_Name
    User = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Stream = models.IntegerField(choices=Choice)
    # Admin Institution code
    AdInsCode = models.CharField(max_length=10)
    # Marks Acheived
    MarksAch = models.IntegerField(null=True,default=0)
    Touched_Status = models.BooleanField(default=False)
    Grade = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.id} - {self.Name}" #type:ignore


