# Import Django Modules
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_new_itinerary_email(agent):
    """
    Sends an email when a new itinerary is created to inform all the agents to check out the
        marketplace
    :param agent:  (MyUser model) -> A user that has is_broker set to true.
    """
    if hasattr(settings, 'DEFAULT_DOMAIN'):
        domain = settings.DEFAULT_DOMAIN
    else:
        domain = "https://bostoncocoon.com/"

    message = render_to_string(
        'scheduler/email/new_itinerary.html',
        {
            'domain': domain,
            'agent_name': agent.first_name
        }
    )

    subject = 'New Itinerary Available in the Cocoon Marketplace'
    recipient = agent.email
    email = EmailMessage(
        subject=subject, body=message, to=[recipient]
    )
    email.content_subtype = "html"

    # send confirmation email to user
    email.send()
