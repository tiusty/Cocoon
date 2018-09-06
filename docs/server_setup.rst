======================
Setting up the server
=======================

AWS Setup
----------

* Create an EC2 instance:

  * Use BostonCocoon Security group
  * Create with Ubuntu 16.04 server
  
* Follow installation setups in docs/installation.rst

 * Skip any step referring to Pycharms and local setup
 
* Install python libraries
 * Make sure to be in virtual env
 :
 
  workon Cocoon
  pip install -r ~/work/Cocoon/config/requirments.txt
 
* Install additional necessary pacakges

 :
  sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y
  
* Symlink apache2 file

 :
  sudo ln -sf ~/work/Cocoon/config/apache2/000-default.conf /etc/apache2/sites-available/
 
 
