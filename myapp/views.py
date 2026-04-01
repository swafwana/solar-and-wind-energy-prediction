import smtplib
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from myapp.models import Complaint, Users, Log

from django.http import JsonResponse
import json
# def login_get(request):
#     return render(request,'login.html')
#
# def login_post(request):
#     return render(request,'login.html')
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


def forgotpassword_get(request):
    return render(request,'forgotpassword.html')

def forgotpassword_post(request):


    email=request.POST['email']

    if User.objects.filter(username=email).exists():

        import random
        new_pass = random.randint(00000, 99999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leagaladvisorteam@gmail.com", " eugnxtyylwtqwlav")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)  # Disconnect from the server
        server.quit()

        user = User.objects.get(username=email)
        user.set_password(str(new_pass))
        user.save()

        return redirect('/myapp/loginindex_get/')
    else:
        messages.warning(request, 'email not  exists')
        return redirect('/myapp/forgotpassword_get/')

# A D M I N--------------------------------
@login_required(login_url="/myapp/loginindex_get/")
def admin_home(request):
    return render(request,'admins/adminhomeindex.html')

def viewcomplaint_get(request):
    data=Complaint.objects.all()

    return render(request,'admins/viewcomplaint.html',{'c':data})
@login_required(login_url="/myapp/loginindex_get/")
def viewlogs_get(request):
    data=Log.objects.all()
    return render(request,'admins/viewlogs.html',{'logs':data})
@login_required(login_url="/myapp/loginindex_get/")
def viewusers_get(request):
    data=Users.objects.all()
    return render(request,'admins/viewuser.html',{'Users': data})
@login_required(login_url="/myapp/loginindex_get/")
def viewblockedusers_get(request):
    data=Users.objects.filter(status="Blocked")
    return render(request,'admins/blockusers.html',{'Users': data})
@login_required(login_url="/myapp/loginindex_get/")
def blockuser_get(request,id):
    Users.objects.filter(id=id).update(status="Blocked")
    return redirect('/myapp/viewblockedusers_get/')


@login_required(login_url="/myapp/loginindex_get/")
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

@login_required(login_url="/myapp/loginindex_get/")
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
    date=datetime.now().strftime("%d-%M-%Y-%H-%M-%S")+'.jpg'
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
@login_required(login_url="/myapp/loginindex_get/")
def sentcomplaint_get(request):
    return render(request,'Users/sentcomplaint.html')

def sentcomplaint_post(request):
    comp= request.POST["complaint"]
    c= Complaint()
    c.date=datetime.now().date()
    c.complaint=comp
    c.reply="Pending"
    c.status="Pending"

    c.USER=Users.objects.get(AUTH_USER=request.user)
    c.save()
    return redirect("/myapp/viewreply_get/")
@login_required(login_url="/myapp/loginindex_get/")
def viewprofile_get(request):
    data=Users.objects.get(AUTH_USER=request.user)


    return render(request,'Users/viewprofile.html',{'data': data})
@login_required(login_url="/myapp/loginindex_get/")
def user_changepassword_get(request):
    return render(request,'Users/changepassword.html')

def user_changepassword_post(request):
    current_password=request.POST["currentpassword"]
    new_password = request.POST["newpassword"]
    confirm_password = request.POST["confirmpassword"]
    user=request.user
    if not user.check_password(current_password):
        messages.error(request,"Invalid  Password")
        return redirect('/myapp/user_changepassword_get/')

    if new_password != confirm_password:
        messages.error(request, "Password doesn't match")
        return redirect('/myapp/user_changepassword_get/')
    user.set_password(new_password)
    user.save()

    return redirect('/myapp/loginindex_get/')
@login_required(login_url="/myapp/loginindex_get/")
def editprofile_get(request):
    u = Users.objects.get(AUTH_USER_id=request.user.id)

    return render(request,'Users/edit.html',{'data':u})

def editprofile_post(request):
    name = request.POST["name"]
    dob = request.POST["dob"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    gender = request.POST["gender"]
    id = request.POST["id"]


    u = Users.objects.get(id=id)
    t=u.AUTH_USER
    t.username=email
    t.save()

    if 'photo' in request.FILES:

        photo = request.FILES["photo"]
        fs = FileSystemStorage()
        date = datetime.now().strftime("%d-%M-%Y-%H-%M-%S") + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        u.photo = path
        u.save()

    u.name = name
    u.dob = dob
    u.email = email
    u.phone = phone
    u.gender = gender
    u.AUTH_USER = t
    u.save()

    return redirect("/myapp/viewprofile_get/")
@login_required(login_url="/myapp/loginindex_get/")
def viewreply_get(request):
    data = Complaint.objects.filter(USER__AUTH_USER=request.user)

    return render(request, 'Users/viewreply.html', {'c': data})

@login_required(login_url="/myapp/loginindex_get/")
def userhome_get(request):
    # Quick debug - add this temporarily
    # print(f"Logged in user: {request.user.username}")
    # print(f"Is staff: {request.user.is_staff}")
    #
    # # Check how many logs exist for this user
    # user_logs = Log.objects.filter(USER__AUTH_USER=request.user)
    # print(f"Logs for this user: {user_logs.count()}")
    #
    # # Check total logs in database
    # total_logs = Log.objects.all().count()
    # print(f"Total logs in DB: {total_logs}")
    #
    # # If counts don't match, you're seeing other users' data
    # if user_logs.count() != total_logs:
    #     print("WARNING: There are logs from other users!")


    # Get total predictions count for the user
    total_predictions = Log.objects.filter(USER__AUTH_USER=request.user).count()

    # Get recent predictions (last 5)
    recent_predictions = Log.objects.filter(
        USER__AUTH_USER=request.user
    ).order_by('-date', '-time')[:5]

    # Get solar vs wind counts
    solar_count = Log.objects.filter(
        USER__AUTH_USER=request.user,
        prediction_type="solar"
    ).count()

    wind_count = Log.objects.filter(
        USER__AUTH_USER=request.user,
        prediction_type="wind"
    ).count()

    context = {
        'total_predictions': total_predictions,
        'recent_predictions': recent_predictions,
        'solar_count': solar_count,
        'wind_count': wind_count,
    }
    return render(request, 'Users/userhome.html', context)


@login_required(login_url="/myapp/loginindex_get/")
def view_all_predictions(request):
    """Simple view for users to see all their predictions"""
    # Get all predictions for logged in user
    all_predictions = Log.objects.filter(
        USER__AUTH_USER=request.user
    ).order_by('-date', '-time')

    context = {
        'predictions': all_predictions,
        'total': all_predictions.count(),
    }
    return render(request, 'Users/all_predictions.html', context)
@login_required(login_url="/myapp/loginindex_get/")
def loadsolar_get(request):
    import pandas
    p="C:\\Users\\HK Technology\\PycharmProjects\\solar_and_wind_energy_prediction\\myapp\\Dataset\\Solar\\Weather_Data_reordered_all3.csv"
    data = pandas.read_csv(p)
    print(data.values)


    return render(request,'Users/loadsolar.html',{'c':data.values})
@login_required(login_url="/myapp/loginindex_get/")
def loadwind_get(request):
    import pandas
    p="C:\\Users\\HK Technology\\PycharmProjects\\solar_and_wind_energy_prediction\\myapp\\Dataset\\Wind\\Location1.csv"

    data=pandas.read_csv(p)
    print(data.values)
    return render(request,'Users/loadwind.html',{'c':data.values})
@login_required(login_url="/myapp/loginindex_get/")
def solarinput_get(request):
    return render(request, 'Users/solarinput.html')

import pandas as pd
from django.shortcuts import render

# Load CSV only once (when server starts)
file_path = r"C:\Users\HK Technology\PycharmProjects\solar_and_wind_energy_prediction\myapp\Dataset\Solar\preprocessed.csv"

df = pd.read_csv(file_path)

# Convert CSV Timestamp column to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])


# def solarinput_post(request):
#
#     if request.method == "POST":
#
#         date = request.POST.get("date")        # 2020-01-02
#         time = request.POST.get("timestamp")   # 08:00
#
#         # Combine and convert to datetime
#         full_timestamp = pd.to_datetime(date + " " + time)
#
#         # Match using datetime
#         result = df[df["Timestamp"] == full_timestamp]
#
#         if not result.empty:
#             solar_generation = result.iloc[0]["SolarGeneration"]
#         else:
#             solar_generation = "No matching data found"
#         print("solar_energy:",solar_generation)
#
#         return render(request, "Users/solarinput.html", {
#             "solar_generation": solar_generation
#         })
#
#     return render(request, "Users/solarinput.html")
#
# def solarinput_post(request):
#
#     if request.method == "POST":
#
#         try:
#             data = json.loads(request.body)
#
#             date = data.get("date")
#             time = data.get("timestamp")
#
#             if not date or not time:
#                 return JsonResponse({"error": "Date or Time missing"}, status=400)
#
#             full_timestamp = pd.to_datetime(date + " " + time)
#
#             result = df[df["Timestamp"] == full_timestamp]
#
#             if not result.empty:
#                 solar_generation = result.iloc[0]["SolarGeneration"]
#             else:
#                 solar_generation = "No matching data found"
#
#             return JsonResponse({
#                 "solar_generation": solar_generation
#             })
#
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#
#     return JsonResponse({"error": "Invalid request"}, status=400)


import json
import pandas as pd
import joblib
from django.http import JsonResponse
#
# model = joblib.load("solar_model.pkl")
import os
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, "myapp", "solar_model.pkl")
model = joblib.load(model_path)

def solarinput_post(request):
    from datetime import datetime
    if request.method == "POST":

        try:
            data = json.loads(request.body)

            timestamp = data.get("timestamp")
            apparent_temp = float(data.get("ApparentTemperature"))
            air_temp = float(data.get("AirTemperature"))
            dew_temp = float(data.get("DewPointTemperature"))
            humidity = float(data.get("RelativeHumidity"))
            wind_speed = float(data.get("WindSpeed"))
            wind_direction = float(data.get("WindDirection"))

            if not timestamp:
                return JsonResponse({"error": "Timestamp missing"}, status=400)

            full_timestamp = pd.to_datetime(timestamp)

            hour = full_timestamp.hour
            month = full_timestamp.month

            input_data = pd.DataFrame([[
                apparent_temp,
                air_temp,
                dew_temp,
                humidity,
                wind_speed,
                wind_direction,
                hour,
                month
            ]], columns=[
                "ApparentTemperature",
                "AirTemperature",
                "DewPointTemperature",
                "RelativeHumidity",
                "WindSpeed",
                "WindDirection",
                "hour",
                "month"
            ])

            prediction = model.predict(input_data)[0]
            # print(prediction,"pppppppppppppppppppppppppppppppp")

            l=Log()

            # from datetime import datetime
            l.date=datetime.now().date()
            l.time=datetime.now().time()
            l.result=float(prediction)
            l.prediction_type = "solar"
            l.USER = Users.objects.get(AUTH_USER=request.user)
            l.save()





            return JsonResponse({
                "predicted_solar_generation": float(prediction)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required(login_url="/myapp/loginindex_get/")
def windinput_get(request):
    return render(request,'Users/windinput.html')
import json
import pandas as pd
import joblib
from django.http import JsonResponse


# load model once
model_wind = joblib.load("C://Users//HK Technology//PycharmProjects//solar_and_wind_energy_prediction//myapp//power_prediction_model1.pkl")


def windinput_post(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            timestamp = data.get("timestamp")

            temperature_2m = float(data.get("temperature_2m"))
            relativehumidity_2m = float(data.get("relativehumidity_2m"))
            dewpoint_2m = float(data.get("dewpoint_2m"))
            windspeed_10m = float(data.get("windspeed_10m"))
            windspeed_100m = float(data.get("windspeed_100m"))
            winddirection_10m = float(data.get("winddirection_10m"))
            winddirection_100m = float(data.get("winddirection_100m"))
            windgusts_10m = float(data.get("windgusts_10m"))

            if not timestamp:
                return JsonResponse({"error": "Timestamp missing"}, status=400)

            # convert timestamp
            dt = datetime.fromisoformat(timestamp)

            hour = dt.hour
            month = dt.month

            # create dataframe in same order as training
            input_data = pd.DataFrame([[
                temperature_2m,
                relativehumidity_2m,
                dewpoint_2m,
                windspeed_10m,
                windspeed_100m,
                winddirection_10m,
                winddirection_100m,
                windgusts_10m,
                hour,
                month
            ]], columns=[
                "temperature_2m",
                "relativehumidity_2m",
                "dewpoint_2m",
                "windspeed_10m",
                "windspeed_100m",
                "winddirection_10m",
                "winddirection_100m",
                "windgusts_10m",
                "hour",
                "month"
            ])

            prediction = model_wind.predict(input_data)

            l_wind = Log()

            l_wind.date = datetime.now().date()
            l_wind.time = datetime.now().time()
            l_wind.result = float(prediction[0])  # FIXED
            l_wind.prediction_type = "wind"
            l_wind.USER = Users.objects.get(AUTH_USER=request.user)
            l_wind.save()

            return JsonResponse({
                "predicted_power": float(prediction[0])
            })


        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)