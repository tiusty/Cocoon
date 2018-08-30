Ubuntu Installation
=======================
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
            pip3 install virtualenwrapper

Setting up Software
-------------------

* Set up ssh keys and add to github
* Clone repo to local machine
    * Preferably clone to: ~/work/

    ::

        cd ~
        mkdir work
        cd work
        clone git <repo> .

* Go to settings, Languages & Frameworks, Django.
    * Click enable Django support. Set the project Root to the top directory for the Git project structure.
    * Set the settings path to the location of the settings file, in my case: Cocoon/settings/local_postgres.py
* Create a run configuration
    *  Go to the Run tab and click edit run configuration. Then click the green + button. Make a new Django server run
        configuration. Set the Name to Cocoon runner.
* In ~/.bashrc add to the bottom:

    ::

        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/PycharmProjects
        source $HOME/.local/bin/virtualenvwrapper.sh

* Create the virtual environment

    ::

        mkvirtualenv Cocoon

* Go to PyCharm settings, click Project: Coocon, then Project Interpreter, then click the gear on the right side of the
    Project Interpreter drop down. Click add, then click the Existing environment. Then set the environment to the
    python in the virtual env i.e ~/.virtualenvs/Coocon/bin/python3.5


Creating the Postgres Database
------------------------------
**Both on the server and locally a postgres database should be used**

Setting up Postgres locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions are from this website_:

.. _website: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

::

    The Database table name should be: Cocoon
    The Database User should be: cocoon_dev
    The Database Password should be: cocoon_pass

::

    sudo -u postgres psql
    CREATE DATABASE Cocoon;
    CREATE USER cocoon_dev WITH PASSWORD 'cocoon_pass'; (everyone should use the same username and password for debugging locally)
    ALTER ROLE cocoon_dev SET client_encoding TO 'utf8';
    ALTER ROLE cocoon_dev SET default_transaction_isolation TO 'read committed';
    ALTER ROLE cocoon_dev SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE Cocoon TO cocoon_dev;
    ALTER USER cocoon_dev CREATEDB; (allow unit tests to be run)
    \q

Tips
-----
* To manually load the virtual environment:

    ::

        workon Cocoon
* To get out of the virtual env:

    ::

        deactivate
