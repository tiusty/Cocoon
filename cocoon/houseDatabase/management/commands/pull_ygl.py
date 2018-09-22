# Django Modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Cocoon Modules
from cocoon.houseDatabase.management.commands.ygl.YGLRequester import YGLRequester
from cocoon.houseDatabase.management.commands.ygl.YGLRequesterImages import YGLRequesterImage


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

        # Pull the homes
        self.pull_ygl_homes(update_timestamp)
        self.pull_ygl_images(update_timestamp)

    @staticmethod
    def pull_ygl_homes(timestamp):
        """
        Pulls the homes from YGL
        """
        ygl_requester = YGLRequester(timestamp)
        ygl_requester.parse_idx_feed()

    @staticmethod
    def pull_ygl_images(timestamp):
        """
        Pulls images for ygl homes
        """
        requester_ygl_images = YGLRequesterImage(timestamp)
        requester_ygl_images.add_images()
