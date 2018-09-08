# Django Modules
from django.core.management.base import BaseCommand

# Cocoon Modules
from cocoon.houseDatabase.management.commands.mlspin.pull_mlspin import MlspinRequester
from cocoon.houseDatabase.management.commands.ygl.pull_ygl import YGLRequester


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
        # self.pull_mlspin_homes()
        self.pull_ygl_homes()

    @staticmethod
    def pull_mlspin_homes():
        """
        Pulls the homes from MLSpin
        """
        # Pull the MLS homes
        mlspin_request = MlspinRequester()
        mlspin_request.parse_idx_feed()

    @staticmethod
    def pull_ygl_homes():
        """
        Pulls the homes from YGL
        """
        ygl_requester = YGLRequester()
        ygl_requester.parse_idx_feed()

