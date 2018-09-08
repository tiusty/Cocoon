# Django Modules
from django.core.management.base import BaseCommand

# Cocoon modules
from cocoon.houseDatabase.management.commands.mlspin.pull_mlspin_images import MLSpinRequesterImage


class Command(BaseCommand):
    """
    Command class that creates an MlsPinRequesterImage object and uploads images for homes in the Cocoon database.
    This command is accessible via manage.py
    """

    help = 'Ingests MLSpin photos into the database'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        self.pull_mls_images()

    @staticmethod
    def pull_mls_images():
        """
        Pulls images for homes in MLS
        """
        # Create the MLSpin Requester
        request = MLSpinRequesterImage()
        # Add images
        request.add_images()
