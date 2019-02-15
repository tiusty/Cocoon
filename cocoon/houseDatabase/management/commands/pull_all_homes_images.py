# Django Modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Cocoon Modules
from cocoon.houseDatabase.management.commands.pull_mlspin_images import MlspinRequesterImage
from cocoon.houseDatabase.management.commands.ygl.YGLRequester import YGLRequester
from cocoon.houseDatabase.management.commands.ygl.YGLRequesterImages import YGLRequesterImage
from cocoon.houseDatabase.management.commands.mls_rets.MLSRetsRequester import MLSRetsRequester


class Command(BaseCommand):
    """
    Command that pulls the homes and images for all the providers, i.e MLSpin and YGL
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
        self.pull_mls_rets_homes(update_timestamp)

        # Pull the images
        self.pull_ygl_images(update_timestamp)
        self.pull_mlspin_images(update_timestamp)

    @staticmethod
    def pull_mlspin_images(timestamp):
        """
        Pulls images for MLSpin homes
        """
        requester_mlspin_images = MlspinRequesterImage(timestamp)
        requester_mlspin_images.add_images()

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

    @staticmethod
    def pull_mls_rets_homes(timestamp):
        """
        Pulls the homes from YGL
        """
        rets_requester = MLSRetsRequester(timestamp)
        rets_requester.run()
