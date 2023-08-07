from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import StLoginForm
from validator.models import CustomUser
from docx import Document
from random import sample
from pathlib import Path
import json
from django.conf import settings
from .models import StInfoModels
from datetime import datetime
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
    if Quesno<=actNoPara//5:

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
                IMAGE_DICT_SRTLIST[index+1]={"Question":Image_Dict[num_String],"Option":[]}
            # used ot make sure that if any question's option are not bold then error doesn't occur
            Default_append=True
            for opNum in optionRandomList:
                OptionParaNum = num+opNum
                OptionParaNum_string = str(OptionParaNum)
                # if image is in Image dictioanry and para num is also created
                # This means both question and answers require images
                if OptionParaNum_string in Image_Dict and  index+1 in IMAGE_DICT_SRTLIST:
                    IMAGE_DICT_SRTLIST[index+1]["Option"].append(Image_Dict[OptionParaNum_string])
                # This condition means question doesn't require  images but options does
                elif index+1 not in IMAGE_DICT_SRTLIST and OptionParaNum_string in Image_Dict:
                    # the opNum also indicates the index of the option . 
                    # In dictionary , images are stored in the basis of the index number
                    # like 0-> image1.png
                    # 1->image2.png
                    # so we require its index number.
                    IMAGE_DICT_SRTLIST[index+1] = {"Question":None,"Option":[Image_Dict[OptionParaNum_string]]}
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
    else:
        return None,None


def StLogin(req):
    err=""
    if req.method =="POST":
        req.session['StName'] = req.POST.get('Name')
        Grade = req.POST.get('Grade')
        req.session["Grade"]= Grade
        InstituteCode = req.POST.get('AdInsCode')
        userName= CustomUser.objects.filter(first_name=InstituteCode).last() # this last doesn't make sense cuz first_name is also unique
        if userName is None:
            context={'err':"Alert: Institution code didn't matched. Try contacting Admin'",'code':404,'err_msg_text':"Admin Portal not found. Try again"       }
            return render(req,"StPage/error.html",context)
        else :pass
            # userName is user object
        if Grade in userName.active_portals: #type:ignore
            try:
                AdminInfo = userName.admininfo_set.get(id=int(userName.active_portals[str(req.session['Grade'])])) #type:ignore
            except:
                context={'err':"Alert: The admin is missing or encountered an error. Please check Institution Code and Grade.'",'code':404,'err_msg_text':"Page not found. Try again"}
                return render(req,"StPage/error.html",context)
        else:
            AdminInfo=userName.admininfo_set.filter(FOR_CLASS=Grade).last()  # type:ignore
        if AdminInfo is not None: 
            Instant_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            Model_time_start = AdminInfo.Start_time.strftime('%Y-%m-%d %H:%M')
            Model_time_end = AdminInfo.End_time.strftime('%Y-%m-%d %H:%M')
            if Instant_time >= Model_time_start and Instant_time <= Model_time_end:
                    form = StLoginForm(req.POST)
                    if form.is_valid():
                        # Getting Code Name
                        AdminCode = form.cleaned_data['AdInsCode'] 
                        Grade = form.cleaned_data['Grade']
                        # filtered User -> Teacher Admin User Exixts
                        # checking wheather or not use exists
                        FiltUser = CustomUser.objects.filter(first_name=AdminCode)
                        # Checks wheather or not institute code exist
                        if FiltUser.exists():
                            FormInst=form.save(commit=False)
                            FormInst.User_id= FiltUser.last().id #type:ignore
                            form.save()
                            req.session['STUDENT_CHECKED'] = True
                            req.session.save()
                            return redirect(f"/{AdminCode}/{Grade}")
                        else:
                            err="Institute Code not found."                
            else:
                context={
                            'err': "You should login with in provided time limit.",
                            'code':"Time Limit ",
                            'err_msg_text':f"Portal opens at {Model_time_start} and closes at {Model_time_end}."
                        }
                return render(req,"StPage/error.html",context)
        else:
            context={'err':"Alert: The admin is missing or encountered an error. Please check Institution Code and Grade.'",'code':404,'err_msg_text':"Page not found. Try again"       }
            return render(req,"StPage/error.html",context)
    form = StLoginForm()
    context={
        'form':form,
        'err':err
    }

    return render(req,"Stpage/index.html",context)

