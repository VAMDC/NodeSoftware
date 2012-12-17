.. _quickstart:

Want to make your research data available through VAMDC but don't
know where to start? You have come to the right place.

* You have data that could complement or improve existing atomic/molecular data.
* I have data in some custom/nonstandard format and want to make it available as a VAMDC node
* I have an existing database and want to connect it to VAMDC

See below for each case.

I have complementary data
=========================

This is for you who don't want to set up and maintain your data in
a regular VAMDC node.

Maybe you have calculated better partition functions or measured
wavelengths more accurately -- things that are best used in
conjunction with other databases. Maybe your data set is too small to
warrant a full node. Or you simply don't have the time to maintain
one.

The solution is to let your data be accessible through an existing VAMDC
database - one dealing with the type of data you have. Go to

http://portal.vamdc.org/vamdc_portal/nodes.seam

Here you will find a list of all database nodes in VAMDC along with
brief descriptions and contact information. Once you find a database
you think would benefit from your data, contact the maintainer via
the email given on that page. As the internal format of each database
varies, you need to agree with the maintainer just how your data
should be supplied.



I have existing data and want it stored as a VAMDC node
======================================================================

This is for you who already maintains a body of data in some custom,
legacy or otherwise non-standard storage/access system. Such systems are
often highly optimized for the hardware they were created on, but can
be hard to maintain, update and keep secure in the long run. Especially
when the original creators have moved on.

As long as you can get your data into normal ASCII files (it can be
gzipped if very large), you should be helped by the import tool
VAMDC distributes. This tool converts from almost any ASCII format
into a form suitable to import into a modern relational database
(MySQL, PostgreSQL etc).

Here are the steps in brief. You can find detailed documentation here: <link>

#. Download the NodeSoftware from #link. This includes the import
   tools, documentation and examples.
#. Prepare your data as ASCII files.
#. Think about how you should store that data in your new database.
   The database schema is defined using the NodeSoftware so you don't have to dabble
   with the database directly.
#. Describe the format of your files in a "mapping file". This tells
   the import tool how it should read your input data and how this maps to the
   new database you are creating.
#. Running the import tools with your mapping file will convert your
   raw input data to intermediary text files on a database-friendly
   format. These can be directly (and efficiently) be imported into
   an SQL database.
#. You need to make your database available online. There are
   instructions and suggestions for this here <link>.
#. From here on, jump to the section on connecting an existing
   database to VAMDC.



Connecting an existing database to VAMDC
========================================

This is for you who have an existing database. Maybe you just created
it from flat files in the previous section. Maybe you are wanting to
improve access to an old and tried system.

Even if your database is already ready to run, it is highly recommended
that you nevertheless set up and manage it using the NodeSoftware. Not only will
this give you more examples to look at, implementing a node from
scratch is a lot of work!

Assuming you have the database up and running and has it set up to be
accessible, you now need to make sure VAMDC can talk to it correctly.

You generally need to prepare two dictionaries:

#. The "restrictables" dictionary -- this dictionary is used when someone from the VAMDC
   side wants to find something in your database. On the VAMDC-side
   generic names are used to describe the query. You must make sure to map
   this generic query to whatever query is required to find that property in your particular database.
#. The "returnables" dictionary -- vice-versa, once your database has processed the
   query, it must echo the result back in a form VAMDC understands. In
   other words you must take your data and map each bit to the label
   that VAMDC dictates for data of that type.

You can find all the keywords that VAMDC specifies here <link to dictionary>
The NodeSoftware contains many examples of how to do this translation in practice.
You can even run a local test node and test it comforms to VAMDC standards.

The final step is registering your node with VAMDC online.
support@vamdc.eu?


