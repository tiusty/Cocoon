# Django Modules
from django.core.management.base import BaseCommand

# Cocoon Modules
from ...models import CommuteType
from .ZipcodeBaseline.ZipcodeBaseline import ZipcodeBaseline


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
        self.load_zipcodes_into_database()

    @staticmethod
    def create_commute_type_objects():
        """
        Create the commute type objects if they don't exist
        """
        for commute_type in CommuteType.COMMUTE_TYPES:
            CommuteType.objects.get_or_create(commute_type=commute_type[0])

    @staticmethod
    def load_zipcodes_into_database():
        # For now we only support driving, later we can add transit
        ZipcodeBaseline().load_zipcode_combinations(CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0])

