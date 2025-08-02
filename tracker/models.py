from django.db import models
from django.contrib.auth.models import User


class Finance(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    CATEGORIES = (
        ('salary', 'Salary'),
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('rent', 'Rent'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('other', 'Other'),
    )

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('mobile', 'Mobile Wallet'),
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORIES, default='other')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type}) - ৳{self.amount}"
