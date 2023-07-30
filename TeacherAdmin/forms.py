from django import forms


# {{forms.name|add_label_class}}
# {{render_field form.images}}
class AdminInfoForms(forms.Form):
    INSNAME = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Institute Name")
    FOR_CLASS = forms.IntegerField(label="For Grade",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    FULLMARKS = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control'}))
    PASSMARKS = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control'}))
    FILENAME = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Word File ")
    ADDTEXT =forms.CharField(max_length=500,
    widget=forms.TextInput(attrs={'class': 'form-control'}),
    label="Additional Text")
    Start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control','type':"datetime-local"}) )
    End_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control','type':"datetime-local"}),)