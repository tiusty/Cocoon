import csv
from enum import Enum


class Columns(Enum):
    ID = 0
    NAME = 1
    CONTACT = 2
    WEBSITE = 3
    PHONE1 = 4
    PHONE2 = 5
    FAX1 = 6
    EMAIL = 7
    ADDRESS1 = 8
    ADDRESS2 = 9
    CITY = 10
    STATE = 11
    ZIP = 12
    SOURCE = 13
    BROKER_NOTES = 14
    UPDATE_DATE = 15
    LISTING_AGENT_ID = 16


counter = 0
with open('ygl_landlords.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        counter += 1
        if counter > 5:
            break
        if line_count == 0:
            print('Column names are {0}'.format(row))
            line_count += 1
        else:
            print('\t{0} works in the {1} department, and was born in {2}.'.format(row[0], row[1], row[2]))
            line_count += 1
    print('Processed {0} lines.'.format(line_count))
