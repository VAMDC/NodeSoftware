.. _deploy:

Deployment of your node
=========================

Now that you have a node that runs nicely with Django's test server, the 
last remaining step is to configure the server that will run the node
in a production setup.

How and on which server you set up your node to run permanently, is much
dependent on your technical resources and the solution we give here is just
one out of several possibilities (although we also quickly mention the most
common alternative).

Gunicorn plus proxy
--------------------------------
Our recommended way for hosting your node by yourself on a server is
Gunicorn (http://gunicorn.org/, `apt-get install gunicorn` on a Debian system) which is aware of Django and understands
its settings.

You would write a `gunicorn.conf` file (you find it in `nodes/ExampleNode`)
like this:

.. literalinclude:: ../../nodes/ExampleNode/gunicorn.conf

and then simply start it from within your node directory with::

    $ gunicorn_django -c gunicorn.conf

The example config makes Gunicorn listen at a unix-socket. Even though you can
connect it to a TCP-port instead (see commented out line), you do not want
external requests sent directly to Gunicorn, but to a proxy instead. This
proxy takes care of the load balancing between the Gunicorn worker processes
and can compress the XML output from your node before sending it.

Nginx as proxy
~~~~~~~~~~~~~~~~~~
Nginx (http://nginx.org/en/, `apt-get install nginx` on a Debian system) is a
fast and light-weight web server. To configure it to serve the running node
with Gunicorn, according to the example above, you would configure it like
this:

.. literalinclude:: ../../nodes/ExampleNode/nginx.conf

Note that you probably want to edit the port, server name and the location
at which to serve the node (change `/yournode/tap` at three places but make
them match each other).

If you installed *nginx* with the debian/ubuntu package, you can place symbolic
links to the config file into `/etc/nginx/` like this to make it use the config
above::

    $ cd /etc/nginx/sites-available/
    $ sudo ln -s $VAMDCROOT/nodes/YourNode/nginx.conf vamdcnode
    $ cd ../sites-enabled/
    $ sudo ln -s ../sites-available/vamdcnode
    $ sudo /etc/init.d/nginx restart

Proxy Alternatives
~~~~~~~~~~~~~~~~~~
What you choose as proxy for Gunicorn is somewhat arbitrary. Common
alternatives to *nginx* are *lighttpd* or *Apache*. Especially if the server
that is to run your node already has an Apache running for serving other
websites, it makes sense to simply tell it how to proxy your Gunicorn server::

    ProxyPass /yournode http://localhost:8000
    ProxyPassReverse /yournode http://localhost:8000


Deployment in Apache
--------------------------------

As an alternative to deplyment with Gunicorn plus proxy, the Apache webserver
can not only act as a proxy but also replace Gunicorn by using its mod_wsgi
plugin to run the Python code directly. The main disadvantage of this setup is
that you cannot configure and restart the node independantly from Apache, so
the likelyhood of interfering with any other sites that Apache serves is
larger.

There are two example files in your node directory for setting this up:

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

Third party hosting
--------------------------------
There are several upcoming hosting solutions that support Django directly so
that you simply would upload the code and your database and everything is
taken care of for you. Once these services mature, they are probably a very
good solution for nodes with relatively small volumes of data.

Searching the web for "django hosting" will point you in the right direction,
as does this list
https://convore.com/django-community/django-hosting-explosion/

Logging
------------------

Finally, a few words on logging the access to your node. There are two basic
ways:

* let the webserver do it.
* let the NodeSoftware do it.

The webserver/proxy, be it nginx or apache, keeps a log on when, how and by
whom your node is accessed. Since the query itself is in the accessed URL, it
also ends up in these logs. There are many tools to analyze and visualize this
kind of logs.

However, this contains no information about what happened inside the
NodeSoftware. If you want to keep tabs on how much data was returned from each
query, how long it took to process and so on, you need to tell the NodeSoftware
to save this information for you - either in a separate log file, or in a
separate table in your database. The infrastructure for this is however not yet
implemented in the NodeSoftware. Stay tuned.
