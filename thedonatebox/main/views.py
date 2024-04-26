from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from django.shortcuts import get_object_or_404
from .models import userinfo, contactinfo
from random import randint

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == "POST":
        print("post request")
        username = request.POST['username']
        password = request.POST['password']

        try:
            usr = userinfo.objects.get(username=username)
            if usr.username==username and usr.password==password:
                response = render(request, "donate.html",{'name':usr.username,'email':usr.email,'phone':usr.phone})
                response.set_cookie("username", usr.username, 24*60*60)
                return response
        except Exception as e:
            print("Exception : ",e)
    return render(request, 'login.html',)


def signup(request):
    if request.method == "POST":
        print("post method")
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                usr = userinfo(username = username, phone = phone, email = email, password = password1)
                usr.save()
            except Exception as e:
                print("Exception :  ",e)
            return render(request, 'login.html')

    return render(request, 'signup.html')

def logout(request):
    pass

def AdminView(request, msg=""):

    try:
        username = request.COOKIES['username']
        _contact = contactinfo.objects.all()
        data = []
        for cont in _contact:
            _usr = userinfo.objects.get(username=cont.name)
            data.append({'username':cont.name,'phone':_usr.phone,'address':cont.address,'image':cont.image,'item':cont.item, 'email':_usr.email})
        return render(request, "customizedadmin.html",{'tempArr':data, "range":range(len(_contact)),"msg":msg})
        
    except Exception as e:
        print("exception :  ", e)
        return render(request, "customizedadmin.html",{"msg":"Please Login to see the Admin page"})


def acceptitem(request):
    item = "null"
    if request.method == "POST":
        item = request.POST["item"]
        email = request.POST["email"]

        try:
            my_email = "en20133485@git-india.edu.in"
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(my_email, "xyz@8910")

            message = MIMEText(f"Your item '{item}' accepted successfully")
            message["From"] = my_email
            message["To"] = email
            message["Subject"] = "About Item"
            
            server.sendmail(my_email, email, message.as_string())
            print("Email sent successfully!")

            return AdminView(request,msg="Item {item} accepted successfully")
        except Exception as e:
            print(e)
            return render(request, "home.html")






        
    

    


def contact(request):    
    if request.method == "POST":
        address = request.POST['address']
        item = request.POST['item']
        
        image = request.FILES['image']

        print(image)
        _contact = contactinfo(name=request.COOKIES['username'], address=address, item=item, image=image)
        _contact.save()
        return render(request, 'submitted.html', {})
    else:
        try:
            username = request.COOKIES['username']
            usr = userinfo.objects.get(username=username)
            return render(request, 'donate.html',{"name":username,'email':usr.email,'phone':usr.phone,'messages':[]})
        except:
            return render(request, 'login.html', {'messages':[]})
    


def enterotp(request):
    return render(request, "forgot-password.html")

def forgotpass(request):
    if request.method == 'POST':
        global otp,email
        try:
            entered_otp = request.POST['otp']
            print("otp:",otp)
            if int(entered_otp) == int(otp):
                return render(request, 'reset-password.html')
            else:
                return render(request, 'verify-otp.html', {'msg':"OTP didn't matched", 'otp':''})
        except:
            otp = randint(100000, 999999)
            body = f'The OTP for password reset is {otp}'
            
            
            try:
                email = request.POST["email"]
                print(email)
                row = userinfo.objects.get(email=email)
            except Exception as e:
                print(e)
                return render(request, 'forgot-password.html',{'msg':"Error while connecting to database", 'otp':''})

            if row != None:
                try:
                    my_email = "en20133485@git-india.edu.in"
                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.login(my_email, "xyz@8910")

                    message = MIMEText(f"Your otp is {otp}")
                    message["From"] = my_email
                    message["To"] = email
                    message["Subject"] = "Forgot passward OTP"
                    
                    server.sendmail(my_email, email, message.as_string())
                    print("Email sent successfully!")


                    print("otp sent ", otp)
                    return(render(request, "verify-otp.html",{}))
                except Exception as e:
                    print(e)
            else:
                return render(request, 'forgot-password.html',{'msg':"Email not found in database. You don't have accound", 'otp':''})
    return(render(request, "forgot-password.html" ))
    

def setnewpass(request):
    global email
    print(email)
    if request.method == "POST":
        newpass = request.POST['pass1']
        confnewpass = request.POST['pass2']
        usr = userinfo.objects.get(email=email)
        usr.password = newpass
        usr.save()
        return render(request, 'login.html', {'msg':'Password changed. Login with new password'})
    return render(request, 'reset-password.html')

