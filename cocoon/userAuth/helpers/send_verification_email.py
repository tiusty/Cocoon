# Used for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ..tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives

# Load the logger
import logging
logger = logging.getLogger(__name__)


def send_verification_email(domain, user):

    if domain is not None:
        # Create the email context that is sent to the user
        current_site = get_current_site(domain)
        mail_subject = 'Verify your Cocoon Account'
        text_message = render_to_string(
            'userAuth/email/account_activate_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        html_message = render_to_string(
            'userAuth/email/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
        )
        from_email = 'devteam@bostoncocoon.com'
        to_email = user.email
        email = EmailMultiAlternatives(mail_subject, text_message, from_email, to=[to_email])
        email.attach_alternative(html_message, "text/html")

        # Send the email to the user
        email.send()
    else:
        logger.error("In {0}, domain is None".format(send_verification_email.__name__))
