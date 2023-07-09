from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import StLoginForm
from django.contrib.auth.models import User
# from validator.models import 
# Create your views here.

STUDENT_CHECKED = False
def StLogin(req):
    err=""
    if req.method =="POST":
        form = StLoginForm(req.POST)
        if form.is_valid():
            # Getting Code Name
            AdminCode = form.cleaned_data['AdInsCode'] 
            # filtered User -> Teacher Admin User Exixts
            FiltUser = User.objects.filter(first_name=AdminCode)
            # Checks wheather or not institute code exist
            if FiltUser.exists():
                FormInst=form.save(commit=False)
                FormInst.User_id= FiltUser[0].id #type:ignore
                form.save()
                global STUDENT_CHECKED;
                STUDENT_CHECKED=True
                return redirect(f"/{AdminCode}")
            else:
                err="Institute Code not found."
    form = StLoginForm()
    context={
        'form':form,
        'err':err
    }
    return render(req,"StPage/index.html",context)

# Institute code is for sure valid because of FiltUser.exists()
def QuesHandler(req,InstituteCode):
    global STUDENT_CHECKED;
    if STUDENT_CHECKED == True:
        
        # STUDENT_CHECKED=False
        context = {

        }
        return render(req,"StPage/QuesPap.html",context)
    else:
        return redirect(StLogin)