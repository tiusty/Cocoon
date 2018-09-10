# Core Django Imports
from django.core.files.images import ImageFile

# Third party imports
from ftplib import FTP, error_perm
import tempfile
import os

# Import from houseDatabase app
from cocoon.houseDatabase.models import RentDatabaseModel, HousePhotos, HomeProviderModel


class MlspinRequesterImage(object):
    """
    This class implements the logic to retrieve all the images for homes on the server
    The homes must already be saved onto the Cocoon database. This will iterate through all the homes
    and if a different amount of images exist on the MLSpin server than on the Cocoon server,
    the directory is deleted and the images are uploaded.

    Attributes:
        self.homes (list(RentDatabaseModel object)) -> This stores all the homes for which
            images are being added to
    """

    def __init__(self, last_update):
        # Create a list of all the homes.
        # If no last_update value is passed in then it defaults to filtering homes that were
        #   last updated today
        self.homes = RentDatabaseModel.objects.filter(last_updated_home=last_update) \
            .filter(listing_provider_home=HomeProviderModel.objects.get(provider="MLSPIN"))

    def add_images(self):
        # For each home see how many photos are stored
        #   If there is not the same amount of photos in the ftp server as there
        #   are saved, then photos were added or deleted. Therefore delete the photos
        #   and re-upload them.
        for home in self.homes:
            # Make sure the listing number is valid
            # This is a simple check that there is a positive listing number
            if home.listing_number > 0:
                # Need to parse the listing numbers to find the location of the photos.
                # The directory goes like photo/##/###/###_#.jpg
                # The first 8 numbers correspond to the mlspin listing number
                first_directory = str(home.listing_number)[:2]
                second_directory = str(home.listing_number)[2:5]
                file_name = str(home.listing_number)[5:9] + "_"

                # Determine if the house photos needs updating.
                # This is to speed up updating the photos by skipping homes with photos already
                if not home.housephotos_set.exists():

                    # Connect to the FTP server and login
                    ftp = FTP("ftp.mlspin.com", "anonymous", "")
                    ftp.login()

                    # Retrieve a list of all the images for a corresponding home (from the mlspin listing number)
                    # Only stores files that have the file_name in the name of the file
                    file_names = list(filter(lambda x: file_name in x, ftp.nlst(os.path.join('photo', first_directory,
                                                                                             second_directory))))

                    # Determine if there are housePhoto files and if so deletes them
                    if home.housephotos_set.exists():
                        for photo in home.housephotos_set.all():
                            # Determine if an image is currently saved
                            # if photo.image:
                            # If there is an image saved, then make sure it is a file
                            # if os.path.isfile(photo.image.path):
                            # Delete the image on the machine
                            # os.remove(photo.image.path)
                            # Delete the image from the database
                            # Note: This does not delete the file from the machine which
                            #   is why it is deleted beforehand. It just deletes the reference
                            #   to the file on the database
                            photo.delete()

                    # Save each image to the database
                    for file in file_names:
                        with tempfile.TemporaryFile("wb+") as lf:
                            try:
                                ftp.retrbinary("RETR " + file, lf.write)
                            # If a permission error occurs then skip to the next image
                            #   This usually occurs if the image doesn't exist for some reason
                            except error_perm:
                                print("Error_perm happened" + str(file))
                                continue
                            # Timeout sometimes occurs, so instead of quiting,
                            #   just skip that image
                            except TimeoutError:
                                print("File Timeout" + str(file))
                                continue
                            new_photos = HousePhotos(house=home)
                            new_photos.image.save(os.path.basename(file), ImageFile(lf))
                            new_photos.save()

                    print("[ ADDED PHOTOS ] " + home.full_address)
                else:
                    print("[ ALL SET ] " + home.full_address)

            else:
                print("Listing number is not valid")
