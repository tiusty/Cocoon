from django.db import models


notSetChar = "Not set"


# Create your models here.
class RentDatabase(models.Model):
    address = models.CharField(max_length=200, default=notSetChar)
    price = models.IntegerField(default=-1)
    home_type = models.CharField(max_length=200, default=notSetChar)

    def __str__(self):
        return self.address