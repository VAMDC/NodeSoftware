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


The main directory of your node
---------------------------------

Let's give the directory which holds your copy of :ref:`source` (it is 
called NodeSoftware and exists whereever you ran the *git clone* 
command, unless you moved it elsewhere and/or renamed it, which is 
absolutely no problem) a name and call it *$VAMDCROOT*. Let's also assume
the name of the dataset is *YourDBname*.

Inside $VAMDCROOT you find several subdirectories. For setting up a new
node, you only need to care about the one called *nodes/*. The very first thing to do, is to make a copy of the ExampleNode::

    $ export $VAMDCROOT=/path/to/where/you/downloaded/NodeSoftware
    $ # (the last line is for Bash-like shells, for C-Shell use *setenv* instead of *export*
    $ cd $VAMDCROOT/nodes/
    $ cp -a ExampleNode YourDBname
    $ cd YourDBname/
 
Inside your node directory
---------------------------------

The first thing to do inside your node directory is to run::

    $ ./manage.py

This will generate a new file *settings.py* for you. This file is where 
you override the default settings which reside in *settings_default.py*. 
There are three configurations items that you need to fill

* The information on how to connect to your database.
* The URL at which the node will be accessible later
* A name and email address for the node administrator(s).

You can leave the default values for now, if you do not yet know what to 
fill in.

There are only three more files that you will need to care about:

* *node/models.py* is where you put the database model,
* *node/dictionaries.py* is where you put the dictionaries and
* *node/queryfunc.py* is where you write the uery function,

all of which will be explained in detail in the following.

The data model and the database
---------------------------------

With *data model* we mean the piece of Python code that tells Django the 
layout of the database, including the relations between the tables. By 
*database* we mean the actual relational database that is to hold the 
data.

There are two basic scenarios to come up with these two ingredients. 
Either the data are already in a relational database, or you want to 
create one.

Case 1: Existing database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to deply the VAMDC node software on top of an existing 
relational database, the *data model* for Django can be automatically 
generated.


Case 2: Create a new database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The dictionaries
----------------------------------


The query routine
-----------------------------------


This file must implement a function called setupResults() which 
takes the parsed SQL from the query parser. setupResults() must pass 
the restrictions on to one or several of your models (depending on 
the database strcture) and also fetch the corresponding items from 
other models that are needed in the return data. setupResults() must 
return a DICTIONARY that has as keys some of the following: Sources 
AtomStates MoleStates CollTrans RadTrans Methods; with the 
corresponding QuerySets as the values for these keys. This 
dictionary will be handed into the generator an allow it to fill the 
XML schema.

Below is an example, inspired by VALD that has a data model like 
this:

* One for the Sources/References
* One for the Species
* One for the States (points to Species once, and to several 
  references)
* One for Transitions (points twice to States (upper, lower) and to 
  several Sources)

In this layout, all restrictions in the query can be passed to
the Transitions model (using the pointers between models to
restrict eg. Transition.species.ionization) which facilitates
things.

Now we can code two helper functions that get the corresponding
Sources and States to a selection of Transitions:




Deploying the node
------------------------------
