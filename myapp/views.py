import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from myapp.models import Complaint, Users, Log


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
        elif user.groups.filter(name="user"):
            return redirect('/myapp/userhome_get/')
        else:
            messages.error(request,"No such group")
            return redirect('/myapp/loginindex_get/')
    else:
        messages.error(request, "No user found")
        return redirect('/myapp/loginindex_get/')

def logout_get(request):
    logout(request)
    return redirect("/myapp/loginindex_get/")


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
    data=Log.objects.all()
    return render(request,'admins/viewlogs.html',{'logs':data})

def viewusers_get(request):
    data=Users.objects.all()
    return render(request,'admins/viewuser.html',{'Users': data})
def viewblockedusers_get(request):
    data=Users.objects.filter(status="Blocked")
    return render(request,'admins/blockusers.html',{'Users': data})
def blockuser_get(request,id):
    Users.objects.filter(id=id).update(status="Blocked")
    return redirect('/myapp/viewblockedusers_get/')



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
    name=request.POST["name"]
    dob=request.POST["dob"]
    email=request.POST["email"]
    phone=request.POST["phone"]
    gender=request.POST["gender"]
    photo=request.FILES["photo"]
    password=request.POST["password"]
    confirmpassword=request.POST["confirmpassword"]
    if password!=confirmpassword:
        messages.error(request,"Passwords did not match")
        return redirect("/myapp/register_get/")
    fs=FileSystemStorage()
    date=datetime.datetime.now().strftime("%d-%M-%Y-%H-%M-%S")+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    user=User.objects.create_user(username=email,password=password)
    user.groups.add(Group.objects.get(name='user'))
    user.save()


    u=Users()
    u.name=name
    u.dob=dob
    u.email=email
    u.phone=phone
    u.gender=gender
    u.photo=path
    u.AUTH_USER=user
    u.save()


    return redirect('/myapp/loginindex_get/')

def sentcomplaint_get(request):
    return render(request,'users/sentcomplaint.html')

def sentcomplaint_post(request):
    return render(request,'users/sentcomplaint.html')

def viewprofile_get(request):
    return render(request,'users/viewprofile.html')

def viewreply_get(request):
    return render(request,'users/viewreply.html')

def userhome_get(request):
    return render(request,'users/userhome.html')

