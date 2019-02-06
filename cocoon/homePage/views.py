# Django Modules
from django.views.generic import TemplateView


class LandingPage(TemplateView):

    template_name = "homePage/landingPage.html"


class AboutUs(TemplateView):

    template_name = "homePage/aboutUs.html"
