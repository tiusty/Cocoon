# Downloads the IDX data file and parses the apartment
# data for the database

'''

Overview

1. Download the file with urllib
2. Hardcode in values like # cols, important cols
3. Split the entire file on the '|' character
4. Check that every value exists 
5. Clean values to work with our db definitions
6. For each apartment, if it doesn't exist:
	- write it into the database
	if it exists,
	- update all of the fields in the database

delimeters are '|' except after no_baths field, they are \r\n

'''

from subprocess import check_output, call
import urllib.request
import shutil
import re

NUM_COLS = 29 # mlspin specific

# IDX URL associated with BIll's MLSpin login
URL = "http://idx.mlspin.com/idx.asp?user=2KBz9tMntTFtBUNR7rdjyYtL2Y2z9tntuNRKTrZRhFoDtU7cvZ292ImROLfmoRnxtyD&proptype=RN"
	
#==================================# 
# For saving the IDX feed to a file 
#==================================#

try: urllib.request.urlretrieve(URL, "idx_feed.txt")
except (urllib.HTTPERROR, urllib.URLERROR):
	print(e)
	call(["curl", "-s", URL, "-o", "idx_feed.txt"])

idx_file = open("idx_feed.txt", "rb")
idx_byte_txt = (idx_file.read())
idx_txt = (idx_file.read().decode("iso-8859-1"))


#==================================# 
# For reading the IDX feed to memory
#==================================#

# idx_response = urllib.request.urlopen(URL)
# idx_byte_data = idx_response.read()
# idx_text = str(idx_byte_data)

# splits on '|' or carriage return

data_cells = re.split(b'\||\r\n', idx_byte_txt)

# print(idx_byte_txt)

PROP_TYPE = 0
LIST_NO = 1
LIST_AGENT = 2
LIST_OFFICE = 3
STATUS = 4
LIST_PRICE = 5
STREET_NO = 6
STREET_NAME = 7
UNIT_NO = 8
TOWN_NUM = 9
AREA = 10
ZIP_CODE = 11
LENDER_OWNED = 12
REMARKS = 13 # 17
PHOTO_COUNT = 14
PHOTO_DATE = 15
PHOTO_MASK = 16
COUNTY = 17
STATE = 18
RN_TYPE = 19
NO_ROOMS = 20
NO_BEDROOMS = 21
NO_FULL_BATHS = 22
NO_HALF_BATHS = 23
MASTER_BATH = 24
PARKING_SPACES = 25
LOT_SIZE = 26
SQUARE_FEET = 27
NO_BATHS = 28


# for i in range(0, NUM_COLS):
# 	print(data_cells[i+29])

for i in range(0, len(data_cells)-29, NUM_COLS):
 	for j in range(i, i+29):
 		print(data_cells[j], end="")

 	print()

