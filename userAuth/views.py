from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegisterForm, UserCreationForm
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('userAuth:login'))


def login(request):
    context = {
        'error_message': [],
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to success page
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            # return invalid user
            context['error_message'].append('Unable to login, try again')
    form = LoginForm
    context['form'] = form
    return render(request, 'userAuth/login.html', context)


def register(request):
    context = {
        'error_message': [],
    }
    print('start')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('was valid')
            return HttpResponseRedirect(reverse('homePage:index'))
        else:
            context['error_message'].append('Unable to create user')
            print(form.errors)
    form = RegisterForm()
    context['form'] = form
    return render(request, 'userAuth/register.html', context)
