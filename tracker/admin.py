from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'type', 'date')

admin.site.register(Transaction, TransactionAdmin)
