=======
Survey
=======

Survey
-------

The survey is taken by a user which asks them a bunch of questions. These questions are then passed into the rent algorithm

Cocoon Algorithm
---------------

The cocoon alogirhtm is a module that takes in the survey and generates a ranked list of homes for the user. The cocoon algorithm attempts to be as modular as possible so different algorithm can inherit the filtering mechanisms they desire. Currently on a renting_algorithm is used, but in the future a buying algorithm etc may be desired.

Files
~~~~~~

* base_algorithm:
 
  * The base algorithm contains data that will be common for every single alogrithm. It basically stores the list of avaiable homes and contains functions to populate the homes based on static filtering. Static filtering are filter items that are generated from a database query and are hard set values. For example, it filters out homes not in the price range, not the right home type, num of bedrooms etc. 

Survey Results
---------------

The survey results takes the ranked list of homes and displays it nicely for the user to see. The user can see the location of the homes on a map and also favorite homes they want to remember. 
