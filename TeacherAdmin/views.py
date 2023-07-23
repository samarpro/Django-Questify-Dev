from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User 
from .forms import AdminInfoForms
from .models import AdminInfo
from pathlib import Path
from django.conf import settings
from StPage.models import StInfoModels
from docx import Document
# Create your views here.
def dashboard(req):
    user=req.user
    if not user.is_anonymous:
        print(type(user) ,user=="AnonymousUser") 
        List_St = StInfoModels.objects.filter(User=user)
        AdminUser = AdminInfo.objects.filter(user=user).last()
        context={
            "ListSt":List_St,
            "PMarks": AdminUser.PASSMARKS, #type:ignore
        }
        return render(req,"TeacherAdmin/dashboard.html",context)
    else:
        return redirect("validator/")

def uploadInfo(req):
    err=msg=""
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
            Obj.save(commit=False) # type: ignore
            msg = "Online Exam Successfully Created."
            err= False
            # namespace for finding images
            
            CustomNsmap = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
            }
            Docx_file = Document(file)
            "Checking each paragraph if contains images at last or not."
            for index,paragraph in enumerate(Docx_file.paragraphs):
                image_object_blip=paragraph.runs[-1]._element.findall('.//a:blip', namespaces=CustomNsmap)
                if image_object_blip:
                    static_images_root = Path(settings.MEDIA_ROOT) / "Admin_Images"
                    for obj_blip in image_object_blip:
                        rId = obj_blip.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if rId:
                            image_part = Docx_file.part.rels[rId].target_part
                            image_binary_data = image_part.blob
                            image_format = image_part.content_type.split("/")[-1]
                            # image_path = join(saving_path,f"adminname-quesno.{image_format}")
                            image_path = Path(static_images_root)/f"9h"
                            with open(image_path,"wb") as f : # type: ignore
                                f.write(image_binary_data)
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