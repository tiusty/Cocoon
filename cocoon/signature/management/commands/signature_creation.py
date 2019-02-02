# Django Modules
from django.core.management.base import BaseCommand

# Cocoon Modules
from ...models import HunterDocTemplateModel


class Command(BaseCommand):
    """
    Creates all the necessary commute objects for Cocoon
    """

    help = 'Create Signature Models'

    def add_arguments(self, parser):
        # add args here
        return

    def handle(self, *args, **options):
        """
        Creates all the necessary signature objects for Cocoon
        """

        self.create_pr_tour_template()

    @staticmethod
    def create_pr_tour_template():
        """
        Creates the hunter doc template for pre tour
        """
        HunterDocTemplateModel.get_pre_tour_template()
