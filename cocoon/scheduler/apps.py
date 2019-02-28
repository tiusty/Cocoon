from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = 'cocoon.scheduler'

    def ready(self):
        import cocoon.scheduler.signals