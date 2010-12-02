.. _newnode:

Step by step guide to a new VAMDC node
======================================

Let's have a look at the structural diagram from the :ref:`intro` once more:

.. image:: nodelayout.png
   :width: 700 px
   :alt: Structural layout of a VAMDC node

If you have followed the instructions of the page on :ref:`prereq`, you 
are done with the yellow box in the figure. This page will tell you 
first how to configure and write the few code bits that your node needs 
before running, and then how to deply the node.

Getting the ingredients in place
---------------------------------

The main directory of your node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's give the directory which holds your copy of :ref:`source` (it is 
called NodeSoftware and exists whereever you ran the *git clone* 
command, unless you moved it elsewhere and/or renamed it, which is 
absolutely no problem) a name and call it *$VAMDCROOT*.




The data model and the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With *data model* we mean the piece of Python code that tells Django the 
layout of the database, including the relations between the tables. By 
*database* we mean the actual relational database that is to hold the 
data.

There are two basic scenarios to come up with these two ingredients. 
Either the data are already in a relational database, or you want to 
create one.

Case 1: Existing database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to deply the VAMDC node software on top of an existing 
relational database, the *data model* for Django can be automatically 
generated.


Case 2: Create a new database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The query routine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The dictionaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Deploying the node
------------------------------
