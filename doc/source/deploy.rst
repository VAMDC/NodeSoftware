.. _deploy:

Deployment of your node
=========================

Now that you have a node that runs nicely with djangos test server, the 
last remaining step is to configure the server that will run the node
in a production setup.

How and on which server you set up your node to run permanently, is much 
dependent on your technical resources and the solution we give here is 
just one out of several possibilities (although we also quickly mention 
the most common alternative).

Gunicorn
--------------------------------

tbw.

The Proxy
--------------------------------

nginx or lighttpd or apache

tbw

Deployment in Apache
--------------------------------

The Apache webserver can not only act as a proxy but also replace 
Gunicorn by using its mod_wsgi plugin to run the Python code directly. 
You can find two example files in your node directory about this:

* *apache.conf*: This is an Apache config file that defines a virtual 
  server, bound to a certain host name. You will have to edit several 
  things in that file before it will work in Apache: the server name
  and the path to the node software in a few places. On a Debian-like 
  system you would then move this file to 
  */etc/apache2/sites-available/vamdcnode* and run *a2ensite vamdcnode* to 
  activate it.
* *django.wsgi*: This is the file that the previous one points to in its 
  WsgiScriptAlias. Edit the path and your node's name.

Once you have set this up and re-started the Apache webserver, your node 
should deliver data at the configured URL.
