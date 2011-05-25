.. _tap:

The VAMDC variant of the Table Access Protocol (TAP)
========================================================

"TAP-XSAMS" is the working title for the emerging data-access services that
return data in XSAMS format (ThomasMarquart? suggests that TAP-VAMDC might be a
better title; I'll change this page if I hear voices in favour) The workshops
run by WP6 and WP7 produced prototypes in Django of this kind of service, but
the web-service protocol needs to be defined independently of that prototype,
so that it can be reimplemented where necessary. This is my take on the
protocol, as known so far.

Philosophy
--------------

TAP-XSAMS provides "virtual data". I.e., it associates data-selection criteria,
defined by a query text in a query language TBD, with an archived data-set,
defined by the address to which the query is sent, the two combined in one URL.
Each such URL represents the results of the query as if they had been
pre-computed and stored on a web-server. The data URLs are semi-permanent; they
can be copied between application, bookmarked, emailed to colleagues, etc.

TAP-XSAMS is based on IVOA's Table Access Protocol (TAP). TAP already does
virtual data and allows us to plug in our own query languages and output
formats. We could redefine all parts of the protocol, but that might take a
long time to get right.

Specifics
-------------------

TAP-XSAMS is defined as a web-service protocol. That means that TAP-XSAMS
services are driven by GET and POST requests to HTTP (or HTTPS) URIs. Low-level
details of the protocol are defined by the HTTP RFCs and we don't have to
specify them. Further, the service can be implemented in any language and on
any database engine without breaking interoperability.

TAP-XSAMS is a RESTful protocol. That means that:

* the various parts of a TAP-XSAMS service each have their own URI;
* the requests and replies are not wrapped in SOAP envelopes;
* we choose the data representation as part of this protocol instead of being forced to use XML.

A TAP-XSAMS service must be a valid implementation of the synchronous-query
parts of the TAP protocol (i.e., the part of TAP covering quick queries where
the results are returned directly to the caller). It should also cover the
asynchronous-query part of tap (i.e. the part covering long-running queries
where the results are cached on the server), but we may not need this very
often for VAMDC.

Query language is selectable in TAP services via a parameter on the query. A
TAP-XSAMS implementation must support VAMDC's preferred query-language and
should also support Astronomical Data Query Language (ADQL: basically SQL92).

Output format for data is selectable in TAP services via a parameter on the
query. A TAP-XSAMS implementation must support the XSAMS format and should also
support VOTable format for compatibility with astronomy tools. An
implementation may also support other formats.

TAP services provide a tabular view of the archived data (even when the output
format is not tabular, as with XSAMS) on which to base the query. TAP-XSAMS
implementations must provide a single, standard table, detailed below.
Implementations may provide other tables, and may provide extra, non-standard
columns within the standard tables. Implementations must not redefine columns
that are part of the TAP-XSAMS standard: e.g. they must not use non-standard
scaling or units.

A TAP-XSAMS implementation must provide the "capabilities" and "tables" URIs as
specified in the Virtual Observatory Support Interfaces (VOSI) standard. These
are the we we register the service details without having to type them in by
hand. VOSI-capabilities supplies an XML document stating the service's other
URIs; if you know this VOSI URI you can get all the others. VOSI-tables returns
an XML document stating the DB schema.

HTTP Header Information
-----------------------------

Statistics
~~~~~~~~~~~~~~~

A TAP-XSAMS service should provide information/statistics about the amount of
data that will be returned for a specific query in the HTTP headers of the
reply to the query. This allows a user (e.g. the portal) to use the HEAD method
(instead of GET) on the same query-URL to gather information before the query
is acutally executed and the data transferred.

The names of the headers to be used are

* VAMDC-COUNT-SPECIES
* VAMDC-COUNT-SOURCES
* VAMDC-COUNT-STATES
* VAMDC-COUNT-COLLISIONS
* VAMDC-COUNT-RADIATIVE
* VAMDC-COUNT-NONRADIATIVE

Their values should be the count of the corresponding blocks in the XSAMS
schema, e.g. the number of radiative transitions that will be returned for this
query. With a reasonable database layout the nodes should easily be able to
gather these numbers by running COUNT queries on their corresponding tables.

Volume limitation
~~~~~~~~~~~~~~~~~~~~~

A TAP-XSAMS service can limit the amount of data it returns via the synchronous
interface, for example to prevent the fetching of the whole database or for
performance reasons. The service must then fill the HTTP-header of the response
with the field VAMDC-TRUNCATED that contains the percentage that the returned
data represent with respect to the total amount available for that query. It is
up to each service to decide both where to put the limit and how to implement
it, for example the number of states or transitions.

As of 2010-10-14, this is implemented for the Django-based prototypes and
activated for the VALD node which now returns max 1000 transitions (plus
corresponding states and sources, of course). Similar limits are easily done
for the other nodes in a few lines of code. In addition to the HTTP-header, the
XSAMS generator also puts a comment into the beginning of the XML-document
which also notifies of the truncation.

For example, a query like this::

    wget -S -O bla.xml "http://vamdc.fysast.uu.se:8888/node/vald//tap/sync/?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+*+WHERE+RadTransWavelengthExperimentalValue+%3E%3D+4000.0+AND+RadTransWavelengthExperimentalValue+%3C%3D+5002.0"

will show the HTTP-header as::

    VAMDC-TRUNCATED: 2.9 %

and at the top of the returned XML, you will find::

    <!--
      ATTENTION: The amount of data returned has been truncated by the node.
      The data below represent 2.9 percent of all available data at this node that
      matched the query.
    -->

