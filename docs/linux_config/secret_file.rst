============
Secret.json
============

This file contains variables that are loaded by the settings file to make machine specific settings. It is also used to hide secret keys etc from going on version control

For a server that uses apache, the settings file is controlled by the DJANGO_SETTINGS_MODULE variable in the secrets.json. It is loaded in wsgi.py
For a runesrver, the settings file is controlled by environment variables. Therefore to change settings files, change the environment variables
Notes: Pycharms sets it for you
