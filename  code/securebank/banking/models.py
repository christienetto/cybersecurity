from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('100.00'))
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.account_number} - ${self.balance}"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    recipient_account = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"${self.amount} - {self.description}"