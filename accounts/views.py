from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import RegisterForm
from .models import CustomUser
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://{domain}/accounts/activate/{uid}/{token}/"

            '''subject = 'Welcome to HealthHub!'
            message = f'Hi {user.username},\n\nThank you for creating an account on HealthHub. We are excited to have you!'
            from_email = 'your_email@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)'''

            send_mail("Activate HealthHub", f"Hi {user.username},\n\nThank you for creating an account on HealthHub. We are excited to have you! \n\n Click to activate: {link}",
                      "admin@healthhub.com", [user.email])
            return HttpResponse("Check your email to activate your account.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    return HttpResponse("Activation link invalid or expired.")