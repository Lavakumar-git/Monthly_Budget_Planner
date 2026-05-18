from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Income, Expense


# REGISTER FORM

class RegisterForm(UserCreationForm):

    email = forms.EmailField(

        widget=forms.EmailInput(attrs={

            'class': 'form-control',

            'placeholder': 'Enter email'

        })
    )

    class Meta:

        model = User

        fields = [

            'username',

            'email',

            'password1',

            'password2'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # USERNAME

        self.fields['username'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Enter username'
        })

        # PASSWORD 1

        self.fields['password1'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Enter password'
        })

        # PASSWORD 2

        self.fields['password2'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Confirm password'
        })


# INCOME FORM

class IncomeForm(forms.ModelForm):

    class Meta:

        model = Income

        fields = [

            'source',

            'amount'
        ]

        widgets = {

            'source': forms.TextInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter income source'
            }),

            'amount': forms.NumberInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter amount'
            }),
        }


# EXPENSE FORM

class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        fields = [

            'category',

            'description',

            'amount'
        ]

        widgets = {

            'category': forms.Select(attrs={

                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={

                'class': 'form-control',

                'placeholder': 'Enter description'
            }),

            'amount': forms.NumberInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter amount'
            }),
        }