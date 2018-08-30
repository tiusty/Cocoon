**Ubuntu**
*Please install ubuntu 16.04*

Installing Software
-------------------

* Install the latest version of pycharms
* Install Git
* Install pip3 + virtualenv + virtualenvwrapper:

        ::

            sudo apt-get install python3-pip
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
        git clone git@github.com:tiusty/Cocoon.git

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

Tips
-----
* To manually load the virtual environment:

    ::

        workon Cocoon
* To get out of the virtual env:

    ::

        deactivate
