.. _concepts:

The main concepts behind the implementation
=============================================

The database
----------------

As already mentioned in the :ref:`intro`, data needs to reside in a 
relational database in order to use the node software for a VAMDC node.

The data model
------------------------


TAP services
---------------

TAP stands for *Table Access Protocol* and is a Virtual O 
bservatorystandard definition of a web service. The detailes specs can 
be found `here <http://www.ivoa.net/Documents/TAP/>`_. All VAMDC nodes 
offer their data though a TAP-like interface which means that the URL 
end-points are named like in TAP, the most important being */tap/sync* 
for a data query which returns the data synchronously (in the immediate 
reply). Also the attribute names for submitting a query are strongly 
inspired by TAP so that a query to a single VAMDC node looks like this::

    http://domain.of.your.node/tap/sync/?LANG=VSS1&FORMAT=XSAMS&QUERY=query string

As of writing this, the VAMDC nodes only use and suport the subset of 
the TAP standard that is needed within the VAMDC. Keep in mind that 
users will not primarily query an indivudual node but use a higher level 
tool like the VAMDC portal for querying many nodes at once.

The more detailed specification of the VAMDC variant of a TAP service can be found at the `wiki-page TapXsamsSpecification <http://voparis-twiki.obspm.fr/twiki/bin/view/VAMDC/TapXsamsSpecification>`_.

.. _conceptdict:

The VAMDC dictionary
---------------------

In order to facilitate automated communication, there is a need for a 
set of names that identify a certain type of data. Each name is unique 
and is uniquely associated with a description, a data type, a unit where 
applicable and a (non-mandatory) restriction.

For illustration, let's have a look at one entry of the dictionary:

================= ============= ======================================================================================================== ============== ============= ======
 Keyword            short descr  long description                                                                                         data type      restriction  unit
================= ============= ======================================================================================================== ============== ============= ======
AtomMassNumber     Atomic mass   Atomic mass in Daltons, which is the same as the unified mass units (1Da = 1u = 1.660 538 86 (28) e-27) (Float|Double)  >1            amu
================= ============= ======================================================================================================== ============== ============= ======

It is the first column that contains the *name* that we use globally 
within VAMDC for a certain bit of information. This is what we mean in 
the following when we talk about "global names" or "keywords".

The full VAMDC dictionary is still being worked on and it currently 
resides as a simple table `in the wiki 
<http://voparis-twiki.obspm.fr/twiki/bin/view/VAMDC/VamdcDictionary>`_. 
A tool for selecting subsets and for easier updates of the dictionary is 
a work in progress.


At the nodes, the dictionary is used in the following different ways. 
Note that some keywords do not make sense being used in all three 
cases. Common sense applies.

Note also that the Returnables and Restrictables, as described in the 
following, are different for each node (depending on the data it offers 
and its structure) and need to be written when setting up a new node.

Returnables
~~~~~~~~~~~~~~~~~

Each node keeps a list of global names that we call the *Returnables*. 
This list contains the names associated with the kinds of information 
that a node has to offer. This is list is offered as XML at the 
*tap/capabilities/* URL end point which allows user applications to 
decide wether it is worth to query a certain node for a certain bit of 
data, or not.

The node software stores the Returnables not only as a list of global 
names, but as a list of key-value pairs where the names are the keys and 
the values are the corresponding places of the data in the *data model* 
(see above). This way, the Returnables become a simple one-to-one map 
between the global names, used by all VAMDC nodes, and the node-specific 
layout of the database.

This "translation" is then used, among other things, by the code that 
fills the data into a certain output format which in turn can become 
node-independant. Thereby each Restrictable icorresponds to a certain 
place (a column in table format, or a certain XML tag) in the output 
format.


Restrictables
~~~~~~~~~~~~~~~~~

It is the list of global names that make sense to put contrains on at a 
certain node and therefore tells which names from the dictionary can be 
used in the WHERE-clause of a query to the node (see query language below).

Again, the node software uses the Restrictables as a list of key-value 
pairs where the keys are the global names and the values are the 
corresponding place in the data model. As for the Returnables, this 
one-to-one map of global names to custom data model allows to translate 
between the two - this time when the query is parsed at arrival. The 
code for parsing the query uses this and can thus be re-used by all 
nodes without altering the code.

Requestables
~~~~~~~~~~~~~~~~~

This is used for a future feature of the query language that is not yet 
implemented in the node software. Just mentioning for sake of 
completeness.


The query language
---------------------

The node software uses the 



The XSAMS schema
-------------------

The generic XSAMS generator
------------------------------


The registry
---------------

The portal
---------------
