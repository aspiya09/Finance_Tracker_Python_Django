from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404


def index(request):
    transactions = Transaction.objects.order_by('-date')
    form = TransactionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expense

    return render(request, 'tracker/index.html', {
        'form': form,
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance
    })

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(request.POST or None, instance=transaction)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')

    transactions = Transaction.objects.order_by('-date')
    income = sum(t.amount for t in transactions if t.type == 'income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expense

    return render(request, 'tracker/index.html', {
        'form': form,
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
        'edit_mode': True,
        'edit_id': pk,
    })


def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('home')
