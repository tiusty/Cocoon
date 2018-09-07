from django.shortcuts import render


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request, 'error_pages/error_404.html', data)
