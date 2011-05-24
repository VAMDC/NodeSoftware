.. _keywords:

The VAMDC dictionary keywords
=================================

In VAMDC, different pieces of software need to communicate to each other. Apart
from protocols and schema, a common vocabulary is needed. By this we mean a
list of "global keywords" that should consist of reasonably short,
human-readable keywords which uniquely define a certain type of information or
data. In the following we describe how the keywords were created and how they
are used in different parts of VAMDC software. The common gain in the various
aspects is that the vocabulary allows to split the tasks that are common to all
data sets from the database-specific information and routines. Thereby it
becomes possible to implement software that can be re-used by multiple
datasets, reducing the deployment on a new data set to implementing the parts
that are truly specific for it. 

The full VAMDC dictionary with all the keywords can be viewed at
http://vamdc.tmy.se/dict/

The Keywords
-----------------------------

In order to compile a list of well-defined names for all kinds of information
that VAMDC datasets can contain, we started from the XSAMS schema for atomic
and molecular data. After flattening the XML structure and removing the tags,
redundant information was removed by hand, however keeping a reflection of the
original hierarchy in the name. For example, all keywords that belong to a
radiative transition start with RadTrans, atmonic state information with
AtomState and so on. Examples of full keywords are AtomStateLandeFactor,
SourceAuthorName, MolecularSpeciesIonCharge.

The vocabulary of keywords is as of this date unfinished and will be subject to
future revision. Already now there have been keywords added that are not
represented in the XSAMS schema and probably more will follow when more and
more databases are included. In addition, a simplification of certain parts
should be possible in order to avoid an unnecessarily large number of entries.


Use of Keywords in Data Output
---------------------------------

With the list of global keywords, it is possible to write generic software for
handling data, where "generic" means that it can run on not only one specific
data set. This is achieved by using only the global names in the to-be-reused
parts of the code, not caring about the data model of a specific data set. A
smaller piece of code, custom for each data set, then takes care of translating
the global names into the local representation of the current data set.

This allows for example to write a generator for XML-output in XSAMS format,
that can be re-used by many databases. It basically defines where in the schema
data that corresponds to a certain keyword should be placed. Since this
generator needs to digest the query result which is in a database-specific
structure, we implement a simple "translation dictionary". This dictionary,
called RETURNABLES, consists of key-value-pairs where the keys are the global
names from the list that have data in the current database. The corresponding
values for each key contain the information about where in the structures that
the database-query returns the actual value can be found. The generic part of
the code can then use this information to replace the global keywords in the
XML-document with the right values.

A data output generator like this has been implemented and tested. It can
produce complete data output for at least one of the VAMDC databases and will
be completed to cover the remaining parts.  Of course, almost any other return
format (e.g. VO-tables) can also be implemented this way and thereby become
usable for VAMDC databases.

Use of Keywords in the Query Language
------------------------------------------

The details of the query language, which is used to transmit a request from the
VAMDC portal to the data nodes, are yet to be specified. The use of a SQL-like
query language is likely. Using the global keywords in the query language is
obvious and provides immense value: By giving global keywords in the query
(instead of table names and columns which differ between databases) the query
itself becomes universal. This means that the portal does not need to know how
to query each data set but can instead send the same query to all nodes which
in turn are expected to understand the keywords that are relevant for it.

An example query can look like this::

    SELECT * WHERE RadTransWavelength < 3000 AND RadTransWavelength > 2500 AND AtomNuclearCharge - 25 AND AtomIonCharge < 2

Each data set must, when it receives such a query, know how to make use of the
global keywords. We need to allow for maximum flexibility here, since a
complicated internal representation of data may result in a non-trivial way to
run the query on the database. The most straight-forward way to translate the
query to the data-specific format is similar to the data output mentioned
before: A dictionary, this time called RESTRICTABLES, of key-value pairs that
contains the mapping between the global keywords and the local data model. Note
that the RETURNABLES-dictionary can not be re-used for this purpose because the
internal format can differ from the query to the output.

We have implemented an parser in our prototype that splits the logical parts of
the SQL-sentence. We also provide functions that translate the
WHERE-restrictions with global keywords into internal query-objects which in
turn can be run on the local data model.

Units
--------------------

VAMDC does not enforce the use of a certain unit for a certain physical
quantity. However, in order to make queries like the example above understood
by all nodes, the keywords that are used as RESTRICTABLE have a default unit
(see http://vamdc.tmy.se/dict/) which is the one used in the query. This means
that each node must be aware and convert the query to its internal unit before
executing the query. However it is not necessary to convert the node's data to
the default unit before returning them.


Use of Keywords for the Registry
--------------------------------------

The two aforementioned dictionaries RETURNABLES and RESTRICTABLES contain the
most important information about each data set in the form of global keywords:
what kind of data is contained in the database and which of these make sense to
restrict in the query. By using only the keys in these key-value pairs we can
compile this information in a format (XML-template) that the registry
understands. Once this extension to the registry is specified, the portal will
be able to decide from the information in the registry which databases might
have a sensible answer to a particular query and only send it to these.

Implicit Keywords
---------------------

for DataType etc.


Sub-dictionaries
---------------------

function names
~~~~~~~~~~~~~~~~~~~~~~~~

Broadening types
~~~~~~~~~~~~~~~~~~~~~~~~~~
