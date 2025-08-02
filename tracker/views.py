from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Finance
from .forms import FinanceForm
import json


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
    filter_type = request.GET.get('type', 'all')
    filter_category = request.GET.get('category', 'all')

    finances = Finance.objects.filter(user=request.user)

    if filter_type != 'all':
        finances = finances.filter(type=filter_type)

    if filter_category != 'all':
        finances = finances.filter(category=filter_category)

    finances = finances.order_by('-date')
    
    form = FinanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('dashboard')

    income = sum(f.amount for f in finances if f.type == 'income')
    expense = sum(f.amount for f in finances if f.type == 'expense')
    balance = income - expense

    context = {
        'form': form,
        'finances': finances,
        'income': income,
        'expense': expense,
        'balance': balance,
        'filter_type': filter_type,
        'filter_category': filter_category,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_finance(request, id):
    finance = get_object_or_404(Finance, id=id, user=request.user)
    form = FinanceForm(request.POST or None, instance=finance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'tracker/edit_finance.html', {'form': form})

@login_required
def delete_finance(request, id):
    finance = get_object_or_404(Finance, id=id, user=request.user)
    finance.delete()
    return redirect('dashboard')
