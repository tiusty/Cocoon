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
  
  **Appriximations for each commute**
  
  * Driving:
   
    * Driving approximations are computed as the distance/time between two zip codes. This gives an approximation of the time and distance that it will take. 
  * Transit:
    
      * Transit currently uses the exact approximation type as Driving
      
  * Bicycling:
    
    * Bicycling does not have an approximation stored in the commutes model. Instead the approximation is determined by computing the lat_lng for the destination and then finding the distance between each home and the destination. Then we give an average speed for a biker and that computes the approximate commute time. Distance is added to the home as the home gets farther away to account for a turns and going around terrain features, i.e lakes
    
 * Walking:
  
    * Walking is computed in the same way as bicycling but uses a different average speed to compute the approximate commute time
