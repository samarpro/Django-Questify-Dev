from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User 
from .forms import AdminInfoForms
from .models import AdminInfo
from pathlib import Path
from StPage.models import StInfoModels
# Create your views here.
def dashboard(req):
    user=req.user
    List_St = StInfoModels.objects.filter(User=user)
    AdminUser = AdminInfo.objects.get(user=user)
    context={
        "ListSt":List_St,
        "PMarks": AdminUser.PASSMARKS,
        }
    return render(req,"TeacherAdmin/dashboard.html",context)

def uploadInfo(req):
    err=msg=""
    BASE_DIR = Path(__file__).resolve().parent.parent
    error_message = ""
    if req.method=="POST":
        form =  AdminInfoForms(req.POST,req.FILES)
        if form.is_valid():
            username = req.user
            InsName=form.cleaned_data['INSNAME']
            fmarks= form.cleaned_data['FULLMARKS']
            pmarks= form.cleaned_data['PASSMARKS']
            file=form.cleaned_data['FILENAME']
            addtext= form.cleaned_data['ADDTEXT']
            # ActUser = User.objects.get(username=username)
            Obj = AdminInfo(user=username,INSNAME=InsName,FULLMARKS=fmarks,PASSMARKS=pmarks,FILENAME=file,ADDTEXT=addtext)
            Obj.save()
            msg = "Online Exam Successfully Created."
            err= False
            # wordFile = Document(BASE_DIR / f"media\WordFiles\{file.name}") #type:ignore
            # return HttpResponse(len(wordFile.paragraphs))
        else:
            err = "Form Invalid. Please try again."
    else:
        form = AdminInfoForms()
    context = {
        'form':form,
        'err':err,
        'msg':msg
        }
    return render(req,"TeacherAdmin/upload.html",context) 