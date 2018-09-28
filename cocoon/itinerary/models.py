from django.db import models

# Import cocoon models
from cocoon.userAuth.models import MyUser
from cocoon.houseDatabase.models import RentDatabaseModel

class Itinerary(models.Model):
	"""
   	Model for Itinerary. These are based on the interface designed on the Google Doc. 

   	NOTE: 
   	1. Itierary File - I wasn't sure what to make FileField, so I made it null for now
   	2. Available_Start_time - I wasn't sure how to make a list,so I just set it as a date for now
   	3. Homes - Alex was relunctant on making this a ManyToMany
    """
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    itinerary_file = models.FileField(Field.null, on_delete=models.CASCADE)
    agent = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    start_time = models.DateTime(default=timezone.now)
    available_start_time = models.DateField(default=timezone.now)
    homes = models.ManyToMAny(RentDatabaseModel)

    def __str__(self):
        return self.itinerary_file
