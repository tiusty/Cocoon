from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username',
            }),
    )
    password = forms.CharField(
        label="Password", max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'placeholder': 'Password',
                'type': 'password',
            }),
    )
    remember = forms.ChoiceField(
        label="Remember",
        widget=forms.CheckboxInput(),
        required=False,
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Usernames",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username',
            }),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1','password2', 'email']

