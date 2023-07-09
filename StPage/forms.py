from django import forms
from .models import StInfoModels

class StLoginForm(forms.ModelForm):
# field will be generate according to the field in Models
    class Meta():
        model = StInfoModels
        fields = ['Name','Stream','AdInsCode']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'custom-class'},),
            # Other field-specific configurations
        }
        labels ={
            'Name':'Examinee Name',
            'Stream':'Choose Your Stream',
            'AdInsCode':'Institution Code'
        }