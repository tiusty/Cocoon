# Django Modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Cocoon Modules
from cocoon.houseDatabase.management.commands.pull_mlspin import MlspinRequester
from cocoon.houseDatabase.management.commands.pull_mlspin_images import MLSpinRequesterImage
from cocoon.houseDatabase.management.commands.ygl.YGLRequester import YGLRequester


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
        # self.pull_mlspin_homes(update_timestamp)
        self.pull_ygl_homes(update_timestamp)

        # Pull the images
        # self.pull_mlspin_images(update_timestamp)

    @staticmethod
    def pull_mlspin_homes(timestamp):
        """
        Pulls the homes from MLSpin
        """
        # Pull the MLS homes
        mlspin_request = MlspinRequester(timestamp=timestamp)
        mlspin_request.parse_idx_feed()

    @staticmethod
    def pull_mlspin_images(timestamp):
        """
        Pulls images for MLSpin homes
        """
        requester_mlspin_images = MLSpinRequesterImage(last_update=timestamp)
        requester_mlspin_images.add_images()

    @staticmethod
    def pull_ygl_homes(timestamp):
        """
        Pulls the homes from YGL
        """
        ygl_requester = YGLRequester(timestamp=timestamp)
        ygl_requester.parse_idx_feed()