# Institute code is for sure valid because of FiltUser.exists()
def QuesHandler(req,InstituteCode,Grade):
    # STUDENT_CHECKED ensures that one student cannot give exam twice by 
    if req.session.get('STUDENT_CHECKED',False) == True:
        # seesion var set in StLogin
        SessStName = req.session.get('StName')
        # first_name in database = Institute code
        # Getting User only 
        # this process consumes a liitle more resoources
        # since we first grab user from CustomUser then navigate to its corresponding AdminInfo
        # we could have directly used AdminInFo Module
        userName= CustomUser.objects.filter(first_name=InstituteCode).last() # this last doesn't make sense cuz first_name is also unique
        # userName is user object
        if Grade in userName.active_portals: #type:ignore
            AdminInfo=userName.admininfo_set.get(id=req.session[str(Grade)]) #type:ignore
        else:
            AdminInfo=userName.admininfo_set.filter(FOR_CLASS=Grade).last()  # type:ignore

        if AdminInfo is not None: 
            # checking wheather or not student is with in Required time stamp
            # time of the instant shen student tried to login
            Instant_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            Model_time_start = AdminInfo.Start_time.strftime('%Y-%m-%d %H:%M')
            Model_time_end = AdminInfo.End_time.strftime('%Y-%m-%d %H:%M')
            if Instant_time >= Model_time_start and Instant_time <= Model_time_end:
                Main_Dict,Images_Dict=WordFileHandler(AdminInfo.FILENAME,AdminInfo.FULLMARKS,AdminInfo.IMAGES_DICT)
                if Main_Dict is not None:
                    # gets student object from Model
                    student_object = StInfoModels.objects.filter(Name=SessStName).last() 
                    # checking if student exists or not
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
                            "MEDIA_ROOT":settings.MEDIA_URL,
                            "InsCode":InstituteCode
                        }
                        req.session['STUDENT_CHECKED']=False
                        req.session.save()
                        return render(req,"StPage/QuesPap.html",context=context) 
                    else:
                        context ={
                            'err':"Student: Nonexistent or Student Error. Try Again",
                            'code':404,
                            'err_msg_text':"Student login error."
                        }
                        return render(req,"StPage/error.html",context) # context is required to pass
                else:
                    context={
                        'err':"Admin Error: Questions found > Questions required. Seek admin for resolution.",
                        'code':404,
                        'err_msg_text':"Question not enough to meet the requirement"
                        }
                    return render(req,"StPage/error.html",context)
            else:
                context={
                    'err': "You should login with in provided time limit.",
                    'code':"Time Limit ",
                    'err_msg_text':f"Portal opens at {Model_time_start} and closes at {Model_time_end}."
                }
                return render(req,"StPage/error.html",context)

        else:
            context={
                'err':"Alert: The admin is missing or encountered an error. Please check Institution Code and Grade.'",
                'code':404,
                'err_msg_text':"Page not found. Try again"
            }
            return render(req,"StPage/error.html",context)
    else:
        return redirect(StLogin)
    
# This block of code handles teh favicon error
# that occurs when django searche for favicon by default.
def empty_favicon_view(request):
    return HttpResponse(status=204)

def Submition(req):
    Bin_data=req.GET.get('data')
    InsCode = req.GET.get('inscode')
    print(dict(req.GET))
    int_data=int(Bin_data,2)
    StName = req.session.get('StName')
    Grade = req.session['Grade'] 
    StObj=StInfoModels.objects.filter(Name=StName,Touched_Status=False)[0]
    StObj.MarksAch=int_data
    # since firstname is also unique, using last or not using doesn't matter
    user_obj = CustomUser.objects.filter(first_name=InsCode).last() #type:ignore
    print(CustomUser.objects.values('first_name'),InsCode)
    user_obj_activePortal_db = user_obj.active_portals #type:ignore
    if Grade in user_obj_activePortal_db:
        Admin_set_passmarks = user_obj.admininfo_set.get(id=user_obj_activePortal_db[Grade]).PASSMARKS  # type:ignore 
    else:
        Admin_set_passmarks = user_obj.admininfo_set.last().PASSMARKS  # type:ignore 
         
    if int_data >= Admin_set_passmarks:
        StObj.Pass = True
    else:
        StObj.Pass = False
    StObj.save()
    print("Done. Worked...")
    return HttpResponseRedirect("/")
