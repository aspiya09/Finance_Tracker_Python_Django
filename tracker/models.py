from django.db import models

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.type}): {self.amount}"
