from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.source


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Shopping', 'Shopping'),
        ('Travel', 'Travel'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Healthcare', 'Healthcare'),
        ('Savings', 'Savings'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category
    
    from django.db import models

from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    security_question = models.CharField(max_length=20)
    security_answer = models.CharField(max_length=200)

    def __str__(self):

        return self.user.username
    