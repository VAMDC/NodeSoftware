.. _prereq:

Software prerequisits and installation
=============================================

Quick start
-----------------

If you use a Linux-distribution like Debian (squeeze) or Ubuntu (some 
not too old version), you can simply run the following command (with 
root-rights) to install all software that you need::

   $ apt-get update && apt-get install python python-pip python-pyparsing python-mysqldb gunicorn nginx git-core ipython
   $ pip install django

This will automagically install some more packages that the above ones 
depend upon. There are most probably similar packages for other linux 
distributions than Debian. All software should be able to be installed 
on Windows and OSX as well but it probably involves some more effort and 
we unfortunately cannot give support for this.

We also provide a virtual machine appliance with Debian/Linux and all required
software installed into it. You can then run this virtual machine on a host
computer, using VirtualBox which is available for free on most operating
systems. See :ref:`virtmach` for more detail on this.

If the commands above worked or you run the virtual machine, you might want to
skip to :ref:`testprereq`. Otherwise continue reading for a list of the
individual software dependencies..

Python plus some modules
--------------------------------

Python is a wide-spread, open-source, object-oriented, 
dynamically-typed, interpreted programming language. You can read all 
about it at http://python.org and there exist installation packages
for all operating systems and architectures.

We require Python between (and including) versions 2.5 and 2.7.

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
:ref:`intro` and http://djangoproject.com). We currently use Django 1.3.X
(where X is the latest bug-fix version number) but newer versions will be
supported as they are released.

The packaged version of your OS is probably outdated. This is why we recommend
to install Django using ``pip`` (see command above). Alternatively follow the
installation instructions on the Django website.

Database engine
------------------

If the data that your node should serve reside already in a relational 
database, there is most probably no need to set up a new one but you 
instead deploy the node software directly on top of the existing 
database. The list of databases that Django can handle can be found at 
http://docs.djangoproject.com/en/1.3/ref/databases/

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

Django
----------

This depends on how you installed Django. With ``pip`` it is enough to run::

    $ pip install --upgrade django


Everything else
----------------

If you have installed all the prerequisites from Debian or Ubuntu packages as recommended, you can simply run the following regularly to keep your system up to date::

    $ apt-get update
    $ apt-get upgrade
