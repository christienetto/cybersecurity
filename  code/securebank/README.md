# Secure Banking App, Intro to Cybersecurity Project I

A vulnerable Django banking application with 5 critical security flaws from the OWASP Top 10 (2021) list.

## Code Structure

- `banking/views.py` - Main application logic with all vulnerabilities
- `banking/models.py` - Simple Account and Transaction models
- `banking/templates/` - Minimal HTML templates
- `banking/urls.py` - URL routing
- `banking/screenshots/BEFORE` - before the fix for the flaw
- `banking/screenshots/AFTER` - after the fix flaw

Note! 
I have used the BEFORE directory to showcase the flaw, for example flaw-1-before-1.png , to show how to reproduce the flaw right before the actual flaw execution and  flaw-1-after-1.png is what the flaw should show afterwards. The AFTER directory in screenshots are what the flaw looks like after the fix, I apologize for the using the same naming convention (flaw-1-after-1.png). I wanted the user to see how exctly to reproduce this flaw by looking at the screenshots.  

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Quick Start
```bash
git clone https://github.com/christienetto/cybersecurity
cd securebank
python -m venv venv
source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

Access at: `http://localhost:8000/`

## Security Vulnerabilities

### FLAW 1: Broken Authentication (A07:2021)
**Location:** `banking/views.py` lines 18-22  
**Issue:** Password only requires 2 characters minimum  
**Exploit:** Register with password "12"  
**Fix:** Commented code has proper password complexity validation (8+ chars, uppercase, lowercase, numbers)

### FLAW 2: Injection - SQL Injection (A03:2021)
**Location:** `banking/views.py` lines 121-138  
**Issue:** Raw SQL query with unsanitized user input in LIKE clause  
**Exploit:** Search for: `' OR '1'='1' --` to retrieve all transactions instead of just matching ones  
**Alternative Exploit:** `' UNION SELECT name FROM sqlite_master WHERE type='table' AND '1'='1` to enumerate database tables  
**Note:** DROP TABLE won't work due to SQLite's single-statement execution limit and cursor constraints  
**Fix:** Commented code shows Django ORM usage instead of raw SQL

### FLAW 3: Security Misconfiguration (A05:2021)
**Location:** `banking/views.py` lines 97-104  
**Issue:** Debug information exposed via URL parameter (scroll a little bit down) 
**Exploit:** Visit `http://localhost:8000/?debug=1` to see sensitive data**Fix:** Commented code shows that only admin can access and debug 
**Fix:** Redirects to the login page

### FLAW 4: Broken Access Control (A01:2021)
**Location:** `banking/views.py` lines 45-52 and 65-72  
**Issue:** No ownership verification, users can modify any account  
**Exploit:** Add money to any IBAN or delete any account  
**Fix:** Commented code shows proper ownership verification before operations, would not allow you to add to another's account.

### FLAW 5: Cross-Site Request Forgery (CSRF)
**Location:** `banking/views.py` lines 75-82  
**Issue:** Critical operations via GET requests without CSRF protection  
**Exploit:** Malicious links can create accounts: `http://localhost:8000/?create=1&iban=HACK1234&password=test`  
**Fix:** Commented code shows POST requests with CSRF token validation

## How to Test Vulnerabilities

1. **Weak Passwords:** Register with username "test" and password "12"
2. **SQL Injection:** Search for `' OR '1'='1' --` in the search transactions area to retrieve all transactions instead of just matching ones
3. **Data Exposure:** Add `?debug=1` to any URL to see sensitive information, scroll a little bit down and some debug data should be shown
4. **Access Control:** Try adding money to random IBAN numbers or deleting accounts you don't own, perhaps first register for two users and check if you can delete the other ones account
5. **CSRF:** Create malicious links that perform actions when clicked by logged-in users, like go to `http://localhost:8000/?create=1&iban=HACK1234&password=test`

## Screenshots

Screenshots stored in `screenshots/` dir.





