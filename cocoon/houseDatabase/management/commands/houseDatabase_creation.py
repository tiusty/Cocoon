# Django Modules
from django.core.management.base import BaseCommand

# Cocoon Modules
from ...models import HomeProviderModel, HomeTypeModel


class Command(BaseCommand):
    """
    Creates all the necessary models for the house database app
    """

    help = 'Create House Database models'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        """
        Creates all the necessary models for the houseDatabase app
        """

        # Create home providers if they don't exist
        self.create_home_provider_objects()

        # Create home types if they don't exist
        self.create_home_type_objects()

    @staticmethod
    def create_home_provider_objects():
        """
        Creates the home provider objects for Cocoon if they don't exist
        """
        for provider in HomeProviderModel.PROVIDER_TYPES:
            HomeProviderModel.objects.get_or_create(provider=provider[0])

    @staticmethod
    def create_home_type_objects():
        """
        Creates the home type objects fro Cocoon if they don't exist
        """
        for home_type in HomeTypeModel.HOME_TYPE:
            HomeTypeModel.objects.get_or_create(home_type=home_type[0])

