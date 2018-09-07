=======================
Setting up the server
=======================

AWS Setup
----------

1. Create an EC2 instance:

* Use BostonCocoon Security group
* Create with Ubuntu 16.04 server
* Create an elastic ip address and assoiated with the instance
* If desired, a record set for type A to the elastic ip address to connect it to a domain
  
2. Follow installation setups in docs/installation.rst

* Follow steps for installing software and setting up software
 
Install python libraries

* Make sure to be in virtual env
 
::
 
  workon Cocoon
  pip install -r ~/work/Cocoon/requirments.txt
 
3. Install additional necessary pacakges

::
 
 sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y
 
 
HTTPS
------
1. Make sure aws inbound connections accepts https
 
2. Copy the http apache2 file and modify values
 
  ::
      
      cd ~/work/Cocoon/config/apache2
      cp 000-default.conf.template 000-default.conf
    
3. Now need to change some of the settings

* Change ServerName to the ServerName, i.e bostoncocoon.com

* Copy it over to the right location
    
    ::
    
      sudo ln -sf ~/work/Cocoon/config/apache2/000-default.conf /etc/apache2/enabled-available/
   
4. Now run the letsencrytscript (from https://letsencrypt.org/getting-started/)

  ::
     
    sudo apt-get update
    sudo apt-get install software-properties-common 
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update
    sudo apt-get install python-certbot-apache 
    sudo certbot --apache
    # Make sure to install cert
    # Also make sure to force redirect of https and not allow http requests
    
5. Once the new https .conf file is created need to do a couple of things

* Remove the comment for:
  
  ::
  
    WSGIDaemonProcess
    WSGIProcessGroup
 
 
 
