from django.contrib import admin
from django.urls import path, include
from robot_func import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('details/', views.details, name="details"),
    path('control/', views.robot_control, name="robot_control"),
    path('account/', views.personal_account, name="account"),    

    #Auth
    path('signup/', views.signupuser, name="signupuser"),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

]
