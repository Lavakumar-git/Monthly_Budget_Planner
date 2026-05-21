from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Income, Expense, UserProfile


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

    security_question = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Example: Your favorite color?'
        })
    )

    security_answer = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter answer'
        })
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'security_question',
            'security_answer',
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
    # SAVE USER PROFILE
    # =========================

    def save(self, commit=True):

        user = super().save(commit=False)

        if commit:

            user.save()

            UserProfile.objects.create(
                user=user,
                security_question=self.cleaned_data['security_question'],
                security_answer=self.cleaned_data['security_answer']
            )

        return user


# =========================
# FORGOT PASSWORD FORM
# =========================

class ForgotPasswordForm(forms.Form):

    username = forms.CharField(

        widget=forms.TextInput(attrs={

            'class': 'form-control',

            'placeholder': 'Enter username'
        })
    )

    security_answer = forms.CharField(

        required=False,

        widget=forms.TextInput(attrs={

            'class': 'form-control',

            'placeholder': 'Enter security answer'
        })
    )

    new_password = forms.CharField(

        required=False,

        widget=forms.PasswordInput(attrs={

            'class': 'form-control',

            'placeholder': 'Enter new password'
        })
    )

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