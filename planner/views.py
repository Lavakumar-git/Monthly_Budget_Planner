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
from .forms import ForgotPasswordForm
from .models import UserProfile
from django.contrib.auth.models import User


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
    if total_income == 0 and total_expense == 0:

        suggestions.append("You haven't added any income or expenses yet. Start by adding your income and expenses to get insights and suggestions.")

    elif balance >=0 and balance< 3000:

        suggestions.append(" Your balance is very low. Try reducing unnecessary spending and try to gain more income.")
     
    elif balance >= 3000 and balance < 5000:

        suggestions.append("Your balance is decresing. Consider reviewing your expenses")
  
    elif balance >= 5000 and balance < 10000:

        suggestions.append(" Your balance is decent, but there's room for improvement. Consider setting a budget and tracking your expenses more closely.")
     
    elif balance >= 10000 and balance < 20000:

        suggestions.append("Great job! You have a healthy balance. Consider investing or saving more.")

    elif balance >= 20000 and balance < 30000:
        suggestions.append("You're doing great! Consider exploring investment opportunities to grow your wealth.")

    elif balance >= 30000:
        suggestions.append("Excellent! You have a very healthy balance. Consider exploring investment opportunities or saving for long-term goals.")

    elif total_expense > total_income:

        suggestions.append( "⚠ Your expenses are higher than your income, try to reduce your expenses." )



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


from rest_framework import generics

from .serializers import (
    IncomeSerializer,
    ExpenseSerializer
)

from .models import (
    Income,
    Expense
)

# =========================
# INCOME APIs
# =========================

class IncomeListCreateAPIView(

    generics.ListCreateAPIView
):

    queryset = Income.objects.all()

    serializer_class = IncomeSerializer


class IncomeDetailAPIView(

    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Income.objects.all()

    serializer_class = IncomeSerializer


# =========================
# EXPENSE APIs
# =========================

class ExpenseListCreateAPIView(

    generics.ListCreateAPIView
):

    queryset = Expense.objects.all()

    serializer_class = ExpenseSerializer


class ExpenseDetailAPIView(

    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Expense.objects.all()

    serializer_class = ExpenseSerializer

    from django.shortcuts import render, redirect
from .forms import RegisterForm


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegisterForm()

    return render(request, 'register.html', {

        'form': form

    })





def forgot_password(request):

    question = None

    message = None

    if request.method == 'POST':

        form = ForgotPasswordForm(request.POST)

        username = request.POST.get('username')

        try:

            user = User.objects.get(username=username)

            profile = UserProfile.objects.get(user=user)

            question = profile.security_question

            answer = request.POST.get('security_answer')

            new_password = request.POST.get('new_password')

            if answer and new_password:

                if profile.security_answer.lower() == answer.lower():

                    user.set_password(new_password)

                    user.save()

                    message = "Password updated successfully"

                else:

                    message = "Wrong security answer"

        except User.DoesNotExist:

            message = "User not found"

    else:

        form = ForgotPasswordForm()

    return render(

        request,

        'forgot_password.html',

        {

            'form': form,

            'question': question,

            'message': message
        }
    )