.. _prereq:

Software prerequisits and installation
=============================================

Quick start
-----------------

On a current Debian or Ubuntu server, this gets you everything::

   $ sudo apt update && sudo apt install git curl
   $ curl -LsSf https://astral.sh/uv/install.sh | sh
   $ git clone https://github.com/VAMDC/NodeSoftware.git
   $ cd NodeSoftware
   $ uv sync

``uv`` (https://docs.astral.sh/uv/) installs the Python version and the
packages that the NodeSoftware needs, as listed in ``pyproject.toml``, into the
directory ``.venv`` inside the NodeSoftware. Nothing is installed system-wide,
so it does not interfere with other software on the server. You then run
commands with ``uv run``, e.g. ``uv run python manage.py test`` in a node
directory. If your node
uses MySQL/MariaDB or PostgreSQL, add the driver with ``uv sync --extra
mysql`` or ``uv sync --extra postgres``.

Without uv, a virtual environment of Python's own does the same::

   $ python3 -m venv .venv
   $ .venv/bin/pip install -e .

and then use ``/path/to/NodeSoftware/.venv/bin/python`` wherever this
documentation says ``uv run python``.

On macOS and other Linux distributions, the steps are the same once git is
installed.

If the commands above worked, you might want to skip to :ref:`testprereq`.
Otherwise read on for the individual pieces.

Python and its packages
--------------------------------

We require Python 3.11 or newer (tested up to Python 3.13). The Python
packages that the NodeSoftware uses are listed in ``pyproject.toml``. The
main ones are:

* *Django*, the Python-based web framework that runs the services (see
  :ref:`intro` and https://www.djangoproject.com). We use Django 5.2 LTS (Long
  Term Support, with security fixes until April 2028).
* *pyparsing*, for parsing the queries.
* *gunicorn*, which runs the node on a server, see :ref:`deploy`.
* the driver for your database: SQLite support comes with Python itself;
  for MySQL/MariaDB it is *mysqlclient*, for PostgreSQL *psycopg2*.

Install them from ``pyproject.toml`` as shown above rather than from your
Linux distribution's packages, which often have other versions.

IPython (https://ipython.org) is a nicer interactive Python shell that
``manage.py shell`` uses if it is installed.

Database engine
------------------

If the data that your node should serve reside already in a relational 
database, there is most probably no need to set up a new one but you 
instead deploy the node software directly on top of the existing 
database. The list of databases that Django can handle can be found at
https://docs.djangoproject.com/en/5.2/ref/databases/

When setting up a new database, we recommend SQLite (https://sqlite.org).
It needs no database server, the whole database is a single file, and it
handles large data sets well as long as the database is only read during
operation, which is the case for a VAMDC node. The VALD node, for example,
serves a 60 GB SQLite database. MySQL/MariaDB (https://mariadb.org) or
PostgreSQL are good choices if the data are in such a database already, or
if other programs write to the database while the node runs. See also
:ref:`importing`.

Webserver
---------------

On a server, the node runs with *gunicorn* behind a web server such as
*nginx*, *Caddy* or *Apache*. This is covered in :ref:`deploy`.

Git version control
--------------------

This is not a real requirement since you can download the node software 
(see :ref:`source`) directly. However, using the version control system 
*git* (https://git-scm.com/), it becomes easier to update your 
installation and to re-submit your changes.


.. _testprereq:

Test your installation
----------------------------

None of the following commands should give you an error::

    $ cd /path/to/where/you/downloaded/NodeSoftware
    $ cd nodes/ExampleNode
    $ cp settings_example.py settings.py
    $ uv run python manage.py test
    $ uv run python manage.py shell

The last command will open an interactive Python shell for you (IPython, 
if you have it installed, otherwise standard Python) and in there you 
should be able to run::

    >>> from node.models import *
    >>> import vamdctap
    >>> exit()


If any of this fails, please make sure you have installed all of the 
above correctly and ask your system administrator for help. For 
contacting us, see :ref:`contact`.

.. note::
	The above only tests that you have installed the software
	correctly, not the setup and configuration of the node in
	question.


.. _upgrading:

Upgrading
========================

Keep your node up to date with the master branch of the repository on GitHub.
This matters for security: in November 2026 a hole was closed that let a
crafted query run code on nodes that use the old helper function *where2q()*,
see :ref:`changes`.

**Before you start**, back up your node directory (``nodes/YourDBname``),
including ``settings.py``, which is not part of the repository, and your
database if it lives in a file like ``node.db``.

**With git** (recommended), in the directory where you cloned the
NodeSoftware::

    $ git pull
    $ uv sync

``git pull`` keeps your own changes to the node directory and tells you if they
collide with changes in the repository.

**Without git**, download
https://github.com/VAMDC/NodeSoftware/archive/refs/heads/master.zip, unpack it
next to your old installation, copy your node directory into its ``nodes/``
directory, then run ``uv sync`` in the new installation. Unpacking the archive
on top of the old installation does not remove files that have been deleted in
the meantime, so we advise against it.

``uv sync`` installs the Python packages in the versions listed in
``pyproject.toml``, including Django. Without uv, ``.venv/bin/pip install -e .``
does the same; a plain ``pip3 install --upgrade django`` may give you a newer
Django than the NodeSoftware supports.

**Afterwards**, restart the node, e.g. ``sudo systemctl restart
yournode.service``, and check that it still answers your example queries.
Running ``./manage.py test`` in your node directory helps if you have
written tests for it, see the ExampleNode.

.. note::

    **Upgrading from a version older than 2025.** Since November 2025 the
    NodeSoftware requires Python 3.11 or newer and Django 5.2. If your node
    ran on Python 2 (all versions before May 2017) or on an old Django, the
    common code will work after the upgrade but your node's own files will
    probably not. Typical changes are ``print`` as a function,
    ``except X as e``, ``key in dict`` instead of ``dict.has_key(key)``,
    ``urlpatterns`` as a plain list in ``urls.py``, an ``on_delete`` argument
    on every ``ForeignKey`` and Django migrations instead of ``syncdb``. The
    ExampleNode shows the current form of all files; the :ref:`changes` lists
    what changed when.

    If you cannot do this right away, at least make sure that your
    ``node/queryfunc.py`` does not use *where2q()* or *eval()*, see the
    November 2026 entry in the :ref:`changes`.

Everything else
----------------

If you have installed all the prerequisites from Debian or Ubuntu packages as recommended, you can simply run the following regularly to keep your system up to date::

    $ sudo apt update
    $ sudo apt upgrade
