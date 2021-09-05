from django.contrib import auth
from home.models import Details
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url="/log")
def dash(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    return render(request, 'dashboard.html', {"details": details})


def index(request):
    return render(request, 'home.html')


def home(request):
    return render(request, "home.html")


def loginuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email).first()
        profile_obj = Profile.objects.filter(user=user_obj).first()
        user = authenticate(username=email, password=password)
        if user_obj is None:
            messages.error(
                request, 'USER NOT FOUND')
            return redirect('/log')

        elif not profile_obj.is_verified:
            messages.error(
                request, 'PROFILE NOT VERIFIED PLEASE CHECK MAIL')

        elif user is not None:
            login(request, user)
            return redirect('/dash')
        else:
            messages.error(request, 'INVALID EMAIL OR PASSWORD')
            return redirect('/log')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        date = request.POST.get('date')
        phone = request.POST.get('phone')
        if password != cpassword:
            messages.info(
                request, 'BOTH PASSWORD! MUST BE SAME')
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists():
            messages.info(
                request, 'EMAIL ALREADY EXISTS')
            return render(request, 'login.html')
        else:
            obj = Details(email=email, name=name, password=password,
                          dob=date,  phone=phone)
            obj.save()
            user = User.objects.create_user(username=email, password=password)
            user.save()
            user = authenticate(username=email, password=password)
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=user, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)

            if user is not None:
                login(request, user)
                return redirect('/token')
            else:
                return redirect('login')
    return render(request, 'register.html')


def verify(request, auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.info(
                request, 'EMAIL IS ALREADY VERIFIED')
            return redirect('/log')
        profile_obj.is_verified = True
        profile_obj.save()
        messages.info(
            request, 'EMAIL HAS BEEN VERIFIED')
        return redirect('/log')


def forgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')

            if not User.objects.filter(username=email).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forgot')

            user_obj = User.objects.get(username=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(email, token)
            return redirect('/token')

    except Exception as e:
        print(e)
    return render(request, 'forgot.html')


@login_required(login_url="/log")
def edit(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    for det in details:
        password = det.password
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        phone = request.POST.get('phone')
        obj = Details(email=username, name=name, password=password,
                      dob=date,  phone=phone)
        obj.save()
        return redirect('/dash')
    return render(request, "edit.html", {"details": details})


@login_required(login_url="/log")
def change(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    for det in details:
        name = det.name
        date = det.dob
        phone = det.phone
        password = det.password
    if request.method == 'POST':
        opassword = request.POST.get('opassword')
        npassword = request.POST.get('npassword')
        cnpassword = request.POST.get('cnpassword')
        if opassword != password:
            messages.info(
                request, 'ENTER CORRECT OLD PASSWORD')
            return render(request, 'change.html')
        elif npassword != cnpassword:
            messages.info(
                request, 'BOTH PASSWORD! MUST BE SAME')
            return render(request, 'change.html')
        elif npassword == password:
            messages.info(
                request, 'OLD PASSWORD AND NEW PASSWORD ARE SAME')
            return render(request, 'change.html')
        obj = Details(email=username, name=name, dob=date,
                      phone=phone, password=npassword)
        obj.save()
        u = User.objects.get(username=username)
        u.set_password(npassword)
        u.save()
        messages.info(
            request, 'Your password has been changed successfully! Please Login Again')
        return redirect("/logout")
    return render(request, "change.html")


def logout_user(request):
    if request.method == 'GET':
        logout(request)

        messages.info(
            request, 'Logged Out')
        return redirect('/home')


def ChangePassword(request, token):
    context = {}
    profile_obj = Profile.objects.filter(
        forget_password_token=token).first()
    context = {'user_id': profile_obj.user.id}
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('reconfirm_password')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.success(request, 'No USER IS FOUND')
            return redirect(f'/change-password/{token}')

        if new_password != confirm_password:
            messages.success(request, 'BOTH PASSWORD MUST BE EQUAL')
            return redirect(f'/change-password/{token}')

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('/log')

    return render(request, 'change-password.html', context)


def token_send(request):
    return render(request, 'token_send.html')


def send_mail_after_registration(email, token):
    subject = "Yout account neeeds to be verrified"
    message = f"Click the link to verify your account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)


def send_forget_password_mail(email, token):
    subject = "Yout account neeeds to be verrified"
    message = f"Click the link to change your password http://127.0.0.1:8000/change-password/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)
