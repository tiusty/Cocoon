from django.shortcuts import render


"""
This view function should only be for global views, i.e error messages 
"""


def error_404_view(request, exception):
    return render(request, 'error_pages/error_404.html')
