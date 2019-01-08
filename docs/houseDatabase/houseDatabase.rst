==============
HouseDatabase
==============

This module takes care of managing the homes and pulling homes from various sources

Internal Modules
------------------

Models.py
~~~~~~~~~~~

HomeTypeModel:

* The home type model stores the possible classifications for a home.

HomeBaseModel:

* This abstract model contains data that every home has. It has the basic information

HomeProviderModel:

* This model keeps track of type of data feed and a timestamp of the most recent update.

InteriorAmenitiesModel:

* This abstract model adds in different interior amenities a home could have

BuildingExteriorAmenitiesModel:

* This abstract model adds in the different exterior amentities a home could have

MLSpinDataModel:

* This abstract model adds in the data fields relevant for a MLS home. This needs to be changed to be more abstracted to support more types of homes in the future

RentDatabaseModel:

* This is the actual model used for storing a home. It inherits all the above models to add in all the necessary fields

HousePhotos:

* This model stores the photos associated with a particular home.

Scripts
~~~~~~~~

pull_all_homes_images.py

* Pulls all the homes and images for all the providers

pull_mlspin.py

* This script pulls all the homes from the MLS feed. It then will load the homes into our database. This will take a long time because there are thousands of homes. When the process of loading homes is done, the pull_mls_images script is called and loads all the images associated with the home.

pull_mlspin_images.py

* This script loads all the MLS images for homes already loaded into our local database

pull_ygl.py

* This script pulls all the homes from the YGL feed. It then will load the homes into our database. This will take a long time because there are thousands of homes. When the process of loading homes is done, the pull_ygl_images script is called and loads all the images associated with the home.

pull_ygl_images.py

* This script loads all the YGL images for homes already loaded into our local database
