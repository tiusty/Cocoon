from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


####################################################
# Notes: The username is set as the current email address
#
#
####################################################

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        label="Email",
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username',
            }),
    )
    password = forms.CharField(
        required=False,
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

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )
    first_name = forms.CharField(
        required=True,
        label="First name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'first name',
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'last name',
            }
        )
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1','password2']

