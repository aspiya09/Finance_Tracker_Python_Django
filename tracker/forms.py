from django import forms
from .models import Finance

class FinanceForm(forms.ModelForm):
    class Meta:
        model = Finance
        fields = ['title', 'amount', 'type']
