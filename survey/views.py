from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('homePage:index'))
