.. _deploy:

Deployment of your node
=========================

Now that you have a node that runs nicely with Django's test server, the
last remaining step is to run it permanently on a server. The setup we
describe here, and which the VALD node uses, is:

* *gunicorn* runs the Python code of the node. It is started and supervised
  by *systemd*, like any other service on a current Linux server.
* A web server in front of it (*nginx*, *Caddy* or *Apache*) receives the
  requests from the internet, handles https and compresses the XML.

The ExampleNode contains example files for all of this.

Before you go live
--------------------------------

In your node's ``settings.py``:

* ``DEBUG = False``. The ExampleNode's settings template sets it to `True`
  for testing. With `True`, error pages show anyone details about your
  installation and settings.
* ``DEPLOY_URL = 'https://your.server/yournode/tap/'``, i.e. the public
  address of your node. It appears in the XSAMS output and in the
  capabilities. Without it the node guesses the address from the request,
  which goes wrong behind a proxy.
* ``ADMINS`` and ``EXAMPLE_QUERIES`` should be filled in, see :ref:`newnode`.

If your database is a file (SQLite), the user that runs the node needs read
access to the file and to its directory.

gunicorn as a systemd service
--------------------------------

gunicorn is installed together with the other dependencies of the
NodeSoftware (it is listed in ``pyproject.toml``), so after ``uv sync`` it is
at ``.venv/bin/gunicorn`` inside the NodeSoftware directory.

The service is described by a systemd unit file. The ExampleNode contains
``gunicorn.service``:

.. literalinclude:: ../../nodes/ExampleNode/gunicorn.service

Adapt the paths, the user and the name `yournode`, then install and start
it::

    $ sudo cp gunicorn.service /etc/systemd/system/yournode.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable --now yournode
    $ systemctl status yournode

After changes to your node's code or settings, ``sudo systemctl restart
yournode`` makes it use them. The output of gunicorn and the node goes to the
system journal, see ``journalctl -u yournode``.

gunicorn listens at a unix socket, which only processes on the same machine
can reach. You do not want requests from the internet to reach gunicorn
directly, but to go through a web server.

A few notes on the parameters:

* **Workers** (``-w``): each worker answers one query at a time, so this is
  the number of queries your node handles in parallel. A worker can use a lot
  of memory during a large query, so make sure your server has enough for all
  of them at once.
* **Timeout** (``-t``): a worker that takes longer than this for a query is
  killed. Large queries can take minutes, mostly for writing the XML (see
  :ref:`limitations`). The web server in front needs a timeout at least as
  long, otherwise it gives up on the query first.
* **Several nodes** on one server simply get one unit each, with different
  names, sockets and ``DJANGO_SETTINGS_MODULE`` if they share a node directory.

nginx in front
~~~~~~~~~~~~~~~~~~
nginx (https://nginx.org, ``sudo apt install nginx`` on Debian/Ubuntu) is a
fast and light-weight web server. The ExampleNode contains this snippet for
the server block of your site:

.. literalinclude:: ../../nodes/ExampleNode/nginx.conf

After editing, check and reload the configuration::

    $ sudo nginx -t && sudo systemctl reload nginx

For https, the usual way is a free certificate from Let's Encrypt, e.g. with
``sudo apt install certbot python3-certbot-nginx`` and ``sudo certbot --nginx``.

Caddy in front
~~~~~~~~~~~~~~~~~~
Caddy (https://caddyserver.com, ``sudo apt install caddy`` on current
Debian/Ubuntu) is a web server with a very short configuration, which also
gets and renews the https certificate by itself. The ExampleNode contains
a ``Caddyfile``:

.. literalinclude:: ../../nodes/ExampleNode/Caddyfile

Apache in front
~~~~~~~~~~~~~~~~~~
If the server already runs Apache for other websites, it can just as well pass
the requests on to gunicorn. The ExampleNode contains this snippet for the
VirtualHost of your site:

.. literalinclude:: ../../nodes/ExampleNode/apache.conf

Check and reload with ``sudo apachectl configtest && sudo systemctl reload
apache2``.

Apache can alternatively run the node's code itself with *mod_wsgi*, without
gunicorn. We do not recommend that any more: the node can then not be
restarted without Apache, and has to run on the Python version that mod_wsgi was
built for.

Checking the deployed node
--------------------------------

From any machine::

    $ curl https://your.server/yournode/tap/availability
    $ curl -I "https://your.server/yournode/tap/sync?QUERY=SELECT+SPECIES"

The second command sends a HEAD request, which only returns the statistics
headers (`VAMDC-COUNT-...`) and is therefore quick. Check that the
`accessURL` in https://your.server/yournode/tap/capabilities is your public
address; if not, set ``DEPLOY_URL``.

Finally, ask the VAMDC team to register your node, see :ref:`contact`.

.. _logging:

Logging
------------------

There are two places where you find out what happens at your node:

* The web server logs each request. Since the query is part of the URL, these
  logs show who asked what and when.
* The NodeSoftware logs what happens inside the node, for example errors in
  your query function, and how long things took.

Nodes use the latter primarily in their ``queryfunc.py``, where you set it up
like this::

    import logging
    log = logging.getLogger('vamdc.node.queryfu')

Then any of the following can be used to log messages of different levels::

    log.debug('some text with a variable: %s' % variable)
    log.info('bla')
    log.warning('bla')
    log.error('bla')
    log.critical('bla')

Where these messages end up is configured in ``settings_default.py`` and you
can as usual override the default in the node's own ``settings.py``. For
example, you set the location and name of the log-file like this::

    LOGGING['handlers']['logfile']['filename'] = '/path/to/yourlog.log'

The directory must be writable by the user that runs the node.

.. note::

    Critical errors (using `log.critical()`) are sent to the configured
    admin email address. You need to supply a valid address and make
    sure your server can send emails. The email address that these messages
    are sent from can be set with ``SERVER_EMAIL='vamdcnode@your.server'``.

If you want to turn off the logging of debug messages, you can add the
following for turning them on or off, depending on your global DEBUG setting::

    if not DEBUG:
        LOGGING['handlers']['logfile']['level'] = 'INFO'

For further information see https://docs.djangoproject.com/en/5.2/topics/logging/
