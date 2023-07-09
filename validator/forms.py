from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # first_name = Institution Name
    first_name = forms.CharField(max_length=255,required=True,label="Institution Code:")
    class Meta():
        model = User 
        fields = ['username','first_name','password1','password2']