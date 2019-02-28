from django.apps import AppConfig


class SurveyConfig(AppConfig):
    name = 'cocoon.survey'

    def ready(self):
        import cocoon.survey.signals
