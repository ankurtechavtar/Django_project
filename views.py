import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import OTP, CustomUser
from .forms import EmailForm, OTPForm

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')
    
def service(request):
    return render(request,'service.html')

def send_otp_email(email):
    otp = str(random.randint(100000, 999999))
    OTP.objects.create(email=email, otp=otp)
    send_mail(
        "Your OTP Code",
        f"Your OTP code is {otp}.",
        "parasharankurdbg@gmail.com", 
        [email],
    )

def login_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user, created = CustomUser.objects.get_or_create(email=email)
            send_otp_email(email)
            request.session['email'] = email
            return redirect('verify_otp')
    else:
        form = EmailForm()
 
    return render(request, 'login.html', {'form': form})

def verify_otp_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if OTP.objects.filter(email=email, otp=otp).exists():
                user = CustomUser.objects.get(email=email)
                login(request, user)
                OTP.objects.filter(email=email).delete()  
                return redirect('home')  
            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})
