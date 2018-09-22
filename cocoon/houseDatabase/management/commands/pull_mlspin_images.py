# Django Modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Cocoon Modules
from cocoon.houseDatabase.management.commands.mlspin.MlspinRequesterImages import MlspinRequesterImage


class Command(BaseCommand):
    """
    Command class that creates an MlsPinRequester object and requests the URL
    of the apartments and towns txt files. This command is accessible via manage.py
    """

    help = 'Ingests IDX feed into database'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        """
        Pulls all the homes for all the providers
        """

        update_timestamp = timezone.now()

        # Pull the images
        self.pull_mlspin_images(update_timestamp)

    @staticmethod
    def pull_mlspin_images(timestamp):
        """
        Pulls images for MLSpin homes
        """
        requester_mlspin_images = MlspinRequesterImage(timestamp)
        requester_mlspin_images.add_images()
