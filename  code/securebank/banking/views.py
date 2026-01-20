from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Account, Transaction
import random
from decimal import Decimal


def login_view(request):
    """Simple login/register page"""
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('banking:dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        
        elif 'register' in request.POST:
            # Register - FLAW 1: Weak password validation
            username = request.POST.get('reg_username')
            password = request.POST.get('reg_password')
            
            # VULNERABLE: Very weak password requirements
            if len(password) < 2:  # FIX: Change to len(password) < 8 and add complexity checks
                messages.error(request, 'Password too short')
                return render(request, 'banking/login.html')
            # FIX: Add password strength validation:
            # import re
            # if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            #     messages.error(request, 'Password must contain uppercase, lowercase, and number')
            #     return render(request, 'banking/login.html')
            
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username exists')
                else:
                    user = User.objects.create_user(username=username, password=password)
                    account_number = f"IBAN{random.randint(1000, 9999)}"
                    Account.objects.create(owner=user, account_number=account_number)
                    login(request, user)
                    return redirect('banking:dashboard')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'banking/login.html')
