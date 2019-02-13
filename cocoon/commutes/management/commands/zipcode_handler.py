from django.core.management.base import BaseCommand

from .ZipcodeBaseline.ZipcodeBaseline import ZipcodeBaseline
from cocoon.commutes.models import CommuteType


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Argument allows zip-codes to be pulled
        parser.add_argument(
            '--create_baseline',
            action='store_true',
            dest='create_baseline',
            help='Creates baseline for zipcode destinations',
        )

        parser.add_argument(
            '--update_baseline',
            action='store_true',
            dest='update_baseline',
            help='Updates baseline for zipcode destinations',
        )

        parser.add_argument(
            '--commute_type_input',
            type=str,
            help='Specify a commute type',
        )

    def handle(self, *args, **options):
        """
        :param args:
        :param options:
        :return:

        Function to run the command. list_zip_codes is all possible zip codes in Boston. The handler
        calls the commute_approximation function, which writes the JSON file "approximations.txt"
        """
        commute_type = self.parse_input_commute_type(options['commute_type_input'])
        if options['create_baseline']:
                ZipcodeBaseline().create_baseline(commute_type)

        if options['update_baseline']:
                ZipcodeBaseline().load_zipcode_combinations(commute_type)

    def parse_input_commute_type(self, commute_type_input):
        commute_type = None
        if commute_type_input == "driving":
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]
        elif commute_type_input == "transit":
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.TRANSIT)[0]
        else:
            print("Unknown Commute type")
            exit(1)
        return commute_type



