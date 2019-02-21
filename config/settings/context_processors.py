from django.conf import settings


def settings_context(request):
    if hasattr(settings, 'USING_PRODUCTION'):
        return {'USING_PRODUCTION': settings.USING_PRODUCTION}
    else:
        return {'USING_PRODUCTION': True}
