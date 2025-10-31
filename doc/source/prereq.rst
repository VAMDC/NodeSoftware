.. _prereq:

Software prerequisits and installation
=============================================

Quick start
-----------------

If you use a Linux distribution like Debian or Ubuntu, you can simply run
the following commands to install all software that you need::

   $ sudo apt update && sudo apt install python3 python3-pip python3-venv gunicorn nginx git ipython3
   $ pip3 install django pyparsing

For Python database drivers (MySQL, PostgreSQL), install as needed::

   $ pip3 install mysqlclient  # for MySQL
   $ pip3 install psycopg2-binary  # for PostgreSQL

**Recommended: Using uv with pyproject.toml**

For modern Python development, we recommend using ``uv`` as a faster alternative
to pip and virtual environment management. The NodeSoftware includes a
``pyproject.toml`` file that defines all dependencies. Install uv with::

   $ curl -LsSf https://astral.sh/uv/install.sh | sh

Then install dependencies using::

   $ uv sync  # installs dependencies from pyproject.toml
   $ uv run python manage.py  # runs commands in the virtual environment

The ``pyproject.toml`` file is the modern Python standard for declaring project
metadata and dependencies. With uv, it automatically creates and manages a virtual
environment, ensuring isolated and reproducible builds. See https://docs.astral.sh/uv/
for more information.

This will automatically install dependencies. Similar packages exist for other
Linux distributions (Fedora, Arch, etc.). All software can also be installed
on Windows and macOS, though setup details differ.

**Docker Alternative**. For a consistent development environment across platforms,
consider using Docker. A basic Dockerfile in your node directory can encapsulate
all dependencies. See https://docs.docker.com/ for container-based deployment.

If the commands above worked, you might want to skip to :ref:`testprereq`.
Otherwise continue reading for a list of the individual software dependencies.

Python plus some modules
--------------------------------

Python is a wide-spread, open-source, object-oriented, 
dynamically-typed, interpreted programming language. You can read all 
about it at http://python.org and there exist installation packages
for all operating systems and architectures.

We require Python 3.11 or newer (tested up to Python 3.13).

We recommend to also install IPython (http://ipython.scipy.org/), an 
improved interactive shell for Python.

Database access library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This depends on your choice of database engine (see below). The two 
choices we support primarily are SQLite (access library comes with 
Python itself) and MySQL (access library at 
http://pypi.python.org/pypi/MySQL-python/ but preferrably installed by 
your OS's package manager).


PyParsing
~~~~~~~~~~~~~~~~~~~~~~~~~

This is needed for our SQL-parser and you can read about it at 
http://pypi.python.org/pypi/pyparsing

Again, it is best installed via your distribution's package manager.


Django
----------------

Django is the Python-based web-framework that we use to run the services (see
:ref:`intro` and http://djangoproject.com). We currently use Django 5.2 LTS
(Long Term Support release). Future LTS and stable releases will be supported
as they become available.

The packaged version of your OS may be outdated. We recommend installing
Django using ``pip3`` (see command above) or using a virtual environment
for better dependency management. Alternatively follow the installation
instructions on the Django website.

Database engine
------------------

If the data that your node should serve reside already in a relational 
database, there is most probably no need to set up a new one but you 
instead deploy the node software directly on top of the existing 
database. The list of databases that Django can handle can be found at
https://docs.djangoproject.com/en/5.2/ref/databases/

When setting up a new database, we recommend one of the following two

* SQLite http://www.sqlite.org/
* MySQL http://mysql.com/ (or, if ORACLE 
  succeeds in messing MySQL up, the MySQL fork called MariaDB 
  http://mariadb.org/ )

Unless the data set is extremely large and/or complex, the choice 
between the two is of minor importance. SQLite has the advantage of not 
relying on a separate server software and is often on par with MySQL in 
terms of speed. Its limitation in terms of concurrent write access is 
not relevant in our typical use case where the database is only read, 
not written to, during standard operation.

Webserver
---------------

The node software needs to run within a webserver. The two setups that we
successfully tested are *Gunicorn* (together with *nginx*) and the Apache
webserver (with its WSGI module). 

This is covered in more detail in :ref:`deploy`.

Git version control
--------------------

This is not a real requirement since you can download the node software 
(see :ref:`source`) directly. However, using the version control system 
*git* (http://git-scm.com/), it becomes easier to update your 
installation and to re-submit your changes.


The node software itself
-----------------------------

See :ref:`source` on how to obtain the source code.


.. _testprereq:

Test your installation
----------------------------

None of the following commands should give you an error::

    $ python -c "import django"
    $ python -c "import pyparsing"

    $ cd /path/to/where/you/downloaded/NodeSoftware
    $ cd nodes/ExampleNode
    $ ./manage.py 
    $ ./manage.py test
    $ ./manage.py shell

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

NodeSoftware
--------------

The simplest way is to simply download the latest tar.gz-archive and extract it
on top of you previous installation. We however strongly recommend to backup
the files in your node-directory before doing this; alternatively moving the
old NodeSoftware to a different location and then copy the files you need from
there into the new version.

If you instead use our version control system, please see :ref:`gitcollab` on
how to get the latest.

.. note::

    After upgrading the NodeSoftware, you should check that your node is
    still running properly. We cannot (yet) guarantee that you
    need not update your node-specific code to fit the latest version. Larger
    changes will be mentioned in the :ref:`changes`.

Django
----------

This depends on how you installed Django. With ``pip3`` it is enough to run::

    $ pip3 install --upgrade django


Everything else
----------------

If you have installed all the prerequisites from Debian or Ubuntu packages as recommended, you can simply run the following regularly to keep your system up to date::

    $ sudo apt update
    $ sudo apt upgrade
