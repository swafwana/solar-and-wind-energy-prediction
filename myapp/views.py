from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from myapp.models import Complaint, Users


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    return render(request,'login.html')
def loginindex_get(request):
    return render(request,'loginindex.html')

def loginindex_post(request):
    Username = request.POST["username"]
    Password = request.POST["password"]
    user=authenticate(request,username=Username,password=Password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name="admin"):
            return redirect('/myapp/admin_home/')
        else:
            messages.error(request,"No such group")
            return redirect('/myapp/loginindex_get/')
    else:
        messages.error(request, "No user found")
        return redirect('/myapp/loginindex_get/')




def forgot_get(request):
    return render(request,'forgotpassword.html')


def forgot_post(request):
    return render(request,'forgotpassword.html')

# A D M I N--------------------------------
def admin_home(request):
    return render(request,'admins/adminhomeindex.html')

def viewcomplaint_get(request):
    data=Complaint.objects.all()

    return render(request,'admins/viewcomplaint.html',{'c':data})

def viewlogs_get(request):
    return render(request,'admins/viewlogs.html')

def viewusers_get(request):
    data=Users.objects.all()
    return render(request,'admins/viewuser.html',{'Users': data})

def changepassword_get(request):
    return render(request,'admins/changepassword.html')

def changepassword_post(request):
    current_password=request.POST["currentpassword"]
    new_password = request.POST["newpassword"]
    confirm_password = request.POST["confirmpassword"]
    user=request.user
    if not user.check_password(current_password):
        messages.error(request,"Invalid  Password")
        return redirect('/myapp/changepassword_get/')

    if new_password != confirm_password:
        messages.error(request, "Password doesn't match")
        return redirect('/myapp/changepassword_get/')
    user.set_password(new_password)
    user.save()

    return redirect('/myapp/loginindex_get/')


def sentreply_get(request,id):
    return render(request,'admins/sentreply.html',{'id':id})

def sentreply_post(request):
    reply=request.POST["reply"]
    id=request.POST["id"]

    data=Complaint.objects.get(id=id)
    data.reply=reply
    data.status="Replied"
    data.save()
    return redirect("/myapp/viewcomplaint_get/")




# U S E R

def register_get(request):
    return render(request,'users/register.html')

def register_post(request):
    return render(request,'users/register.html')

def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')

def sentcomplaint_post(request):
    return render(request,'users/sentcomplaint.html')

def viewprofile_get(request):
    return render(request,'users/viewprofile.html')

def viewreply_get(request):
    return render(request,'users/viewreply.html')
