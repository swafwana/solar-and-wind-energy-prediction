"""
URL configuration for solar_and_wind_energy_prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [


    # path('loginindex_get/',views.loginindex_get),

    path('loginindex_get/', views.loginindex_get),
    path('loginindex_post/',views.loginindex_post),
    path('forgotpassword_get/',views.forgotpassword_get),
    path('forgotpassword_post/',views.forgotpassword_post),
    path('logout_get/',views.logout_get),

    #ADMIN
    path('admin_home/',views.admin_home),

    path('viewcomplaint_get/',views.viewcomplaint_get),
    path('viewlogs_get/',views.viewlogs_get),
    path('viewusers_get/',views.viewusers_get),
    path('changepassword_get/',views.changepassword_get),
    path('changepassword_post/',views.changepassword_post),
    path('sentreply_get/<id>',views.sentreply_get),
    path('sentreply_post/',views.sentreply_post),
    path('viewblockedusers_get/',views.viewblockedusers_get),
    path('blockuser_get/<id>',views.blockuser_get),
    #USER
    path('register_get/',views.register_get),
    path('register_post/',views.register_post),
    path('sentcomplaint_get/',views.sentcomplaint_get),
    path('sentcomplaint_post/',views.sentcomplaint_post),
    path('viewprofile_get/',views.viewprofile_get),
    path('editprofile_get/',views.editprofile_get),
    path('editprofile_post/',views.editprofile_post),
    path('user_changepassword_get/',views.user_changepassword_get),
    path('user_changepassword_post/',views.user_changepassword_post),
    path('viewreply_get/',views.viewreply_get),
    path('userhome_get/',views.userhome_get),
    path('loadsolar_get/',views.loadsolar_get),
    path('loadwind_get/',views.loadwind_get),
    path('solarinput_get/',views.solarinput_get),
    path('solarinput_post/',views.solarinput_post),
    path('windinput_get/',views.windinput_get),
    path('windinput_post/',views.windinput_post),











]
