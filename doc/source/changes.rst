.. _changes:

Changelog
=================

.. _note:

    This chapter will be difficult to understand if you have not read the whole
    document before since terms are used that are introduced later. It is
    meant for returning readers, especially the maintainer of VAMDC nodes.

June 15, 2011
------------------

**Version**. This documentation has been updated to match the release of the
NodeSoftware 11.5r1 which implements the VAMDC Standards release 11.5.
NodeSoftware 11.5r1 supersedes and obsoletes version 11.5 (released May 26) and
all nodes are encouraged to upgrade. This is mainly a bug-fix release and upgraded nodes will only have to do the two small changes mentioned below.

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

**Limitations**. A chapter on the limitations of the NodeSoftware has been addedd to the documentation: :ref:`limitations`

**Dictionary**. The NodeSoftware makes use of dictionary keywords that are not
in the VAMDC Standards 11.5 but will be in the next Standards release (11.7).
If you want to use the NodeSoftware's XML-generator for solids, particles or
molecular quantum numbers, please see http://dictionary.vamdc.org/dict/ for the
new keywords.

**Registration**. The NodeSoftware now automatically reports its own version and the standards version it implements at *tap/capabilities*. You might want to make the VAMDC Registry re-read this information (click "Edit metadata" and "Update the registry entry").

**Virtual Machine**. The virutal machine has been updated to include Django 1.3 and NodeSoftware 11.5r1.

May 26, 2011
------------------

**Version numbers**. As of now, we introduce version numbers for both the standards (XSAMS, VAMDC-TAP, see separate documentation) and for their implementation in the NodeSoftware which is the concern of this document. Version numbers follow the format YY.MMrX where YY is for the year, MM the month, and X an increasing number for bugfix revisions that do not affect the usage of the NodeSoftware.

The most important changes from the perspective of a node-operator who wants to upgrade to this `11.5` release are:

**Update to Django 1.3**. The NodeSoftware now requires Django version 1.3 and node operators probably need to upgrade their installation of Django. See :ref:`upgrading`.

**Email**. Make sure you have set a correct email address in ``settings.py``. It will be used to report critical errors to, including reports on what went wrong.

**Logging**. The capabilities to log debug and error-messages have been extended. See :ref:`logging`. 

**Example query**. As soon as a node becomes operational, please add an example query to its ``settings.py``. It will be used for automated testing. Example::

    EXAMPLE_QUERY = 'SELECT ALL WHERE RadTransWavelength > 4000 AND RadTransWavelength < 4005'

**Volume estimate**. In order to allow the portal (and other queries to your node) to find out how big the resulting XML-output for a particular query will be, nodes should estimate this and relay it via the new HTTP-header `VAMDC-APPROX-SIZE`. The easiest way to do this is to run a test query, determine the outputs size (in MB) and divide it by the number of items (e.g. transitions, if these dominate your results). This number can then be used to estimate the size of any query, see the updated example at :ref:`queryfu`.

**Other Header changes**. The header `VAMDC-COUNT-SPECIES` has been replaced by `VAMDC-COUNT-ATOMS` and `VAMDC-COUNT-MOLECULES`. See the standards documentation for the full definition.

**Error handling in urls.py**. The NodeSoftware has become more error-safe
and tries to handle unexected input and "crashes" more gracefully. You need not care about this, excpet making sure that the following two lines are present at the end of the file ``urls.py`` in your node's main directory::

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
