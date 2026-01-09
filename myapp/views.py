from django.shortcuts import render



def login_get(request):
    return render(request,'login.html')

def login_post(request):
    return render(request,'login.html')
def loginindex_get(request):
    return render(request,'loginindex.html')

def loginindex_post(request):
    return render(request,'loginindex.html')

def forgot_get(request):
    return render(request,'forgotpassword.html')


def forgot_post(request):
    return render(request,'forgotpassword.html')

# A D M I N--------------------------------
def admin_home(request):
    return render(request,'admins/adminhomeindex.html')

def viewcomplaint_get(request):
    return render(request,'admins/viewcomplaint.html')

def viewlogs_get(request):
    return render(request,'admins/viewlogs.html')

def viewusers_get(request):
    return render(request,'admins/viewuser.html')

def changepassword_get(request):
    return render(request,'admins/changepassword.html')

def changepassword_post(request):
    return render(request,'admins/changepassword.html')

def sentreply_get(request):
    return render(request,'admins/sentreply.html')

def sentreply_post(request):
    return render(request,'admins/sentreply.html')

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
