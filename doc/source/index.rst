.. _frontpage:

============================================
Documentation for the VAMDC node software.
============================================

.. toctree::
   :maxdepth: 1

   intro
   concepts
   prereq
   newnode
   importing
   deploy
   virtmach
   addit
   contact
   modules

PDF
========

A PDF-version of this page is available at http://vamdc.tmy.se/doc/nodesoftware.pdf.

Changelog
=================

May 23, 2011
------------------

These are the most important changes for the `11.5` release of the NodeSoftware:

**Update to Django 1.3**. You probably need to upgrade your installation of Django. Read how to at

**Logging**

**Email**

**Example query**

**Volume estimate**

**Other Header changes**

**Dictionary changes**

**Error handling in urls.py**


March 10, 2011
------------------

The chapter :ref:`concepts` now has more detail on the XSAMS schema.

A large part of the XML/XSAMS generator has been rewritten, both to comply with
the new version of the schema (http://tmy.se/xsams) and in terms of its
structure. In addition the keywords in the VAMDC dictionary have changed
somewhat. This means that **you will probably need to update your query
function and dictionaries when you update the NodeSoftware.**

:ref:`newnode` has been updated and extended accordingly.

A new version of the :ref:`Virtual Machine <virtmach` has also been uploaded,
containing the latest NodeSoftware and operating system.

February 2011
-----------------

The deployment of nodes is now covered in more detail at :ref:`deploy`.

Index and search
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


