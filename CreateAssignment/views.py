import datetime 
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from django.contrib import messages
from .models import createlink,Instructions
from django.shortcuts import redirect, render
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DeleteView
from django.contrib import messages

RANDOM_LINK_GENERATED=''
def randlink():
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    letters = []
    for i in alphabets:
        letters.append(i)
    link ='' 
    for i in range(10):
        link += letters[random.randint(0,25)]
        if i==2 or i == 6 :
            link+='-'
    return link
# Create your views here.
@login_required
def linkcreate(request):
    
    if request.method == "POST":
        # print('HELLO WORLD')
        #try:
           # if request.POST["course_name"].strip() == "" or request.POST["assign_name"].strip() == "" or request.POST["result_time"] == "" or request.POST["start"] =="":
               # messages.error(request,"Fill all the details to continue!")
                #return redirect("./")
        #except:
              #  messages.error(request,"Fill all the details to continue!")
               # return redirect("./")
        start = request.POST["start"].replace('T',' ')
        first_sub_time = request.POST["first_sub_time"].replace('T',' ')
        second_sub_time = request.POST["second_sub_time"].replace('T',' ')
        no_of_submissions = request.POST["no_of_submissions"]
        perc_penalty = request.POST["perc_penalty"]
        notif = request.POST["notif"]
        face_rec = request.POST["face_rec"]
        neg_mark = request.POST["neg_mark"]
        res_anno = request.POST["res_anno"]
        result_time = request.POST["result_time"].replace('T',' ')
        ajf =str(datetime.datetime.strptime(first_sub_time, '%Y-%m-%d %H:%M')-datetime.datetime.strptime(start, '%Y-%m-%d %H:%M'))
        if ajf[0] == '-' or ajf == '0:00:00':
            messages.error(request,'Start time cannot be same or greater than first submission time')
            return redirect('./')
        if str(datetime.datetime.strptime(second_sub_time, '%Y-%m-%d %H:%M')-datetime.datetime.strptime(first_sub_time, '%Y-%m-%d %H:%M'))[0] == '-':
            messages.error(request,'First submission time cannot be same or greater than second submission time')
            return redirect('./')
        if str(datetime.datetime.strptime(result_time, '%Y-%m-%d %H:%M')-datetime.datetime.strptime(second_sub_time, '%Y-%m-%d %H:%M'))[0] == '-':
            messages.error(request,'Second submission time cannot be greater than result time')
            return redirect('./')

        if (datetime.datetime.strptime(start, '%Y-%m-%d %H:%M') <= datetime.datetime.now()):
            messages.error(request,'Start time has to be in future')
            return redirect('./')

        create = createlink()
        create.course_name = request.POST["course_name"].strip().replace(" ","-")
        create.assignment_name = request.POST["assignment_name"].strip().replace(" ","-")
        create.start = request.POST["start"]
        create.first_sub_time = request.POST["first_sub_time"]
        create.second_sub_time = request.POST["second_sub_time"]
        create.no_of_submissions = request.POST["no_of_submissions"].strip().replace(" ","-") 
        create.perc_penalty = request.POST["perc_penalty"].strip().replace(" ","-") 
        create.notif = request.POST["notif"].strip().replace(" ","-")  
        create.face_rec = request.POST["face_rec"].strip().replace(" ","-") 
        create.neg_mark = request.POST["neg_mark"].strip().replace(" ","-") 
        create.res_anno= request.POST["res_anno"].strip().replace(" ","-") 
        create.creator_id = request.user.id
        create.result_time = request.POST["result_time"]
        link = None
        while(True):
            link = randlink()
            if createlink.objects.filter(link= link).first() is None:
                break
        print("link",link)
        create.link= link
        create.save()
        messages.success(request,f"Assignment has been created successfully!")
        return redirect("/")
    return render(request,"CreateAssignment/home.html")

@login_required
def instructions(request):
    # inst = instructions.objects.filter(link =createlink.objects.filter(link = link).first()).first()
    # if request.method == "POST":
    #     inst.instructions = request.POST["instructions"]
    #     inst.save()
    if request.method == "POST":
        inst_1 = request.POST["inst_1"]
        inst_2 = request.POST["inst_2"]
        inst_3 = request.POST["inst_3"]
        inst_4 = request.POST["inst_4"]
        inst_5 = request.POST["inst_5"]
        instructions = Instructions()
        instructions.inst_1 = request.POST["inst_1"]
        instructions.inst_2 = request.POST["inst_2"]
        instructions.inst_3 = request.POST["inst_3"]
        instructions.inst_4 = request.POST["inst_4"]
        instructions.inst_5 = request.POST["inst_5"]
        instructions.save()
        messages.success(request,f"Instructions have been updated successfully!")
        return redirect("/")
    return render(request,"CreateAssignment/instructions.html")

   
    
    # inst = instructions.objects.filter(link =createlink.objects.filter(link = link).first()).first()
    # if request.method == "POST":
    #     inst.instructions = request.POST["instructions"]
    #     inst.save()
    #     return redirect("./feed")
    # return redirect("./feed")

        



# @login_required
# def deletelink(request,link):
#     if request.method == "POST":
#         x = createlink.objects.filter(link = link).all().delete()
#         return redirect('CreateAssignment/home1.html')
#     return render(request,"CreateAssignment/home1.html")
