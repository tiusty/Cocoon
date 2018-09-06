from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction
from .models import MyUser, UserProfile
from django import forms

from .constants import HUNTER_CREATION_KEY, BROKER_CREATION_KEY


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
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
        label="Password",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'placeholder': 'Password',
                'type': 'password',
            }),
    )
    remember = forms.BooleanField(
        label="Remember",
        initial=False,
        required=False,
    )


class BaseRegisterForm(UserCreationForm):

    creation_key = forms.CharField(
        required=True,
        label="Please enter the key",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'key',
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label="Email Address",
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
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class ApartmentHunterSignupForm(BaseRegisterForm):

    def is_valid(self):
        valid = super(ApartmentHunterSignupForm, self).is_valid()

        if not valid:
            return valid

        current_form = self.cleaned_data.copy()

        if current_form['creation_key'] != HUNTER_CREATION_KEY:
            self.add_error('creation_key', "Creation Key invaild")
            valid = False

        return valid

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hunter = True
        user.save()
        return user


class BrokerSignupForm(BaseRegisterForm):

    def is_valid(self):
        valid = super(BrokerSignupForm, self).is_valid()

        if not valid:
            return valid

        current_form = self.cleaned_data.copy()

        if current_form['creation_key'] != BROKER_CREATION_KEY:
            self.add_error('creation_key', "Creation Key invaild")
            valid = False

        return valid

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_broker = True
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        label="Email Address",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
            }),
        required=False,
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
        model = MyUser
        fields = ['email', 'first_name', 'last_name']
