import datetime 
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from django.contrib import messages
from .models import createlink, Instruction
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
        if request.POST["course_name"].strip() == "" or request.POST["assignment_name"].strip() == "" or request.POST["result_time"] == "" or request.POST["start"] =="":
                messages.error(request,"Fill all the details to continue!")
                return redirect("./")

        start = request.POST["start"].replace('T',' ')
        first_sub_time = request.POST["first_sub_time"].replace('T',' ')
        second_sub_time = request.POST["second_sub_time"].replace('T',' ')
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
        create.no_of_submissions = request.POST["no_of_submissions"]
        create.perc_penalty = request.POST["perc_penalty"]
        create.notif = request.POST["notif"]  
        create.face_rec = request.POST["face_rec"] 
        create.neg_mark = request.POST["neg_mark"]
        create.res_anno= request.POST["res_anno"]
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
        Instruction.objects.create(instructions= "", assignment_id = create.id )
        messages.success(request,f"Assignment has been created successfully!")
        return redirect("../"+link+"/")
    return render(request,"CreateAssignment/home.html")

@login_required
def summary(request,link):
    codes_id=createlink.objects.filter(link=link).first()
    return render(request, "CreateAssignment/summary.html", {"assign": codes_id})


@login_required
def instructions(request,link):
    code = createlink.objects.filter(link=link).first()
    inst = Instruction.objects.filter(assignment_id = code.id).first()
    if request.method == "POST":
         inst.instructions = request.POST["instructions"]
         inst.save()
         messages.success(request,f"Instructions have been updated successfully!")
         return redirect("/")
    return render(request,"CreateAssignment/instructions.html")

@login_required
def edit(request,link):
        
    codes = createlink.objects.filter(link = link).all()
    # if codes.first() is None:
    #     return render(request,"public/something.html",{'msg':"Check your link again. This Link is not valid.","videos":topThree()})
    # if request.user.id != codes.first().creator_id:
    #     return render(request,"public/something.html",{"msg":"You are not allowed on this page. Please go back.","videos":topThree()})
    if request.method == 'POST':
        start = request.POST["start"].replace('T',' ')
        first_sub_time = request.POST["first_sub_time"].replace('T',' ')
        second_sub_time = request.POST["second_sub_time"].replace('T',' ')
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

        for code in codes:
            code.course_name = request.POST["course_name"].strip().replace(" ","-")
            code.assignment_name = request.POST["assignment_name"].strip().replace(" ","-")
            code.start = request.POST["start"]
            code.first_sub_time = request.POST["first_sub_time"]
            code.second_sub_time = request.POST["second_sub_time"]
            code.no_of_submissions = request.POST["no_of_submissions"] 
            code.perc_penalty = request.POST["perc_penalty"]
            code.notif = request.POST["notif"] 
            code.face_rec = request.POST["face_rec"]
            code.neg_mark = request.POST["neg_mark"] 
            code.res_anno= request.POST["res_anno"]
            code.creator_id = request.user.id
            code.result_time = request.POST["result_time"]
            code.save()
        messages.success(request,"Settings Updated Successfully")
        return redirect('/')
    code = codes.first()
    # start_v = str(code.start)[:10]+'T'+str(code.start)[11:16]
    # end_v = str(code.margin)[:10]+'T'+str(code.margin)[11:16]
    # res_t = str(code.result_time)[:10]+'T'+str(code.result_time)[11:16]
    data = {'course':code.course_name,'topic':code.assignment_name,'start':code.start,'first_sub_time':code.first_sub_time,'second_sub_time':code.second_sub_time,"code_id":code.id,"no_of_submissions":code.no_of_submissions,"perc_penalty""ttype":code.perc_penalty,"notif":code.notif, "face_rec":code.face_rec, "neg_mark":code.neg_mark, "res_anno": code.res_anno,"result_time" :code.result_time}
    return render(request,'CreateAssignment/settings.html',data)
