from django import forms
from .models import AdminInfo


# {{forms.name|add_label_class}}
# {{render_field form.images}}
class AdminInfoForms(forms.Form):
    INSNAME = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Institute Name")
    FULLMARKS = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PASSMARKS = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control'}))
    FILENAME = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Word File ")
    ADDTEXT =forms.CharField(max_length=500,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    label="Additional Text")

    class Meta():
        model = AdminInfo
        fields =["INSNAME","FULLMARKS","PASSMARKS","FILENAME","ADDTEXT"]