from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import StLoginForm
from validator.models import CustomUser
from docx import Document
from random import sample
from pathlib import Path
import json
from .models import StInfoModels

# Create your views here.
# handels all the processing
def WordFileHandler(FilePath,Quesno,Image_Dict):
    BASE_DIR = Path(__file__).resolve().parent.parent
    ANS_LIST = []
    PARSE_DICT ={}
    ActPath= f"{BASE_DIR}/media/{FilePath}"
    doc = Document(ActPath)
    paraObj = doc.paragraphs
    # Final Dict which contains images of the question present in PARSE_DICT
    # Image list shortlist
    IMAGE_DICT_SRTLIST = {}
    noPara = len(paraObj)
    actNoPara = (noPara//5)*5
    # random list of question no
    randomList = sample(range(0,actNoPara,5),Quesno)
    for index,num in enumerate(randomList):
        paraText = paraObj[num].text
        # random list for option no
        optionRandomList=sample(range(1,5),4)
        OPTION_LIST = []
        # checking wheather or not the para num is in IMAGE_DICT
        num_String = str(num) 
        if  num_String in Image_Dict:
            """if para num -> num exists in IMAGE_DICT Add that in a dict which is inside a dict"""
            IMAGE_DICT_SRTLIST[index+1]={"Question":Image_Dict[num_String],"Option":dict({})}
        # used ot make sure that if any question's option are not bold then error doesn't occur
        Default_append=True
        for opNum in optionRandomList:
            OptionParaNum = num+opNum
            OptionParaNum_string = str(OptionParaNum)
            # if image is in Image dictioanry and para num is also created
            # This means both question and answers require images
            if OptionParaNum_string in Image_Dict and  index+1 in IMAGE_DICT_SRTLIST:
                print(Image_Dict)
                print(f"opNum:{opNum}.... optionParaNum:{OptionParaNum_string}...num:{num}")
                IMAGE_DICT_SRTLIST[index+1]["Option"][opNum] = Image_Dict[OptionParaNum_string]
            # This condition means question doesn't require  images but options does
            elif index+1 not in IMAGE_DICT_SRTLIST and OptionParaNum_string in Image_Dict:
                # the opNum also indicates the index of the option . 
                # In dictionary , images are stored in the basis of the index number
                # like 0-> image1.png
                # 1->image2.png
                # so we require its index number.
                IMAGE_DICT_SRTLIST[index+1] = {"Question":None,"Option":{opNum:Image_Dict[OptionParaNum_string]}}
                # If Option is empty then it means no option require Images.

            optionObject = paraObj[OptionParaNum] 
            if optionObject.runs[0].bold == True:
                Default_append=False
                # The answer index is based in lenght of the OPTION_LIST1
                ANS_LIST.append(len(OPTION_LIST))
            OPTION_LIST.append(optionObject.text)
            # condition for making default index 0 
        if Default_append:
            ANS_LIST.append(0)

        # Updating Main Dict -> Question, Option and 
        PARSE_DICT[paraText] = OPTION_LIST
    PARSE_DICT["Answers"] = ANS_LIST
    return PARSE_DICT,IMAGE_DICT_SRTLIST


def StLogin(req):
    req.session['StName'] = req.POST.get('Name')
    err=""
    if req.method =="POST":
        form = StLoginForm(req.POST)
        if form.is_valid():
            # Getting Code Name
            AdminCode = form.cleaned_data['AdInsCode'] 
            # filtered User -> Teacher Admin User Exixts
            FiltUser = CustomUser.objects.filter(first_name=AdminCode)
            # Checks wheather or not institute code exist
            if FiltUser.exists():
                FormInst=form.save(commit=False)
                FormInst.User_id= FiltUser.last().id #type:ignore
                form.save()
                req.session['STUDENT_CHECKED'] = True
                req.session.save()
                return redirect(f"/{AdminCode}/")
            else:
                err="Institute Code not found."
    form = StLoginForm()
    context={
        'form':form,
        'err':err
    }
    return render(req,"Stpage/index.html",context)

# Institute code is for sure valid because of FiltUser.exists()
def QuesHandler(req,InstituteCode):
    # STUDENT_CHECKED ensures that one student cannot give exam twice by 
    # if req.session.get('STUDENT_CHECKED',False) == True:
    if True:
        SessStName = req.session.get('StName')
        # first_name in database = Institute code
        userName= CustomUser.objects.filter(first_name=InstituteCode)[0]
        AdminInfo=userName.admininfo_set.last()  # type:ignore
        if AdminInfo is not None: 
            Main_Dict,Images_Dict=WordFileHandler(AdminInfo.FILENAME,AdminInfo.FULLMARKS,AdminInfo.IMAGES_DICT)
            student_object = StInfoModels.objects.filter(Name=SessStName).last() 
            if student_object is not None:
                student_id = student_object.id #type:ignore
                context = {
                    'fullMarks':AdminInfo.FULLMARKS,
                    'passMarks':AdminInfo.PASSMARKS,
                    'addtext':AdminInfo.ADDTEXT,
                    'insName':AdminInfo.INSNAME,
                    "MAIN_DICT":Main_Dict,
                    "ANS":json.dumps(Main_Dict['Answers']),
                    "counter":1,
                    "Student_Name":SessStName, # !#%--!#% these are yet to be display in front end
                    "Student_id": student_id,  # !#%--!#% these are yet to be display in front end,
                    "Image_Dict": Images_Dict ,
                }
                req.session['STUDENT_CHECKED']=False
                req.session.save()
                return render(req,"StPage/QuesPap.html",context=context)
            else:
                return render(req,"StPage/error.html") # contrext is required to pass
        else:
            return render(req,"StPage/error.html")
    else:
        return redirect(StLogin)

from django.http import HttpResponse
# This block of code handles teh favicon error
# that occurs when django searche for favicon by default.
def empty_favicon_view(request):
    return HttpResponse(status=204)

def Submition(req):
    Bin_data=req.GET.get('data')
    int_data=int(Bin_data,2)
    StName = req.session.get('StName')
    StObj=StInfoModels.objects.filter(Name=StName,Touched_Status=False)[0]
    StObj.MarksAch=int_data
    StObj.save()
    return redirect("/")