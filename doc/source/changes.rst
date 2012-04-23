.. _changes:

Changelog
=================

.. note::
    This chapter will be difficult to understand if you have not read the whole
    document before, since terms are used that are introduced later. It is meant
    for returning readers, especially the maintainers of VAMDC nodes.

April 23, 2012
---------------------

**Version 11.12r2**. This is a bugfix-release of the NodeSoftware, implementing the VAMDC standards 11.12. There are no major internal changes that should require updating the code that is specific for each data node.

**Django 1.4**. A new version of Django, the framework that we build upon, has been released. With the few changes contained in this release, deployment should not break when upgrading to Django 1.4 and we encourage all nodes to do so. (However staying at 1.3 for a while is no security risk.) If you installed Django via `pip` as recommended later in this document, upgrading is as simple as::

    pip install --upgrade django



February 13, 2012
---------------------

**Version**. This is for *NodeSoftware 11.12r1* which is the first bugfix-release for version 11.12 released before.

No major internal changes that require updating the code that is specific for each node, except:

**NormalModes**. Previously, the NormalModes in the atomic state composition of XSAMS were wrongly attached to each Atom object, now they need to be handed to the generator as ``AtomState.NormalModes``. This means that nodes which use this part of the schema need to update their query-function.

January 22, 2012
----------------------

**Version**. This is for *NodeSoftware 11.12* which implements the VAMDC
standards 11.12. (Please make sure to also read the changes for the beta
release below.)

Since the beta-release (11.10beta), there are no major changes of the internal
workings, which means that you most likely do not need to change the
query-function if it worked with that. However, please test your node after an
upgrade anyway.

**Dictionary**. Some keywords have changed, both Restrictables and Returnables
(due to the changes in the schema), so please double-check the node's
``dictionaries.py`` against http://dictionary.vamdc.org/.

**DEPLOY_URL**. You can now override the automatic determination of the URL at
which a node is deployed, see :ref:`deployurl`.

**New IDs**. The XSAMS standard now makes mandatory several IDs in an XSAMS
document, for example each process must have an ID now. Please read
:ref:`fillingids` on how to do this.

**Advanced treatment of Restrictables**. If a node wants to support a
Restrictable that does not match a field in the database, this can now be
handled with some custom code. See :ref:`specialrestr`.

**Finding the bug**. For debugging purposes, it may help to manually go through
the steps that happen when a query comes to a node. See :ref:`debugntest` for
information on how to do this.

**Self-referencing <Source>**. In the bibliographical part of the XSAMS schema,
i.e. the <Source> elements, the xml-generator now automatically adds such an
element in order to describe the document itself. It contains a timestamp and
the full query URL, among other things. Please check the output if this works
correctly for your node.

