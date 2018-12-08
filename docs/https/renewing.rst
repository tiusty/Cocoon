Renewing HTTPS
===============


1. Make sure to open AWS firewall to all inbound connections (if there are firewall restrictions)

2. Run

::
    sudo certbot --apache
   
Then click enter through the prompts. At the end do 1. (no redirect) since the config is already set up and you don't want to touch it

