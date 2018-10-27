# Django Modules
from django.core.management.base import BaseCommand

# Cocoon Modules
from cocoon.commutes.models import CommuteType


class Command(BaseCommand):
    """
    Creates all the necessary commute objects for Cocoon
    """

    help = 'Create Commute Type Models'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        """
        Creates all the necessary commute objects for Cocoon
        """

        # Create the commute types if they don't exist
        self.create_commute_type_objects()

    @staticmethod
    def create_commute_type_objects():
        """
        Create the commute type objects if they don't exist
        """
        for commute_type in CommuteType.COMMUTE_TYPES:
            CommuteType.objects.get_or_create(commute_type=commute_type)
