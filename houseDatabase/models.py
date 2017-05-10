from django.db import models
import datetime


notSetChar = "Not set"


# Create your models here.
class RentDatabase(models.Model):
    address = models.CharField(max_length=200, default=notSetChar)
    price = models.IntegerField(default=-1)
    home_type = models.CharField(max_length=200, default=notSetChar)
    moveInDay = models.DateField(default=datetime.date.today)
    numBedrooms = models.IntegerField(default=0)
    numBathrooms = models.IntegerField(default=0)
    air_conditioning = models.BooleanField(default=False)
    washDryer_InHome = models.BooleanField(default=False)
    dishWasher = models.BooleanField(default=False)
    bath = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    def get_price(self):
        return self.price

    def get_price_str(self):
        return "$" + str(self.price)

    def get_move_in_day(self):
        return self.moveInDay

    def get_num_bedrooms(self):
        return self.numBedrooms

    def get_home_type(self):
        return self.home_type

    def get_address(self):
        return self.address

    def has_air_conditioning(self):
        return self.air_conditioning

    def has_wash_dryer_in_home(self):
        return self.washDryer_InHome

    def has_dish_washer(self):
        return self.dishWasher

    def has_bath(self):
        return self.bath

