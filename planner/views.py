from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import RegisterForm, IncomeForm, ExpenseForm
from .models import Income, Expense
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Expense
import json
from django.db.models import Sum


def home(request):
    return render(request,'home.html')

@login_required
def profile(request):

    return render(
        request,
        'profile.html'
    )


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    income_form = IncomeForm()

    expense_form = ExpenseForm()

    incomes = Income.objects.filter(user=request.user)

    expenses = Expense.objects.filter(user=request.user)

    total_income = incomes.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_expense = expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    balance = total_income - total_expense

    # AI SUGGESTIONS

    suggestions = []

    if total_expense > total_income:

        suggestions.append(
            "⚠ Your expenses are higher than your income."
        )

    if balance < 1000:

        suggestions.append(
            " Your balance is very low. Try reducing unnecessary spending."
        )

    shopping_total = expenses.filter(
        category='Shopping'
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    if shopping_total > total_income * 0.3:

        suggestions.append(
            " Shopping expenses are too high this month."
        )

    food_total = expenses.filter(
        category='Food'
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    if food_total > total_income * 0.2:

        suggestions.append(
            " Food expenses are higher than recommended."
        )

    if total_income > total_expense:

        suggestions.append(
            " Excellent budgeting! Your savings ratio looks healthy."
        )

    context = {

        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'suggestions': suggestions,
        'incomes': incomes,
        'expenses': expenses,
        'income_form': income_form,
        'expense_form': expense_form,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


@login_required
def add_income(request):

    if request.method == 'POST':
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})

@login_required
def profile(request):

    return render(
        request,
        'profile.html'
    )

@login_required
def history(request):

    incomes = Income.objects.filter(
        user=request.user
    )

    expenses = Expense.objects.filter(
        user=request.user
    )

    context = {
        'incomes': incomes,
        'expenses': expenses,
    }

    return render(
        request,
        'history.html',
        context
    )


@login_required
def add_expense(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request,'add_expense.html', {'form': form})

# EDIT INCOME

@login_required
def edit_income(request, id):

    income = get_object_or_404(
        Income,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = IncomeForm(request.POST, instance=income)

        if form.is_valid():
            form.save()
            return redirect('history')

    else:
        form = IncomeForm(instance=income)

    return render(
        request,'add_income.html',{'form': form})


# DELETE INCOME

@login_required
def delete_income(request, id):

    income = get_object_or_404(
        Income,
        id=id,
        user=request.user
    )

    income.delete()

    return redirect('history')


# EDIT EXPENSE

@login_required
def edit_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()
            return redirect('history')

    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        'add_expense.html',
        {'form': form}
    )


# DELETE EXPENSE

@login_required
def delete_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    expense.delete()

    return redirect('history')

from django.db.models import Sum


@login_required
def history(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by('-date')

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')

    total_income = incomes.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_expense = expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    context = {

        'incomes': incomes,

        'expenses': expenses,

        'total_income': total_income,

        'total_expense': total_expense,
    }

    return render(
        request,
        'history.html',
        context
    )