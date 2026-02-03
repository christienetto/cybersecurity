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


@login_required
def dashboard(request):
    """Main banking page with all functionality"""
    accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'GET':
        if 'add' in request.GET:
            # Add money - FLAW 5: No access control
            to_account = request.GET.get('to')
            amount = request.GET.get('amount')
            if to_account and amount:
                try:
                    account = Account.objects.get(account_number=to_account)
                    # VULNERABLE: Can add money to any account
                    # FIX: Verify account ownership:
                    # if account.owner != request.user:
                    #     messages.error(request, 'Access denied: You can only modify your own accounts')
                    #     return render(request, 'banking/dashboard.html', {'accounts': accounts})
                    account.balance += Decimal(amount)
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=Decimal(amount),
                        description=f"Money added by {request.user.username}"
                    )
                    # FIX: Add security logging:
                    # logger.warning(f'SECURITY: Money added ${amount} to {to_account} by {request.user.username} from IP {request.META.get("REMOTE_ADDR")}')
                    messages.success(request, f'Added ${amount} to {to_account}')
                except:
                    messages.error(request, 'Account not found')
        
        elif 'delete' in request.GET:
            # Delete account - FLAW 5: No access control
            iban = request.GET.get('iban')
            if iban:
                try:
                    account = Account.objects.get(account_number=iban)
                    # VULNERABLE: Can delete any account
                    # FIX: Verify account ownership:
                    # if account.owner != request.user:
                    #     messages.error(request, 'Access denied: You can only delete your own accounts')
                    #     return render(request, 'banking/dashboard.html', {'accounts': accounts})
                    account.delete()
                    # FIX: Add security logging:
                    # logger.warning(f'SECURITY: Account {iban} deleted by {request.user.username} from IP {request.META.get("REMOTE_ADDR")}')
                    messages.success(request, f'Deleted account {iban}')
                except:
                    messages.error(request, 'Account not found')
        
        elif 'create' in request.GET:
            # Create account - FLAW 6: CSRF via GET
            iban = request.GET.get('iban')
            password = request.GET.get('password')
            if iban and password:
                # VULNERABLE: Creating accounts via GET request
                # FIX: Use POST request with CSRF token:
                # if request.method == 'POST':
                #     # Django automatically validates CSRF token for POST requests
                #     Account.objects.create(owner=request.user, account_number=iban)
                try:
                    Account.objects.create(owner=request.user, account_number=iban)
                    messages.success(request, f'Created account {iban}')
                except:
                    messages.error(request, 'Could not create account')
        
        elif 'search' in request.GET:
            # Search - FLAW 2: SQL Injection
            query = request.GET.get('q', '')
            if query:
                # VULNERABLE: Raw SQL injection
                sql = f"SELECT * FROM banking_transaction WHERE description LIKE '%{query}%'"
                # FIX: Use parameterized queries or Django ORM:
                # transactions = Transaction.objects.filter(description__icontains=query, account__owner=request.user)
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                    messages.success(request, f'Found {len(results)} transactions')
                except Exception as e:
                    messages.error(request, f'Database error: {str(e)}')
                    # FIX: Don't expose database errors to users:
                    # logger.error(f'Database error: {str(e)}')
                    # messages.error(request, 'Search temporarily unavailable')
    
    # FLAW 3: Debug info exposure
    debug_info = None
    if request.GET.get('debug'):
        debug_info = {  # FIX: Remove debug info entirely or restrict to admin users only
            'user_id': request.user.id,
            'session': request.session.session_key,
            'secret': 'sk_live_12345',  # FIX: Never expose API keys or secrets
            'db_pass': 'admin123'  # FIX: Never expose database credentials
        }
        # FIX: Proper implementation:
        # if request.user.is_superuser:
        #     debug_info = {'queries': len(connection.queries)}
        # else:
        #     debug_info = None
    
    return render(request, 'banking/dashboard.html', {
        'accounts': accounts,
        'debug_info': debug_info
    })
