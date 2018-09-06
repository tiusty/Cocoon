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
  
4. Symlink apache2 file

::
 
 sudo ln -sf ~/work/Cocoon/config/apache2/000-default.conf /etc/apache2/sites-available/
 
 
