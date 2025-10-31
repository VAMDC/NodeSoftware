.. _quickstart:

`VAMDC <http://www.vamdc.org/>`_ is a European collaborative effort to centralize access to
atomic and molecular research data. Data producers maintain their
scientific resources as "nodes" in the VAMDC network. Data consumers can then conveniently
query the network from an online portal, receiving collated information from the nodes having what
they need. Not only does this allow consumers a unified way to access data, since references are
stored with the data, it also creates a clear way for scientists to credit the original data producer.

This quickstart guide is aimed at you who are a data producer and are interested
in making your research available through VAMDC. This page is relevant to you if any
of the following statments apply:

* I have data that could complement or improve existing atomic/molecular data.
* I have data in some custom format and want to make it available as a VAMDC node.

The `full documentation <http://www.vamdc.org/documents/nodesoftware/index.html>`_
gives more details. Also don't be shy to send an email to support@vamdc.eu if you run into trouble.


I have complementary data
=========================

This is for you who don't want to set up and maintain your data in
a regular VAMDC node. Maybe you have calculated better partition functions or measured
wavelengths more accurately -- things that are best used in
conjunction with other databases. Maybe your data set is too small to
warrant a full node. Or you simply don't have the time to maintain
one.

The solution is to let your data be accessible through an existing VAMDC
database - one dealing with the type of data you have.

Go to the `VAMDC portal <http://portal.vamdc.org/vamdc_portal/nodes.seam>`_. Here you will
find a list of all database nodes in VAMDC along with
brief descriptions and contact information. Once you find a database
you think would benefit from your data, contact the maintainer via
the email given on that page. As the internal format of each database
varies, you need to agree with the maintainer just how your data
should be supplied.


I want to publish existing data as a VAMDC node
===============================================

This is for you who already maintain a body of data. Maybe it's in a
database. Maybe it's stored using some legacy or otherwise
non-standard storage/access system. Such systems are often highly
optimized for the hardware they were created on, but can be hard to
maintain, update and keep secure in the long run. Especially
when the original creators have moved on.

VAMDC's open-source *NodeSoftware* package is downloadable via GIT using
`these <http://www.vamdc.org/documents/nodesoftware/prereq.html>`_
instructions. There are also tarballs to be found `here <http://www.vamdc.eu/software>`_.
The default NodeSoftware is `Python <http://www.python.org/>`_ based and uses the `Django <https://www.djangoproject.com/>`_
framework and a few more dependencies outlined on the
`prerequisites <http://www.vamdc.org/documents/nodesoftware/prereq.html>`_ page. All documentation
referes to the Python version of the software.

The NodeSoftware contains all tools for setting up and running a
VAMDC node. It also offers import tools for converting existing data.
It supports several modern relational databases (*MySQL*,
*PostgreSQL* etc).

Once you have everything installed, here is how you
get it set up, in brief:

#. In the NodeSoftware directory, go to  ``nodes/``. Copy and rename
   the ExampleNode directory. This will hold your new node.
#. In your new node directory, edit ``settings.py``. This sets up your
   database and other properties. See other nodes for more examples.
#. You now need to specify the database schema to match how you store
   your data. You need to describe the tables as "models" using Django's
   easy syntax.

  * If you already store data in a relational database, you can let Django create the
    database models automatically as described on the
    `Django homepage <https://docs.djangoproject.com/en/5.2/howto/legacy-databases/#auto-generate-the-models>`_.
  * If your data is stored in some other form you need to define your database
    scheme yourself. See examples in the ExampleNode.

The NodeSoftware can help you import legacy data from text files on
almost any format. The included import tool (in the ``imptools/``
directory) converts from such raw data into a format possible to directly import into a
modern database. The process is summarized below (in more detail in
the `imptool documentation <http://www.vamdc.org/documents/nodesoftware/prereq.html>`_).

#. Prepare your raw data as text files (they can be gzipped if very
   large).
#. Describe the format of your text in a *mapping file*. This tells
   the import tool how it should read your input data and how this maps to the
   new database structure you are creating. You can find an example
   mapping file in the ExampleNode.
#. Run the import tool on your mapping file. This will convert your
   raw input data to intermediary text files exactly representing
   how the data will be represented in your database.
#. Import the converted files into your database using the SQL command
   suitable for your database (such as ``LOAD DATA INFILE`` for MySQL).

To test your new Node you can start it with Django's in-built
testserver (``manage.py runserver``). This will start your node locally
on port `8000` by default. You can then download the JAVA-based validation
tool from http://www.vamdc.org/software and try sending some queries.

Test that ``<URL>/availability`` and ``<URL>/capabilities``
work as they should. Remember to set up some sample queries in your
settings file (see examples in the file) - once you register with VAMDC these will be used to
test your node's status.

The Django test server should *never* be used for anything but
debugging. See the `documentation <http://www.vamdc.org/documents/nodesoftware/deploy.html>`_
for instructions on setting up a full-fledged webserver and proxy to serve your data.


I want to connect my existing node to VAMDC
============================================

This is for you who have an existing database and NodeSoftware set up
already. You now need to make sure VAMDC can talk to it correctly.

VAMDC exchanges data with nodes on a unified format. In one direction are sent queries
using well-defined keywords, in the other are results in a standardized XML format.
These VAMDC-keys may not match your actual database structure or naming
scheme at all. You thus need to prepare a "dictionary" that
properly maps incoming requests to queries to your database. Vice-versa,
you need a dictionary to convert your data back to the VAMDC's unified
format.

The VAMDC dictionaries are necessarily rather complex in order to
cover all possible data forms. They are more extensively explained on the
the `concepts <http://www.vamdc.org/documents/nodesoftware/concepts.html#conceptdict>`_, page
and in the `new node <http://www.vamdc.org/documents/nodesoftware/newnode.html#the-dictionaries>`_.
documentation. Thmere is also a `list of all VAMDC keywords <http://dictionary.vamdc.org/returnables/>`_.
The NodeSoftware contains many examples of creating your dictionaries.

The final step consists of registering your node with
the central VAMDC registry.

#. Go to the VAMDC registry at https://registry.vamdc.org/
#. Follow the registration process for creating a new node entry.
#. Provide human-readable information about your node, including:

  * *Title* to identify your node
  * *Contact details* for the node maintainer
  * *Description* of what type of data users should expect to find

#. Enter the ``/capabilities`` URL of your node. Remember that you must have
   set up some sample queries in your settings file.
#. Complete the registration process.

Once registered, data consumers will be able to access your node from the
`VAMDC portal <http://portal.vamdc.org/vamdc_portal/>`_.

Welcome the VAMDC community!

