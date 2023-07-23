from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import StLoginForm
from django.contrib.auth.models import User
from docx import Document
from random import sample
from pathlib import Path
import json
from .models import StInfoModels

# Create your views here.
STUDENT_CHECKED = False

# handels all the processing
def WordFileHandler(FilePath,Quesno):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ANS_LIST = []
    PARSE_DICT ={}
    ActPath= f"{BASE_DIR}\media/{FilePath}"
    doc = Document(ActPath)
    paraObj = doc.paragraphs
    noPara = len(paraObj)
    actNoPara = (noPara//5)*5
    randomList = sample(range(0,actNoPara,5),Quesno)
    for num in randomList:
        paraText = paraObj[num].text
        optionRandomList=sample(range(1,5),4)
        OPTION_LIST = []
        for opNum in optionRandomList:
            optionObject = paraObj[num+opNum]
            if optionObject.runs[0].bold == True:
                ANS_LIST.append(len(OPTION_LIST))
            OPTION_LIST.append(optionObject.text)
        
        PARSE_DICT[paraText] = OPTION_LIST
    PARSE_DICT["Answers"] = ANS_LIST
    return PARSE_DICT


def StLogin(req):
    req.session['StName'] = req.POST.get('Name')
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
                return redirect(f"/{AdminCode}/")
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
        # first_name in database = Institute code
        userName= User.objects.filter(first_name=InstituteCode)[0]
        AdminInfo=userName.admininfo_set.all()[0] # type:ignore
        Main_Dict=WordFileHandler(AdminInfo.FILENAME,AdminInfo.FULLMARKS)
        context = {
            'fullMarks':AdminInfo.FULLMARKS,
            'passMarks':AdminInfo.PASSMARKS,
            'addtext':AdminInfo.ADDTEXT,
            'insName':AdminInfo.INSNAME,
            "MAIN_DICT":Main_Dict,
            "ANS":json.dumps(Main_Dict['Answers']),
            "counter":1,
        }
        STUDENT_CHECKED=False
        return render(req,"StPage/QuesPap.html",context=context)
    else:
        return redirect(StLogin)

from django.http import HttpResponse
def empty_favicon_view(request):
    return HttpResponse(status=204)

def Submition(req):
    Bin_data=req.GET.get('data')
    int_data=int(Bin_data,2)
    StName = req.session.get('StName')
    print(StName)
    StObj=StInfoModels.objects.filter(Name=StName,Touched_Status=False)[0]
    StObj.MarksAch=int_data
    StObj.save()
    return redirect("/")