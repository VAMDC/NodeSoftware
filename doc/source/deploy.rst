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
Gunicorn (http://gunicorn.org/, `sudo apt install gunicorn` on Debian/Ubuntu) which is aware of Django and understands
its settings.

You would write a `gunicorn.conf` file (you find it in `nodes/ExampleNode`)
like this:

.. literalinclude:: ../../nodes/ExampleNode/gunicorn.conf

and then simply start it from within your node directory with::

    $ gunicorn -c gunicorn.conf settings.wsgi:application

(Note: In modern Django, use the WSGI application directly rather than the deprecated gunicorn_django command.)

The example config makes Gunicorn listen at a unix-socket. Even though you can
connect it to a TCP-port instead (see commented out line), you do not want
external requests sent directly to Gunicorn, but to a proxy instead. This
proxy takes care of the load balancing between the Gunicorn worker processes
and can compress the XML output from your node before sending it.

Nginx as proxy
~~~~~~~~~~~~~~~~~~
Nginx (http://nginx.org/en/, `sudo apt install nginx` on Debian/Ubuntu) is a
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
* *wsgi.py*: This is the file that the previous one points to in its 
  WsgiScriptAlias. Edit the path and your node's name.

Once you have set this up and re-started the Apache webserver, your node 
should deliver data at the configured URL.

Container-based deployment
--------------------------------
Modern deployment increasingly uses containerization for consistency across
environments. Docker containers can encapsulate your node with all dependencies,
making deployment portable and reproducible. Container orchestration platforms
like Kubernetes can manage scaling and availability.

For cloud platforms, services like AWS ECS, Google Cloud Run, or Azure Container
Apps provide managed container hosting. Platform-as-a-Service options like
Heroku, Railway, or Fly.io also support Django applications with minimal
configuration.

See https://docs.docker.com/ and Django deployment documentation for container-based
deployment patterns.

.. _logging:

Logging
------------------

Finally, a few words on logging the access to your node. There are two basic
ways:

* let the webserver do it.
* let the NodeSoftware do it.

The webserver/proxy, be it nginx or apache, keeps a log on when, how and by
whom your node is accessed. Since the query itself is in the accessed URL, it
also ends up in these logs. There are many tools to analyze and visualize this
kind of logs. In the case of Apache/WSGI-deployment, errors in the NodeSoftware show up the webservers error-log since it is the former that executes the latter. With gunicorn, the webserver knows nothing about the NodeSoftware's errors since it only acts as a proxy. Gunicorn keeps its own logs.

However, the webserver logs usually contain no information about what happened
inside the NodeSoftware. If you want to keep tabs on how much data was returned
from each query, how long it took to process and so on, you need to tell the
NodeSoftware to save this information for you - this is where the `logging`-facility comes into play.

Nodes will primarily use this in their ``queryfunc.py`` where you initialize it like this::
    
    import logging
    >>> log = logging.getLogger('vamdc.node.queryfu')

Then any of the following can be used to log messages of different levels::

    >>> log.debug('some text with a variable: %s'%variable)
    >>> log.info('bla')
    >>> log.warning('bla')
    >>> log.error('bla')
    >>> log.critical('bla')

Where these messages end up is configured in ``settings_default.py`` and you can as usual override the default in the node's own ``settings.py``. For example, you set the location and name of the log-file like this::

    LOGGING['handlers']['logfile']['filename'] = '/path/to/yourlog.log'

.. note::

    Critical errors (using `log.critical()`) are sent to the configured
    admin email address. You need to supply a valid address and make
    sure your server can send emails. The email address that these messages
    are sent from can bet set with ``SERVER_EMAIL='vamdcnode@your.server'``.

If you want to turn off the logging of debug messages, you can add the following for turning them on or off, depending on your global DEBUG setting::

    if not DEBUG:
        LOGGING['handlers']['logfile']['level'] = 'INFO'

For further information see https://docs.djangoproject.com/en/5.2/topics/logging/
