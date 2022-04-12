from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re

# Create your views here.

def home(request):
    return render(request,"index.html")

def signup(request):

    #Get User data
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        #Chek Username if exist
        if User.objects.filter(username=username):
            messages.error(request,"This username is already taken please try again")
            return redirect("home")


        #Check Email if exist

        if User.objects.filter(email=email):
            messages.error(request,"This email already used in another account. please try again")
            return redirect("home")


        #Check Username Length

        if len(username) < 8 and len(username) > 16 :
            messages.error(request, "The lenght of the username between 8 and 16. please try again")
            return redirect("home")

        #Check Password

        if pass1 != pass2:
            messages.error(request, "Please recheck the password")
        #Check Password Regex

        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,16}$"
        match_re = re.compile(reg)
        res = re.search(match_re,pass1)

        if  res:
            pass
        else:
            messages.error(request, "Please enter password should be One Capital Letter  Special Character One Number  Length Should be 8-16: ")
            return redirect("home")

        #Chek Username isnt all number

        if not username.isalnum():
            messages.error(request,"Username must be Alphanumeric!")
            return redirect("home")



        #Save User data
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        #Success Message
        messages.success(request,"Your Account has been successfully created")
        #Redirect User to the sign in page
        return redirect("signin")
    return render(request,"signup.html")

def signin(request):
    if request.method == "POST":

        #Get user data
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        #Authentication
        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,"index.html",{'fname':fname})

        else:
            return HttpResponse(request,"Bad Credentials!")
            return redirect('home')


    return render(request,"signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("home")
