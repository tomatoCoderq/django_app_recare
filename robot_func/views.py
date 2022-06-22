from loguru import logger
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from retiree_care_project import connections
from retiree_care_project import settings
from .models import RobotsCode
from .forms import CodeInput



client = connections.mqtt_connection()
ftp = connections.ftp_connection() 

'''Authentication part'''
def signupuser(request):
    if request.method == "GET":
        return render(request, "robot_func/signupuser.html", {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('account')                             
            except IntegrityError:
                return render(request, 'robot_func/signupuser.html', {'form':UserCreationForm(), 'error':'Такой пользователь уже зарегистрирован!'})
        else:
            return render(request, 'robot_func/signupuser.html', {'form':UserCreationForm(), 'error':'Пароли не совпадают!'})

def loginuser(request):
    if request.method == "GET":
        return render(request, "robot_func/loginuser.html", {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'robot_func/loginuser.html', {'form' : AuthenticationForm(), 'error':'Такого пользователя не существует!'})
        else:
            login(request, user)
            return redirect('account')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    if request.method == "GET":
        return redirect('home')


'''Functionality part'''
@login_required
def robot_control(request):
    form = CodeInput(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        print(f"code: {code}")
        if code == "010122":
            return render(request, 'robot_func/robot_functions.html')
        else:
            return render(request, 'robot_func/personal_account.html', {"form":CodeInput, "error":"У нас нет такого кода в базе. Возможно вы неправильно ввели код."})
    else:
        if 'check_position' in request.GET:
            client.publish("tomatocoder/go", "go") 
            return render(request, 'robot_func/robot_functions.html', {'message':'Отлчино! Робот выехал. Подождите пару минут и вы сможете посмотреть отчёт! '})
        if 'get_report' in request.GET:
            ftp.downloadFile("frame.jpg", "/Users/tomatocoder/Desktop/retiree_care_project/robot_func/static/robot_func/frame.jpg")
            ftp.downloadFile("output.wav", "/Users/tomatocoder/Desktop/retiree_care_project/robot_func/static/robot_func/output.wav") 
            return render(request, 'robot_func/robot_functions.html', {'message':'Отчёт готов!'})
        if request.method == 'GET':
            return render(request, 'robot_func/robot_functions.html')


@login_required
def personal_account(request):
    return render(request, 'robot_func/personal_account.html', {"form":CodeInput})

def home(request):
    return render(request, 'robot_func/home.html')

def details(request):
    return render(request, 'robot_func/details.html')