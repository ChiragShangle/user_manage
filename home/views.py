from home.models import Details
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *


def dash(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    return render(request, 'dashboard.html', {"details": details})


def index(request):
    return render(request, 'home.html')


def home(request):
    return render(request, "home.html")


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('/dash')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dash')
            else:
                messages.error(request, 'INVALID EMAIL OR PASSWORD')
                return redirect('/login')
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        date = request.POST.get('date')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        if password != cpassword:
            mess = {'abcd': 'BOTH PASSWORDS MUST BE SAME!'}
            return render(request, 'register.html', mess)

        if User.objects.filter(username=email).exists():
            mess = {'abcd': 'Email ALREADY EXIST!'}
            return render(request, 'login.html', mess)
        else:
            obj = Details(email=email, name=name, password=password,
                          date=date, address=address, phone=phone)
            obj.save()
            user = User.objects.create_user(username=email, password=password)
            user.save()
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')
            else:
                return redirect('login')
    return render(request, 'register.html')


def forgot(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    for det in details:
        name = det.name
        date = det.date
        phone = det.phone
        address = det.address
    if request.method == 'POST':
        email = request.POST.get('email')
        fpassword = request.POST.get('fpassword')
        cfpassword = request.POST.get('cfpassword')
        if fpassword != cfpassword:
            mess2 = {'abcd': 'BOTH PASSWORDS MUST BE SAME!'}
            return render(request, 'forgot.html', mess2)

        obj = Details(email=email, name=name, date=date,
                      address=address, phone=phone, password=fpassword)
        obj.save()

    return render(request, 'forgot.html')


def edit(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    for det in details:
        password = det.password
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        obj = Details(email=username, name=name, password=password,
                      date=date, address=address, phone=phone)
        obj.save()
        return redirect('/dash')
    return render(request, "edit.html")


def change(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    for det in details:
        name = det.name
        date = det.date
        phone = det.phone
        address = det.address
        password = det.password
    if request.method == 'POST':
        opassword = request.POST.get('opassword')
        npassword = request.POST.get('npassword')
        cnpassword = request.POST.get('cnpassword')
        if npassword != cnpassword:
            mess2 = {'abcd': 'BOTH PASSWORDS MUST BE SAME!'}
            return render(request, 'change.html', mess2)
        elif opassword != password:
            mess1 = {'efgh': 'ENTER CORRECT OLD PASSWORD!'}
            return render(request, 'change.html', mess1)

        obj = Details(email=username, name=name, date=date,
                      address=address, phone=phone, password=npassword)
        obj.save()
        user = User(username=username, password=npassword)
        user.save()

        return redirect('/dash')
    return render(request, "change.html")


def logout_user(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/home')
