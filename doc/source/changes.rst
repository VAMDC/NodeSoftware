.. _changes:

Changelog
=================

May 26, 2011
------------------

**Version numbers**. As of now, we introduce version numbers for both the standards (XSAMS, VAMDC-TAP, see separate documentation) and for their implementation in the NodeSoftware which is the concern of this document. Version numbers follow the format YY.MMrX where YY is for the year, MM the month, and X an increasing number for bugfix revisions that do not affect the usage of the NodeSoftware.

The most important changes from the perspective of a node-operator who wants to upgrade to this `11.5` release are:

**Update to Django 1.3**. The NodeSoftware now requires Django version 1.3 and node operators probably need to upgrade their installation of Django. See :ref:`upgrading`.

**Logging**

**Email**. Make sure you have set a correct email address in ``settings.py``. It will be used to report critical errors to, including reports on what went wrong.

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

Known limitations
==================

To be addressed in the 11.8 release

* The "Cases" for molecular quantum numbers are not yet implemented in the XSAMS-generator (but can be included with the hook for custom XML).
* Tools for treating certain Restrictables as special cases for a flexible
* 
