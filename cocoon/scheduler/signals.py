# Django module imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# App module imports
from .models import ItineraryModel


@receiver(post_save, sender=ItineraryModel)
def itinerary_model_save(instance, *args, **kwargs):
    """
    This function runs post-save of the new model.
    Specifically, it is used to wait until the models other fields have been
    set to hash them together, forming the url
    """

    if instance.url is '':
        instance.url = instance.generate_slug()
        instance.save()


@receiver(post_delete, sender=ItineraryModel)
def itinerary_model_delete(instance, *args, **kwargs):
    """
    After an Itinerary model is deleted, if it had an agent associated with it,
        then email that agent that their itinerary has been deleted.

    Also doesn't email the user if the itinerary is already finished
    """

    # Only perform action is the itinerary is assigned to an agent and the itinerary
    #   is not already finished
    if instance.agent is not None and not instance.finished:

        # Email the agent telling them that the itinerary has been cancelled
        message = render_to_string(
            'scheduler/email/itinerary_cancellation_email.html',
            {
                'client': instance.client,
                'agent': instance.agent.first_name,
                'homes': instance.homes,
            }
        )
        subject = 'Itinerary cancelled for {0}'.format(instance.client)
        recipient = instance.agent.email
        email = EmailMessage(
            subject=subject, body=message, to=[recipient]
        )
        email.content_subtype = "html"

        # send confirmation email to user
        email.send()

