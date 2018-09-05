=========
Commutes
=========

This module takes care of doing approximate commute caching. It also queries the google distance matrix api to retieve exact and approximate commutes for different locations. All of the commute generation is done in this module.

Internal Modules:
------------------

Distance_matrix.py
~~~~~~~~~~~~~~~~~~~~~
This module does both updates the caching for approximate commutes and handles the querying to google distance matrxip api
  
**Files:**

* update_commute_cache.py

  * This file updates the cache for all the approximate commutes. Each commute type stores the approximations in a different manner. Right now only Driving and Transit have a cache stored.
  
* distance_wrapper.py

  * This file contains the DistanceWrapper class which wraps the google distance matrix api to more easily be used. This also handles errors that occur from the return of the api calls. This is used to generate both the approximations and exact commutes

* compute_approximates.py

  * This file computes the approximate distance/time between the given zipcodes. 
