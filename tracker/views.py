from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Finance
from .forms import FinanceForm
import json
import csv
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from collections import defaultdict
import calendar
from django.shortcuts import render
from .utils.gemini_summary import generate_monthly_summary


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
    finances = Finance.objects.filter(user=request.user).order_by('-date')
    form = FinanceForm()

    # Filtering
    type_filter = request.GET.get('type')
    category_filter = request.GET.get('category')
    payment_filter = request.GET.get('payment_type')
    search_query = request.GET.get('q')

    if type_filter:
        finances = finances.filter(type=type_filter)

    if category_filter:
        finances = finances.filter(category=category_filter)

    if payment_filter:
        finances = finances.filter(payment_type=payment_filter)

    if search_query:
        finances = finances.filter(title__icontains=search_query)

    # Totals
    income = sum(f.amount for f in finances if f.type == 'income')
    expense = sum(f.amount for f in finances if f.type == 'expense')
    balance = income - expense

    # Monthly summary
    monthly_summary = (
        finances.annotate(month=TruncMonth('date'))
        .values('month', 'type')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )

    summary_dict = defaultdict(lambda: {'income': 0, 'expense': 0, 'balance': 0})

    for entry in monthly_summary:
        month_str = entry['month'].strftime('%B %Y')
        summary_dict[month_str][entry['type']] = entry['total']

    for month, data in summary_dict.items():
        data['balance'] = data['income'] - data['expense']

    finance_data = [
        {"title": f.title, "amount": f.amount, "type": f.type}
        for f in finances
    ]
    ai_summary = generate_monthly_summary(finance_data)  # text from Gemini API

    context = {
        'form': form,
        'finances': finances,
        'income': income,
        'expense': expense,
        'balance': balance,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'payment_filter': payment_filter,
        'search_query': search_query,
        'summary_dict': dict(summary_dict),
        'summary': ai_summary,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def post_finance(request):
    if request.method == 'POST':
        form = FinanceForm(request.POST)
        if form.is_valid():
            finance = form.save(commit=False)
            finance.user = request.user
            finance.save()
            return redirect('dashboard')
    else:
        form = FinanceForm()
    
    return render(request, 'tracker/post_finance.html', {'form': form})

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

@login_required
def export_csv(request):
    finances = Finance.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="finance_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Type', 'Category', 'Payment Type', 'Date', 'Notes'])

    for f in finances:
        writer.writerow([f.title, f.amount, f.type, f.category, f.payment_type, f.date, f.notes])

    return response


def summary_view(request):
    data = Finance.objects.all()

    # Format data for AI
    finance_data = [
        {"title": item.title, "amount": item.amount, "type": item.type}
        for item in data
    ]

    summary = generate_monthly_summary(finance_data)

    return render(request, "tracker/summary.html", {"summary": summary})