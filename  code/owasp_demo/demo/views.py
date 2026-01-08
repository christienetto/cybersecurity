from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse

# Create your views here.

# NOTE: You need demo/templates/register.html and demo/templates/login.html for the registration and login forms to work.
# Registration view with OWASP flaw: weak password allowed unless check is uncommented
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Uncomment the following lines to enforce strong password (OWASP fix)
        # if len(password) < 8:
        #     return HttpResponse('Password too short! Must be at least 8 characters.', status=400)
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse('User created successfully!')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=400)
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse('Logged in successfully!')
        else:
            return HttpResponse('Invalid credentials', status=401)
    return render(request, 'login.html')
