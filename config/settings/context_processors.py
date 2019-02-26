from django.conf import settings


def settings_context(request):
    context = {}

    # Determines if the system is running on production settings
    if hasattr(settings, 'USING_PRODUCTION'):
        context['USING_PRODUCTION'] = settings.USING_PRODUCTION
    else:
        context['USING_PRODUCTION'] = True

    # Whenever the request is not present then we need to determine the
    #   domain via the context processor
    if hasattr(settings, 'DEFAULT_DOMAIN'):
        context['DEFAULT_DOMAIN'] = settings.DEFAULT_DOMAIN
    else:
        context['DEFAULT_DOMAIN'] = "https://bostoncocoon.com/"

    return context
