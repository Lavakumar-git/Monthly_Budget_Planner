from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Income, Expense


# =========================
# REGISTER FORM
# =========================

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

        # USERNAME FIELD

        self.fields['username'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Enter username'
        })

        # PASSWORD 1 FIELD

        self.fields['password1'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Enter password'
        })

        # PASSWORD 2 FIELD

        self.fields['password2'].widget.attrs.update({

            'class': 'form-control',

            'placeholder': 'Confirm password'
        })

    # =========================
    # USERNAME VALIDATION
    # =========================

    def clean_username(self):

        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError(

                "Username already exists"

            )

        return username

    # =========================
    # EMAIL VALIDATION
    # =========================

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(

                "Email already registered"

            )

        return email


# =========================
# INCOME FORM
# =========================

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


# =========================
# EXPENSE FORM
# =========================

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

                'placeholder': 'Enter description',

                'rows': 3
            }),

            'amount': forms.NumberInput(attrs={

                'class': 'form-control',

                'placeholder': 'Enter amount'
            }),
        }