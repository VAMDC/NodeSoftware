.. _querylang:

The VAMDC query language
==========================

VSS1
-----------

The VAMDC-standard query language, or languages, will be specified here when we
know what we need.

So far, we have discussed SQL/ADQL with standard operands (proposed at the Koln
meeting) and an XML vocabulary for tightly-focused queries (proposed by
Christian Hill via email).

Given the stipulations in previous sections, the language must be compact
enough to embed as a parameter in a virtual-data URI.  Proposal: VAMDC
SQL-subset 1

Currently, the only known, working implementation of TAP-XSAMS uses a tiny
subset of SQL. This is almost certainly all we'll have for the level-1 release,
so I propose to formalize it as follows, under the name VSS1 for "VAMDC
SQL-subset 1".

VSS1 is a subset of SQL92 and uses the basic syntax of that language.

The SELECT verb is included in VSS1, but no other verbs: UPDATE, CREATE, ALTER,
DROP et al. are not part of VSS1. This means that a VSS1 statement can't alter
the database to which is is applied.

VSS1 has no FROM clause. All queries apply to the single, standard table
defined as part of the TAP-XSAMS standard.

VSS1 includes the WHERE clause.

All the following are excluded from VSS1: joins; ORDER BY; GROUP BY;
sub-queries (HAVING clause etc.); CORRESPONDING; UNION; EXCEPT; INTERSECT.

The COUNT and TOP keywords are not part of VSS1.

Derived columns (e.g. ratios of database columns) are not part of VSS1.

A service that supports VSS1 must process as SQL92 all queries presented as
VSS1 (e.g. TAP requests with LANG=VSS1) which are correct SQL92, with the
following exceptions.

Where the query uses language features outside the sub-set specified above, the
service may reject the query. If it does not reject the query then the service
must process it as SQL92.

Where the output is to XSAMS, selection of database columns in the query is
inappropriate: it could lead to query results that cannot be represented in
valid XSAMS. For such queries, the service may ignore the column selection in
the query and proceed as if the query had been "SELECT \*". If the service does
not make this substitution, it must either produce valid output in XSAMS or
reject the query; the service must not produce an XSAMS output that is invalid
because it is incomplete.

VSS1 is a very small sub-set of SQL and doesn't support "clever" or advanced
queries. This is deliberate: it's a very-basic language for the TAP-XSAMS
web-services where the data are pre-joined and simple queries should be enough
for most of the use-cases. If we need a language for some other use that is
smaller than SQL92 but more capable than VSS1, then let's define VSS2, VSS3
etc. rather than bloating VSS1. We can always retire VSS1 later in the VAMDC
project if we no longer like it.

Standard view of data
~~~~~~~~~~~~~~~~~~~~~~~~~~

TAP-XSAMS includes a standard view of the underlying database with standard and
column names, such that the same query can work on all services of the type.
The view looks to the client like a single table and may be implemented in any
way that achieves this. E.g., it may be implemented as a basic table (i.e.
holds a copy of the data), as a RDBMS view onto existing tables (i.e. doesn't
copy the data, but derives them from other tables on demand) or as a
materialized view (i.e. caches the data but can easily regenerate them to match
a change in the source tables).

This standard table is intended to be addressed using the VSS1 language, above.
Queries in that language do not state the name of the target table (they are
implicitly targeted at the standard table), so the actual name of the table is
not important: TAPXSAMS is suggested.

The columns of the standard table are still work in progress and are described
at GlobalKeywordsAndQueryLanguage.

Examples of virtual-data URIs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TAP looks complicated when you skim its specification but the external face is
really quite simple. Suppose you have a TAP-XSAMS service registered to a base
URI of http://some.server/some/path then the following are possible URIs for
query results.

This is a basic query in the VAMDC-standard language with XSAMS output::

    http://some.server/some/path/sync?REQUEST=doQuery&LANG=VAMDC1&FORMAT=XSAMS&QUERY=select%20*%20from%20xsams

Here I've guessed at some of the undecided issues in the specification above:

There's a VAMDC-standard language called "VAMDC1" and it's basically SQL92.

The standard DB-schema in TAP-XSAMS is based on a table (or RDBMS view) called
"xsams".

The spaces in the query text get escaped to "%20" when the query is embedded in
the URI. The query is really "select * from xsams". A better query would set
some selection constraints: "select * from xsams where ...".

This is the same query with VOtable output:

http://some.server/some/path/sync?REQUEST=doQuery&LANG=VAMDC1&FORMAT=votable&QUERY=select%20*%20from%20xsams

and this shorter form does the same thing:

http://some.server/some/path/sync?REQUEST=doQuery&LANG=VAMDC1&QUERY=select%20*%20from%20xsams

because TAP-XSAMS is a special case of TAP and TAP defaults to VOTable.

The queries above should work on any TAP-XSAMS installation because of the
standard DB-schema. Here's a different kind of query that works on the extra
tables of a particular database:

http://some.server/some/path/sync?REQUEST=doQuery&LANG=ADQL&QUERY=select%20*%20from%20collisions%20where%20collider_dn%3DH2O

(i.e. "select * from collisions where collider_dn=H2O" from BASECOL). The
language here is ADQL rather than VAMDC1 because it's using an arbitrary table
instead of the standard schema.

VSS2
----------

Requestables

grouped parameters by prefix like Recatant1.StateEnergy


