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
import random


@login_required(login_url="/log")
def dash(request):
    username = request.user.username
    details = Details.objects.filter(email=username)
    info = Addinfo.objects.filter(email=username)
    return render(request, 'dashboard.html', {"details": details, "info": info})


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
            otp = str(random.randint(100000, 999999))
            profile_obj = Profile.objects.create(
                user=user, otp=otp)
            profile_obj.save()
            send_otp_mail(email, otp)
            if user is not None:
                login(request, user)
                return redirect('/otp')
            else:
                return redirect('login')
    return render(request, 'register.html')


def send_otp_mail(email, otp):
    subject = "Your account needs to be verified"
    message = f"Otp to register is {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)


def reotp(request):
    messages.info(
        request, 'OTP HAS BEEN RESEND ON YOUR MAIL')
    username = request.user.username
    otp = str(random.randint(100000, 999999))
    user_obj = User.objects.get(username=username)
    profile_obj = Profile.objects.filter(user=user_obj).first()
    if profile_obj.is_verified == True:
        messages.info(
            request, 'MAIL ALREADY VERIFIED')
        return redirect('/log')

    if request.method == 'POST':
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.filter(user=user_obj).first()
        otp = request.POST.get('otp')
        if profile_obj.otp == otp:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.info(
                request, 'EMAIL HAS BEEN VERIFIED PLEASE LOGIN')
            return redirect('/log')
        else:
            messages.info(
                request, 'INVALID OTP')
            return render(request, 'otp.html')
    profile_obj.otp = otp
    profile_obj.save()
    email = username
    send_otp_mail(email, otp)
    return render(request, 'otp.html')


def otp(request):
    username = request.user.username
    user_obj = User.objects.get(username=username)
    profile_obj = Profile.objects.filter(user=user_obj).first()
    if profile_obj.is_verified == True:
        messages.info(
            request, 'MAIL ALREADY VERIFIED')
        return redirect('/log')

    if request.method == 'POST':
        messages.info(
            request, 'ENTER OTP SEND ON YOUR MAIL')
        otp = request.POST.get('otp')
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if profile_obj.otp == otp:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.info(
                request, 'EMAIL HAS BEEN VERIFIED PLEASE LOGIN')
            return redirect('/log')
        else:
            messages.info(
                request, 'INVALID OTP')
            return render(request, 'otp.html')
    return render(request, 'otp.html')


def forgot(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')

            if not User.objects.filter(username=email).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forgot')
            user_obj = User.objects.get(username=email)
            otp = str(random.randint(100000, 999999))
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.otp = otp
            profile_obj.save()
            send_forget_password_mail(email, otp)
            return redirect(f'/fotp/{email}')
    except Exception as e:
        print(e)
    return render(request, 'forgot.html')


def fotp(request, email):

    messages.info(
        request, 'ENTER OTP SEND ON YOUR MAIL')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_obj = User.objects.filter(username=email).first()
        profile_obj = Profile.objects.filter(user=user_obj).first()
        if profile_obj.otp == otp:
            messages.info(
                request, 'EMAIL HAS BEEN VERIFIED')
            return redirect(f'/change-password/{otp}')
        else:
            messages.info(
                request, 'INVALID OTP')
            return render(request, 'otp.html')
    return render(request, 'otp.html')


def send_forget_password_mail(email, otp):
    subject = "Yout account neeeds to be verrified"
    message = f"Otp to change your password is {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = {email}
    send_mail(subject, message, email_from, recipient_list)


def ChangePassword(request, otp):
    context = {}
    profile_obj = Profile.objects.filter(
        otp=otp).first()
    context = {'user_id': profile_obj.user.id}
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('reconfirm_password')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.success(request, 'No USER IS FOUND')
            return redirect(f'/change-password/{otp}')

        if new_password != confirm_password:
            messages.success(request, 'BOTH PASSWORD MUST BE EQUAL')
            return redirect(f'/change-password/{otp}')

        user_obj = User.objects.get(id=user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        username = user_obj.username
        profile_obj = Details.objects.get(email=username)
        profile_obj.password = new_password
        profile_obj.save()
        messages.success(request, 'PASSWORD CHANGED SUCCESSFULLY')

        return redirect('/log')

    return render(request, 'change-password.html', context)


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
        messages.info(
            request, 'YOUR DETAILS HAVE BEEN EDITED SUCCESSFULLY')

        return redirect('/dash')
    return render(request, "edit.html", {"details": details})


@login_required(login_url="/log")
def info(request):
    username = request.user.username

    if Addinfo.objects.filter(email=username).exists() and Addinfo.objects.filter(is_submitted=0):
        return redirect('/draft')
    elif Addinfo.objects.filter(is_submitted=1) and Addinfo.objects.filter(email=username).exists():
        return redirect('/submit')

    elif request.method == 'POST' and 'saveasdraft' in request.POST:
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        city = request.POST.get('city')
        officeno = request.POST.get('officeno')

        obj = Addinfo(email=username, designation=designation,
                      address=address, city=city, pin=pin, officeno=officeno, is_submitted=False)
        obj.save()
        messages.info(
            request, 'DRAFT SAVED')
        return redirect('/dash')
    elif request.method == 'POST' and 'submitbtn' in request.POST:
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        city = request.POST.get('city')
        officeno = request.POST.get('officeno')
        obj = Addinfo(email=username, designation=designation,
                      address=address, city=city, pin=pin, officeno=officeno, is_submitted=True)
        obj.save()

        messages.info(
            request, 'INFORMATION SUBMITTED')
        return redirect('/dash')
    return render(request, 'add_info.html')


@login_required(login_url="/log")
def draft(request):
    username = request.user.username
    info = Addinfo.objects.filter(email=username)
    if request.method == 'POST' and 'savedraft' in request.POST:
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        city = request.POST.get('city')
        officeno = request.POST.get('officeno')
        obj = Addinfo(email=username, designation=designation,
                      address=address, city=city, pin=pin, officeno=officeno, is_submitted=False)
        obj.save()
        messages.info(
            request, 'DRAFT SAVED')
        return redirect('/dash')
    elif request.method == 'POST' and 'submitbt' in request.POST:
        designation = request.POST.get('designation')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        city = request.POST.get('city')
        officeno = request.POST.get('officeno')
        obj = Addinfo(email=username, designation=designation,
                      address=address, city=city, pin=pin, officeno=officeno, is_submitted=True)
        obj.save()
        messages.info(
            request, 'INFORMATION SUBMITTED')
        return redirect('/dash')

    return render(request, 'draft.html', {"info": info})


@login_required(login_url="/log")
def submit(request):
    username = request.user.username
    info = Addinfo.objects.filter(email=username)
    for inf in info:
        designation = inf.designation
        address = inf.address
        city = inf.city
        pin = inf.pin
        officeno = inf.officeno
        obj = Addinfo(email=username, designation=designation,
                      address=address, city=city, pin=pin, officeno=officeno, is_submitted=True)
        obj.save()
    return render(request, 'save.html', {"info": info})


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
            request, 'YOUR PASSWORD HAS BEEN CHANGED SUCCESSFULLY, PLEASE LOGIN AGAIN')

        return render(request, "success.html")
    return render(request, "change.html")


def logout_user(request):
    if request.method == 'GET':
        logout(request)

        messages.info(
            request, 'Logged Out')
        return redirect('/home')


def token_send(request):
    return render(request, 'token_send.html')
