from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login

# Create your views here.
def SignUp(req):
    if req.method=='POST':
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req,user)
            return redirect('../../')
    else:
        form = CustomUserCreationForm()
    context={'SigninForm':form}
    return render(req,'registration/signup.html',context)