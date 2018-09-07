=====================
Ubuntu Installation
=====================
*Please install ubuntu 16.04*


Installing Software
-------------------

* Install the latest version of pycharms
* Install Git
* Install pip3 + virtualenv + virtualenvwrapper + databse necessary libraries:

        ::

            sudo apt-get update
            sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
            pip3 install virtualenv
            pip3 install virtualenvwrapper

Setting up Software
-------------------

* Set up ssh keys and add to github
* Clone repo to local machine
    * Preferably clone to: ~/work/

    ::

        cd ~
        mkdir work
        cd work
        git clone git@github.com:tiusty/Cocoon.git

* In ~/.bashrc add to the bottom:

    ::

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/work
        source $HOME/.local/bin/virtualenvwrapper.sh

* Create the virtual environment

    ::

        mkvirtualenv Cocoon




Creating the Postgres Database
------------------------------
**Both on the server and locally a postgres database should be used**

Pycharms setup
~~~~~~~~~~~~~~~~~

* Go to settings, Languages & Frameworks, Django.
    * Click enable Django support. Set the project Root to the top directory for the Git project structure.
    * Set the settings path to the location of the settings file, in my case: Cocoon/settings/local_postgres.py
* Create a run configuration
    *  Go to the Run tab and click edit run configuration. Then click the green + button. Make a new Django server run
        configuration. Set the Name to Cocoon runner.
* Go to PyCharm settings, click Project: Coocon, then Project Interpreter, then click the gear on the right side of the Project Interpreter drop down. Click add, then click the Existing environment. Then set the environment to the python in the virtual env i.e ~/.virtualenvs/Coocon/bin/python3.5
        

Setting up Postgres locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions are from this website_:

.. _website: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

::
        
    Everyone should use the same username and password for debugging locally:
    
    The Database table name should be: Cocoon
    The Database User should be: cocoon_dev
    The Database Password should be: cocoon_pass

::

    sudo -u postgres psql
    CREATE DATABASE Cocoon;
    CREATE USER cocoon_dev WITH PASSWORD 'cocoon_pass'; 
    ALTER ROLE cocoon_dev SET client_encoding TO 'utf8';
    ALTER ROLE cocoon_dev SET default_transaction_isolation TO 'read committed';
    ALTER ROLE cocoon_dev SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE Cocoon TO cocoon_dev;
    ALTER USER cocoon_dev CREATEDB;
    \q


Setting up the necessary Models
---------------------------------
* To Access anything you need to create a super user account for you local server
    * Go to the terminal:

    ::

        cd ~/work/Cocoon # Go to Cocoon project root directory
        workon Cocoon # Load the virtual environment
        python manage.py createsuperuser # Creates a super user
        #   Follow steps and create the super user

* Go to the admin site
    * probably: http://127.0.0.1:8000/adminBostoncocoon/

* There are models you need to create:
    * Commute Types:
        * Click on Commute Types, then add Commute Types
        * Make sure to create at least one, i.e driving, but you can create all if you want
    * Home Type Models:
        * Click on Home Type Models, then add Home Type Model
        * Create at least apartment, but you can create all 4 if you want
    * MLSManagementModel:
        * Click on MLSManagementModel, then click add
        * Just need to click save

Adding Homes to the database
-----------------------------
* Go to the manage.py location and make sure to have the virtual env loaded
    * You can also load manage.py through pycharms in the tools drop down

* Run the pull_mlspin script to add homes to the database
    * This script will try to add every avaiable apartment in boston, therefore please
        make sure to exit the script after adding a decent number of homes, maybe like 500

* To add pictures for those homes run the pull_mls_images script
    * This script might take a little while to run but wait until this script exits

Tips
-----
* To manually load the virtual environment:

    ::

        workon Cocoon
* To get out of the virtual env:

    ::

        deactivate
