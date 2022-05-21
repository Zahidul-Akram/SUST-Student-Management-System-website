from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from student_management_app.EmailBackEnd import EmailBackEnd


def showLoginpage(request):
    return render(request,"login_page.html")

def dologin(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        user=EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect("/faculty_home")
            else:
                return HttpResponseRedirect("/student_home")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")
def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" UserType : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


