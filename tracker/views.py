from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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


def home(request):
    return render(request, 'tracker/home.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'tracker/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'tracker/login.html')

@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')