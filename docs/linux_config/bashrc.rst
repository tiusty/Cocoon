===============
Bash.rc File
===============

Copy the following code into bottom of bash.rc
  * Some of the code was added in the installation doc, so please don't duplicate. This is just as reference
  
bash.rc
-----------

::
  
  export DJANGO_SETTINGS_MODULE=config.settings.production # Sets the setting for for the runserver script, wsgi loads it from the secret file
  export WORKON_HOME=$HOME/.virtualenvs # Sets the locations that the virtualenvs will be stored for virtaulenvwrapper
  export PROJECT_HOME=$HOME/work # Sets the project home directory
  source $HOME/.local/bin/virtualenvwrapper.sh # Sets the location of the virtualenvwrapper script
