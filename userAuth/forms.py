from django.contrib.auth.forms import AuthenticationForm
from django import forms


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username",
                               max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'name': 'username',
                                          'placeholder': 'Username',
                                          }),
                               )
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'name': 'password',
                                          'placeholder': 'Password',
                                          }),
                               )
    remember = forms.ChoiceField(
        label="Remember",
        widget=forms.CheckboxInput(),
        required=False,
    )
