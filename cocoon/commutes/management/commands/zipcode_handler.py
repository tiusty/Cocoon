from django.core.management.base import BaseCommand

from .ZipcodeBaseline.ZipcodeBaseline import ZipcodeBaseline


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
            '--commute_type',
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
        if options['create_baseline']:
            if options['commute_type'] and (options['commute_type'].lower() == "driving" or
                                            options['commute_type'].lower() == "transit"):

                commute_type = options['commute_type'].lower()

                ZipcodeBaseline().create_baseline(commute_type)
                ZipcodeBaseline().update_zipcode_database()


