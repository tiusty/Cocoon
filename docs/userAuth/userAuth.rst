========
UserAuth
========

Models.py
~~~~~~~~

MyUesr

* Stores all the information based on user. Determines user type, i.e broker or hunter.

UserProfile

* Stores all the information for the users profile. Stores mappings to user surveys, favorites, visit list etc

Views.py
~~~~~~~~~

Signup

* Has functionality for signing up a user. The user signup depends if they are creating a broker or a hunter account.

Login

* Contains functionality for authenticating and logging in users

User Profile

* Contains functionality to display the user profile with appropriate information

Forms.py
~~~~~~~~~

LoginUserForm

* Login form for autenticating and logging in users

BaseRegisterForm

* The base register form that is used by both the ApartmentHunter and Broker signup forms

ApartmentHunterSignupForm

* The form for an apartment hunter to sign up with Cocoon

BrokerSignupForm

* The form for a broker to sign up with Cocoon

ProfileForm

* A form that allows a user to change certain information about their profile
