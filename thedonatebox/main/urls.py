from django.urls import path
from django.conf import settings

from .forms import LoginForm, RegistrationForm
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('customizedadmin',views.AdminView),
    path("accounts/login", views.login, name="login"),
    path('registration/', views.signup, name='registration'),
    
    path('accounts/logout/',views.logout, name='logout'),
    
    path('contact/', views.contact, name='contact'),

    path('forgotpass', views.forgotpass, name='forgotpass'),
    path('setnewpass', views.setnewpass, name='setnewpass'),
    path("acceptitem", views.acceptitem, name="acceptitem")

    

    # path('submitted/', views.submit, name="submitted"),
]
