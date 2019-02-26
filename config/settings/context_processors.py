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
        context['default_domain'] = settings.DEFAULT_DOMAIN
    else:
        context['default_domain'] = "https://bostoncocoon.com/"
