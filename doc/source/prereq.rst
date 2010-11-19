
Software prerequesits and installation
=============================================

Quick start
-----------------

If you use a Linux-distribution like Debian (squeeze) or Ubuntu (some not 
too old version), you can simply run the following commands to install 
all software that you need::

   $ apt-get update && apt-get install python python-django python-pyparsing python-mysqldb apache2 libapache2-mod-wsgi git-core

There are most probably similar packages for other linux distributions. 
All software should be able to be installed on Windows and OSX as well 
but it probably involves some more effort and we unfortunately cannot 
give support for this.

In any case, you can ask us for a virtual machine appliance with 
Debian/Linux and all required software installed. You can then
run this virtual machine on any host computer using either VirtualBox
or VMware.


Python plus some modules
--------------------------------

Python is a wide-spread, open-source, object-oriented, 
dynamically-typed, interpreted programming language. You can read all 
about it at http://python.org and there are installation packages
for all operating systems and architectures.

We require Python between (and including) versions 2.5 and 2.7.


Database access library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It depends on your choice of database engine (see below). The two 
choices we primarily support are SQLite (access library comes with 
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

If you have your data already in a relational database, there most 
probably is no need to set up a new one but you instead deploy the node 
software directly on top of it. The list of databases that Django can 
handle is at http://docs.djangoproject.com/en/1.2/ref/databases/

When setting up a new database, we recommend one of the following two

* SQLite http://www.sqlite.org/
* MySQL http://mysql.com/ (or, if ORACLE 
  succeeds in messing MySQL up, the MySQL fork called MariaDB 
  http://mariadb.org/ )



Webserver
---------------

We support the Apache webserver (http://apache.org) with the WSGI module 
(http://code.google.com/p/modwsgi/) as default webserver to deploy a 
node with Django.

However, Django is known to also run in newer webservers like cherokee, 
nginx or lighttpd which are more light-weight and faster.


Git version control
--------------------

This is not a real requirement since you can download the node software 
(see :ref:`source`) directly. However, if you use the git version 
control system (http://git-scm.com/), it becomes easier to update to 
installation and to re-submit your changes.


The node software itself
-----------------------------

See :ref:`source` on how to obtain the source code.
