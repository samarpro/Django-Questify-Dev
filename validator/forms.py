from django.contrib.auth.forms import UserCreationForm
from django import forms
from validator.models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    # first_name = Institution Name
    first_name = forms.CharField(max_length=255,required=True,label="Institution Code:")
    class Meta():
        model = CustomUser 
        fields = ['username','first_name','password1','password2']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        # Regular expression to check for special characters
        if re.search(r'[+=_-`~;\/!@#$%^&*(),. ?":{}|<>]', first_name):
            raise forms.ValidationError("Institution Code should not contain special characters.") 
        return first_name