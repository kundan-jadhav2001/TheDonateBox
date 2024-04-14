from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages

from django.shortcuts import get_object_or_404
from .models import userinfo
# from pymongo import MongoClient
# import datetime
# client = MongoClient("mongodb://localhost:27017/")
# import cloudinary.uploader

# # Create your views here.
# db = client.thedonatebox
# collection = db.app_customer
# userinfo = db.app_userinfo
          
# cloudinary.config( 
#   cloud_name = "dslbnwrre", 
#   api_key = "543599432364487", 
#   api_secret = "aTumbr-nSvhAGJJLHbMxKCaC16Q" 
# )

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
            render(request, 'login.html')

    return render(request, 'signup.html')

def logout(request):
    pass

def AdminView(request):

    try:
        username = request.COOKIES['username']
        Customer.objects.get(user=username)
        data = collection.find()
        tempArr = []
        for i in data:
            tempArr.append(i)
        return render(request,'customizedadmin.html',{"tempArr":tempArr})

    except KeyError:
        return render(request, 'index.html', {'msg':"Please Signin to check the predictions."})
    except Exception as e:
        print(e)
        return render(request, 'prediction/database.html', {'msg':"No data to show"})
    return render(request, 'prediction/database.html', {'data':data})


    

# class RegistrationView(View):
#     def get(self, request):
#         form = RegistrationForm()
#         return render(request, 'app/signup.html', {'form': form})

#     def post(self, request):
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             if form.password1 == form.password2:
#                 # userinfo(username=form.username,phone=form.phone,email=form.email,password=form.password1).save()
#                 messages.success(request, 'Successfully Registered. Please login to continue.')
#             else:
#                 messages.error(request, 'Password and Confirm password not matched...')
#         return render(request, 'app/signup.html', {'form': form})
    

def contact(request):    
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            # user = request.user
            name = request.POST['name']
            phone = request.POST['phone']
            address = request.POST['address']
            item = request.POST['item']
            image = request.POST['image']
            print(image)
            upimage = cloudinary.uploader.upload("C:\\Users\\Fahad\\Desktop\\imgup\\"+image)
            print(upimage)
            reg = Customer(name=name, phone=phone, address=address, item=item, image=upimage['secure_url'])
            # messages.success(
            #     request, "Your Form has been Submitted"
            # )
            reg.save()
        return render(request, 'submitted.html', {'form': form,'messages':[]})
    else:
        try:
            username = request.COOKIES['username']
            usr = userinfo.objects.get(username=username)
            return render(request, 'donate.html',{"name":username,'email':usr.email,'phone':usr.phone,'messages':[]})
        except:
            return render(request, 'login.html', {'form': form,'messages':[]})
    

def forgotpass(request):
    if request.method == 'POST':
        global otp, email
        try:

            entered_otp = request.POST['otp']
            print('trying', entered_otp)
            print(otp)
            if int(entered_otp) == int(otp):
                return render(request, 'newpass.html')
            else:
                return render(request, 'forgotpass.html', {'msg':"OTP didn't matched", 'otp':''})
        except:
            otp = randint(100000, 999999)
            body = f'The OTP for password reset is {otp}'
            
            with connection.cursor() as cursor:
                try:
                    email = request.POST["email"]
                    cursor.execute("select name from userinfo where email = %s", [email])
                    row = cursor.fetchone()
                except Exception as e:
                    return render(request, 'forgotpass.html',{'msg':"Error while connecting to database", 'otp':''})

            if row != None:
                try:
                    send_mail(
                    'OTP',
                    body,
                    'kundanjadhav2001@gmail.com',
                    [f'{request.POST["email"]}'],
                    fail_silently=False,
                    )
                    return(render(request, "forgotpass.html",{'otp':otp}))
                except Exception as e:
                    print(e)
            else:
                return render(request, 'forgotpass.html',{'msg':"Email not found in database. You don't have accound", 'otp':''})
    return(render(request, "forgotpass.html", {'otp':''} ))
    

def setnewpass(request):
    print(email)
    if request.method == "POST":
        newpass = request.post['newpass']
        with connection.cursor() as cursor:
            cursor.execute(f"update userinfo set pass = {newpass} where email = {email};")
            return render(request, 'login.html')
    return render(request, 'forgotpass.html')




# def contact(request):
#     if request.method == 'POST':
#         try:
#             name = request.POST.get('name')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone')
#             address = request.POST.get('address')
#             item = request.POST.get('item')

#             input_data = {
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "address":address,
#             "item":item,
#             "date": datetime.datetime.now(tz=datetime.timezone.utc),
#             }
#             collection.insert_one(input_data)
#             messages.success(
#                 request, 'Thank you for contacting us! We will soon contact you for further updates.'
#             )
#         except Exception as e:
#                 request, 'Error'
#                 print('something went wrong',e)
            
#         return render(request, 'app/donate.html')
        
#     return render(request, 'app/donate.html')


