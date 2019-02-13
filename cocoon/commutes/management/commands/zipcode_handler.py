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
            help='Creates zipcode baseline file',
        )

        parser.add_argument(
            '--load_baseline',
            action='store_true',
            dest='load_baseline',
            help='Loads zipocodes from baseline file into the database',
        )

        parser.add_argument(
            '--compare_baseline',
            action='store_true',
            dest='compare_baseline',
            help='Compares zipcodes from baseline file to the database',
        )

        parser.add_argument(
            '--commute_type_input',
            type=str,
            help='Specify a commute type. One of:"driving", "transit"',
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

        elif options['load_baseline']:
                ZipcodeBaseline().load_zipcode_combinations(commute_type)

        elif options['compare_baseline']:
            ZipcodeBaseline().compare_baseline(commute_type)

    @staticmethod
    def parse_input_commute_type(commute_type_input):
        """
        Parses input commute type variable to determine which commute type is being run
            If the type is unknown then quit
        :param commute_type_input: (string) -> the commute type input the user entered
        :return:
        """
        commute_type = None
        if commute_type_input.lower() == "driving":
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.DRIVING)[0]
        elif commute_type_input.lower() == "transit":
            commute_type = CommuteType.objects.get_or_create(commute_type=CommuteType.TRANSIT)[0]
        else:
            print("Unknown Commute type")
            exit(1)
        return commute_type



