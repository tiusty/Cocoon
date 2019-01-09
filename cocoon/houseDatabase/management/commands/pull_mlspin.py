# Django Modules
from django.core.management.base import BaseCommand
from django.utils import timezone

# Cocoon Modules
from cocoon.houseDatabase.management.commands.mlspin.MlspinRequester import MlspinRequester
from cocoon.houseDatabase.management.commands.mlspin.MlspinRequesterImages import MlspinRequesterImage


class Command(BaseCommand):
    """
    Command class that creates an MlsPinRequester object and requests the URL
    of the apartments and towns txt files. This command is accessible via manage.py
    """

    help = 'Ingests IDX feed into database'

    def add_arguments(self, parser):
        # Argument allows a specified number of homes to be pulled,
        #   If not specified then all homes are pulled.
        parser.add_argument(
            '--num_homes',
            action='store',
            dest='num_homes',
            help='Number of homes to pull, leave blank for all',
            type=int)

    def handle(self, *args, **options):
        """
        Pulls all the homes for all the providers
        """
        num_homes = -1
        if options['num_homes']:
            num_homes = options['num_homes']

        update_timestamp = timezone.now()

        # Pull the homes
        self.pull_mlspin_homes(update_timestamp, num_homes)

        # Pull the images
        self.pull_mlspin_images(update_timestamp)

    @staticmethod
    def pull_mlspin_homes(timestamp, num_homes):
        """
        Pulls the homes from MLSpin
        """
        # Pull the MLS homes
        mlspin_request = MlspinRequester(timestamp, num_homes=num_homes)
        mlspin_request.parse_idx_feed()

    @staticmethod
    def pull_mlspin_images(timestamp):
        """
        Pulls images for MLSpin homes
        """
        requester_mlspin_images = MlspinRequesterImage(timestamp)
        requester_mlspin_images.add_images()
