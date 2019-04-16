import csv


class YglLandlordInfo(object):

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

    def __init__(self, filename="ygl_landlords.csv"):
        self.landlords = {}
        self.parse_csv(filename)

    def parse_csv(self, filename):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    self.landlords[row[YglLandlordInfo.ID]] = row
                line_count += 1

    def retrieve_landlord(self, landlord_id, index):
        """
        Retrieves information on the landlord based on the landlord id
        :param landlord_id: (int) The landlord id
        :param index: (int) The index of which data is desired, should be one of the values
            assigned by the class. I.e YglLandlordInfo.ID for example
        :return: (string) -> The data associated with the requested data
        """
        return self.landlords[int(landlord_id)][int(index)]
