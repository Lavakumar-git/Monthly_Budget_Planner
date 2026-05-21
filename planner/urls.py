from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
       path('',views.home,name='home'),
       path('register/',views.register_view,name='register'),
       path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
       path('logout/',auth_views.LogoutView.as_view(),name='logout'),
       path('dashboard/',views.dashboard,name='dashboard'),
       path('add-income/',views.add_income,name='add_income'),
       path('edit-income/<int:id>/',views.edit_income,name='edit_income'),
       path('delete-income/<int:id>/',views.delete_income,name='delete_income'),
       path('add-expense/',views.add_expense,name='add_expense'),
       path('edit-expense/<int:id>/',views.edit_expense,name='edit_expense'),
       path('delete-expense/<int:id>/',views.delete_expense,name='delete_expense'),
       path('profile/',views.profile,name='profile'),path('history/',views.history,name='history'),
       path('api/income/',IncomeListCreateAPIView.as_view(),name='income_api'),
       path('api/income/<int:pk>/',IncomeDetailAPIView.as_view(),name='income_detail_api'),
       path('api/expense/',ExpenseListCreateAPIView.as_view(),name='expense_api'),
       path('api/expense/<int:pk>/',ExpenseDetailAPIView.as_view(),name='expense_detail_api'),


path(

    'forgot-password/',

    views.forgot_password,

    name='forgot_password'
),
]