Last, but not least, since we often are asked how to test a node, we'd like to
mention that there is a very convenient software called **TAPvalidator** (see
http://www.vamdc.org/software) which can be used to query a node, browse the
output and check that it is valid with respect to the xsams standard.


September 30, 2011
---------------------

**Version**. This is for *NodeSoftware 11.10beta*, which has most of the changes
for the upcoming 11.10 standards release and is aleady more robust than
previous releases. All nodes are encouraged to upgrade.

**Query functions**. The standard way of starting a node's query function has
changed: the function *where2q()* is superseded by *sql2Q()*. **This means you
should change this in your code!** See the updated example in :ref:`queryfu`.

**Requestables**. Queries to the nodes can now ask to return only a certain
part of the XML document, for example "SELECT Spiecies WHERE ..." instead of
"SELECT ALL WHERE ...". This works behind the scenes, but a node's query
function might want to skip some of the work, see :ref:`manualrequestables`

**Returnables**. Many Returnables (e.g. all that correspond to a DataType in
the XML schema) now can receive vectors which allows to give several values of
the same quantity. See :ref:`specialreturnable` on how to do this.

**Unit conversions**. Each Restrictable has a default unit in which the queries
are formulated. If a node's database has the quantity in a different unit, the
value in the query needs to be converted to the internal unit. There is now a
comfortable mechanism to do this, see :ref:`unitconv`

**Dictionaries**. While we're at Restrictables, it is good to keep in mind that
a node is the more useful the more Restrictables it supports, simply because it
will be able to answer a higer fraction of queries. All nodes that have data
about radiative transitions are **highly encouraged** to support
RadTransWavelength, even if they internally keep frequency or wavenumber. Some
clients, like the current portal, made the choice to always use wavelength.

**Restrictable prefixes**. Apart from the Requestables (see above) the second
major addition in the query language VSS2 is that Restrictables can have
prefixes, separated by a dot from the usual keyword. For example *SELECT *
WHERE Upper.AtomStateEnergy > 13*. See the standard documentation for all
available prefixes. Currently the easiest way for a node to support these is to
treat them as separate Restrictables in ``dictionaries.py``. This becomes
tricky for collisions where the prefixes allow to group Restrictables to belong
to reactants and/or products. Since this very much depends on the individual
node, there are currently no specific tools for this, but we are certainly open
for ideas on how to solve this.

**Special Restrictables**. If a node needs to handle one or more Restrictables
as special cases, for example because the corresponding value is not in the
database, this is certainly possible. See :ref:`specialrestr`

**Custom return formats**. This goes beyong the VAMDC standard but if you are
interested to return other formats from your node, you can have a look at
:ref:`returnresult`.

The section on :ref:`logging` has been extended as well and a few notes about
:ref:`moredjango` were added.


June 15, 2011
------------------

**Version**. This documentation has been updated to match the release of the
NodeSoftware 11.5r1 which implements the VAMDC Standards release 11.5.
NodeSoftware 11.5r1 supersedes and obsoletes version 11.5 (released May 26) and
all nodes are encouraged to upgrade. This is mainly a bug-fix release and
upgraded nodes will only have to do the two small changes mentioned below.

**Example Queries**. The way to define example queries in each node's
``settings.py`` has changed in order to allow several of them. They will be used
for automated testing and are as of this version returned to the VAMDC
registry. New example::

    EXAMPLE_QUERIES = [\
        'SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4005',
        'SELECT ALL WHERE AtomSymbol = "Fe"',
        ]

**CaselessDict**. The import and use of `CaselessDict` in the nodes'
``dictionaries.py`` or ``queryfunc.py`` is not longer necessary and should be
removed.

**Limitations**. A chapter on the limitations of the NodeSoftware has been
addedd to the documentation: :ref:`limitations`

**Dictionary**. The NodeSoftware makes use of dictionary keywords that are not
in the VAMDC Standards 11.5 but will be in the next Standards release (11.7).
If you want to use the NodeSoftware's XML-generator for solids, particles or
molecular quantum numbers, please see http://dictionary.vamdc.org/dict/ for the
new keywords.

**Registration**. The NodeSoftware now automatically reports its own version
and the standards version it implements at *tap/capabilities*. You might want
to make the VAMDC Registry re-read this information (click "Edit metadata" and
"Update the registry entry").

**Virtual Machine**. The virutal machine has been updated to include Django 1.3
and NodeSoftware 11.5r1.

May 26, 2011
------------------

**Version numbers**. As of now, we introduce version numbers for both the
standards (XSAMS, VAMDC-TAP, see separate documentation) and for their
implementation in the NodeSoftware which is the concern of this document.
Version numbers follow the format YY.MMrX where YY is for the year, MM the
month, and X an increasing number for bugfix revisions that do not affect the
usage of the NodeSoftware.

The most important changes from the perspective of a node-operator who wants to
upgrade to this `11.5` release are:

**Update to Django 1.3**. The NodeSoftware now requires Django version 1.3 and
node operators probably need to upgrade their installation of Django. See
:ref:`upgrading`.

**Email**. Make sure you have set a correct email address in ``settings.py``.
It will be used to report critical errors to, including reports on what went
wrong.

**Logging**. The capabilities to log debug and error-messages have been
extended. See :ref:`logging`. 

**Example query**. As soon as a node becomes operational, please add an example
query to its ``settings.py``. It will be used for automated testing. Example::

    EXAMPLE_QUERY = 'SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4005'

**Volume estimate**. In order to allow the portal (and other queries to your
node) to find out how big the resulting XML-output for a particular query will
be, nodes should estimate this and relay it via the new HTTP-header
`VAMDC-APPROX-SIZE`. The easiest way to do this is to run a test query,
determine the outputs size (in MB) and divide it by the number of items (e.g.
transitions, if these dominate your results). This number can then be used to
estimate the size of any query, see the updated example at :ref:`queryfu`.

**Other Header changes**. The header `VAMDC-COUNT-SPECIES` has been replaced by
`VAMDC-COUNT-ATOMS` and `VAMDC-COUNT-MOLECULES`. See the standards
documentation for the full definition.

**Error handling in urls.py**. The NodeSoftware has become more error-safe and
tries to handle unexected input and "crashes" more gracefully. You need not
care about this, excpet making sure that the following two lines are present at
the end of the file ``urls.py`` in your node's main directory::

    handler500 = 'vamdctap.views.tapServerError'
    handler404 = 'vamdctap.views.tapNotFoundError'

**Dictionary changes**. Since the XSAMS-schema has changed, so have the
dictionary keywords, especially in the Broadening-part of radiative transitions
and the atomic quantum numbers. Also new keywords have been added for the bits
that are newly implemented in the XML-generator.

**Stricter format for accuracies**. In compliance with XSAMS' new way of
defining a value's accuracy, the keywords that are not explicity given for
`DataTypes` have become more. Any word `SomeKeyword` that is marked as a
`DataType` in the dictionary allows for use of the following words as well:
SomeKeywordUnit, SomeKeywordRef, SomeKeywordComment, SomeKeywordMethod,
SomeKeywordAccuracyCalibration, SomeKeywordAccuracyQuality,
SomeKeywordAccuracySystematic, SomeKeywordAccuracySystematicConfidence,
SomeKeywordAccuracySystematicRelative, SomeKeywordAccuracyStatistical,
SomeKeywordAccuracyStatisticalConfidence,
SomeKeywordAccuracyStatisticalRelative, SomeKeywordAccuracyStatLow,
SomeKeywordAccuracyStatLowConfidence, SomeKeywordAccuracyStatLowRelative,
SomeKeywordAccuracyStatHigh, SomeKeywordAccuracyStatHighConfidence,
SomeKeywordAccuracyStatHighRelative. See also the standards documentation.

.. note::

    The last two points mean that you probably have to update your ``dictionaries.py``.

March 10, 2011
------------------

The chapter :ref:`concepts` now has more detail on the XSAMS schema.

A large part of the XML/XSAMS generator has been rewritten, both to comply with
the new version of the schema and in terms of its
structure. In addition the keywords in the VAMDC dictionary have changed
somewhat. This means that **you will probably need to update your query
function and dictionaries when you update the NodeSoftware.**

:ref:`newnode` has been updated and extended accordingly.

A new version of the :ref:`virtmach` has also been uploaded,
containing the latest NodeSoftware and operating system.

February 2011
-----------------

The deployment of nodes is now covered in more detail at :ref:`deploy`.
