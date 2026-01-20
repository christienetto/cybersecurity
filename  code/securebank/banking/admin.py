from django.contrib import admin
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'owner', 'balance', 'created_at']
    search_fields = ['account_number', 'owner__username']
    readonly_fields = ['created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'description', 'created_at']
    search_fields = ['description', 'account__account_number']
    readonly_fields = ['created_at']