.. _prereq:

Software prerequesits and installation
=============================================

Quick start
-----------------

If you use a Linux-distribution like Debian (squeeze) or Ubuntu (some 
not too old version), you can simply run the following command (with 
root-rights) to install all software that you need::

   $ apt-get update && apt-get install python python-django python-pyparsing python-mysqldb apache2 libapache2-mod-wsgi git-core ipython

There are most probably similar packages for other linux distributions. 
All software should be able to be installed on Windows and OSX as well 
but it probably involves some more effort and we unfortunately cannot 
give support for this.

In any case, you can ask us for a virtual machine appliance with 
Debian/Linux and all required software installed into it. You can then
run this virtual machine on a host computer, using either VirtualBox
or VMware which are available for free on most operating systems.

If the command above worked, you might want to skip to :ref:`testprereq` 
below. Otherwise continue reading for a list of the individual software 
dependencies..

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

Django is the Python-based web-framework that we use to run the services 
(see :ref:`intro` and http://djangoproject.com). We use Django 1.2.X 
where X is the latest bug-fix version number.

The packaged version of your OS might be outdated. In this case follow the 
installation instructions on the Django website.

Database engine
------------------

If the data that your node should serve reside already in a relational 
database, there is most probably no need to set up a new one but you 
instead deploy the node software directly on top of the existing 
database. The list of databases that Django can handle can be found at 
http://docs.djangoproject.com/en/1.2/ref/databases/

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
not wrtten to, during standard operation.

Webserver
---------------

We support the Apache webserver (http://apache.org) with the WSGI module 
(http://code.google.com/p/modwsgi/) as default webserver to deploy a 
node with Django.

Django is known to also run in newer webservers like cherokee, nginx or 
lighttpd which are more light-weight and faster. We did in any case not 
find the web server to be a bottleneck for the performance.


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

