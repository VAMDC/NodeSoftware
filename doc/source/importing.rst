.. _importing:

How to get your data into the database
=========================================

In the previous chapter, we have learned how to define the database layout
and tell the framework to create the database accordingly. The following
describes how to fill this database with data that reside one or many
ascii tables.

.. note::
    There are many ways to achieve this and you are certainly free to
    fill the database in any way you want, if you already know how to
    do it.

The strategy we adopt is to use the database's own import mechanisms 
which are manyfold faster for large amounts of data than manually 
inserting row by row.

So the import becomes a two-step process:

#. create one ascii file per data model where each of them has columns
   that exactly match the columns in the database.
#. run one SQL command for each of these files to load it into the
   matching database table.


Since you might already have step 1 finished or might be able to get it 
with your own data handling tools, let's have a look at step 2 first.


Loading ascii data into the database
------------------------------------------

In the following, we assume that you use MySQL as your database engine 
which is our recommendation when a new database is set up for the first 
time. Other engines have similar mechanisms for bulk loading data.

The command we use looks like this::

    mysql> LOAD DATA INFILE '/path/to/data.file' into table <TAB>;

where <TAB> is the name of the table that matches the file that is 
loaded. 

.. note:: The table names have a prefix *node_*, i.e. the table 
    for a model called *State* will be called *node_state*, unless you 
    specify the table name in the model's definition. You can see a list
    of all tables by running *SHOW TABLES;*.

The LOAD DATA command has several more options and switches for setting 
the column delimiter, skipping header lines and the like. Mathematical 
or logical operations can be run on the columns, too, before the data 
get inserted into the database.

You can read all about LOAD DATA at http://dev.mysql.com/doc/refman/5.1/en/load-data.html

A more complete example would look like::

    mysql> LOAD DATA INFILE '/path/transitions.dat' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' IGNORE 1 LINES;


Preparing the input files
----------------------------------

In the not so unlikely case that the data are not yet in a format that 
exacly matches the database layout, we provide a tool that can be used 
to re-write your data and create the ascii files that can be loaded as 
described above.

These files must fulfill the following criteria:

* One file per database table. LOAD DATA cannot update existing rows.
* Same number of columns in the file as in the table and in the right order. Although LOAD DATA can take a list of columns to circumvent this restriction, it makes sense to get this right.
* Links between the tables are in place. The key values that link tables (e.g. states and transitions) should be already in the ascii files (even though they *can* still be generated with LOAD DATA by using some SQL magic).
* A consistent delimiter between the columns (no fixed record length) and consistent quoting.
* Empty (NULL) values are written as *\\N*, not 0 or anything else. (Can also be fixed later if this is the only thing missing)


The Node Software ships with a *rewrite tool* for creating the files 
according to these criteria. The tool can be used to import almost any 
format of file as long as it stores its records as *lines* (blocks of 
data stretching several lines in the file are currently only partly 
supported).

For using the rewrite tool, you need to tell it how your original data 
files are named and how they are structured. This is done in something 
called a *mapping file*. The mapping file describes how the rewriter 
should extract data from your custom text files and write them into the files
that match the data model.

  should usually import helper functions from *imptools/linefuncs.py*
  to do much of the work for you. There is a sample mapping file in
  the *imptools/* directory, you can copy that to your Node to
  edit.


Starting the rewrite

Once you have defined the mapping file as described in the following 
section, you give it as an argument to 
the *imptools/run_rewrite.py* program::

    $ python run_rewrite.py mapping_mynode.py

  

The mapping file
----------------

The mapping file is a standard Python file. It must define a variable 
called *mapping* which contains a list of definitions that describe
how the rewriter should parse the lines of any number of text files and 
put the result into the output files.

Let's start by defining your input files::

   from imptools.linefuncs import *

   # the names of the input files
   basepath = "/path/to/your/raw_data/" 
   file1 = basepath + 'raw_file1.txt'
   file2 = basepath + 'raw_file2.txt'
   file3 = basepath + 'raw_file3.txt'
   outfile1 = basepath + 'references.dat'
   outfile2 = basepath + 'species.dat'

   mapping = [ ... ]  # described below








The ``mapping`` list
+++++++++++++++++++++


The ``mapping`` variable is a list of Python *dictionaries*. A python
dictionary is written as ``{key:value, key2:value2, ... }``. One of
these keys, *linemap*, is itself a list with further dictionaries. The
structure looks like this::





 mapping = [
    {key : value, 
     key : value,
     linemap : [
         {linemap_key : value, 
          linemap_key : value},
         {linemap_key : value, 
          linemap_key : value}] }
     {key : value, 
      key : value, 
      linemap : [ ... ]}
    ] 



The keys and values of each dictionary describes how to populate one output
file using any number of source text files.  

=============  =========================================================
**key**        **value**
-------------  ---------------------------------------------------------
*Mandatory*
outfile        The name of the file that should be created. 
infiles        Input file(s). If more than one file is used, this
               should be a list of filenames.          
linemap        A list of dictionaries defining how to parse each line 
               of the file(s) into its components.
*Optional*
headlines      Number of header lines at the top of the 
               input file() (default: 0). 
commentchar    Which comment symbol is used in the input
               file(s) (default: '#'). 
cnull          Values in the input file(s) that should be
               considered 'null' and ignored (no default).
errline        Whole lines in the input file(s) that should 
               be considered non-valid and ignored (no default). 
lineoffset     An offset step length (in number of lines) between 
               two or more read input files. Default (0) means stepping
               one line at a time. Am offset of 1 means skipping every
               other line. So a lineoffset of (0,2) would mean that
               while every line is read in the first file, only every
               third is used in the second file (default is 0 offset).
=============  =========================================================

If you are using more than one input file to populate one output file
(for example if you read one piece of data from each file and combines
them), you need to supply lists to all entries identifying features
in the files, such as *commentchar*, *cnull* etc. If you do not the
rewriter will return errors. Note that in order to correlate several
files like this they all have to have its data in the form of lines,
and be able to step systematically through those lines. Use
*lineoffset* to step at different rates through the files.

The *linemap* key points to another list with dictionaries. This is the
actual operating piece of code and describes exactly how to parse each
line (or lines, if more than one input file is used). The result of
each dictionary is the population of one database field in your
model. 

==================  =========================================================
**linemap_key**     **value**
------------------  ---------------------------------------------------------
*Mandatory*
cname               The name of the field in your database model.
cbyte               A tuple ``(linefunction, arguments)``. This defines a
                    function capable of parsing the line(s) to produce
                    the data needed to feed to the field *cname*. The only
                    provision of a linefunction is that it should take 
                    an argument *linedata* as its first argument. This
                    contains the current line to parse, or a list of lines
                    if more than one input files where read simultaneously.
*Optional*
debug               This will activate verbose error messages for this
                    parsing only. Useful for finding problems with the mapping. 
==================  =========================================================

Continuing our example, here's of how this could look in the mapping
file (the line breaks are technically not needed, but make things easier to
read)::
   
   mapping = [
     # first dictionary, writing into references.dat
     {
       'outfile': outfile1,
       'infiles': file1,
       'headlines' : 3,
       'commentchar' : '#',
       'linemap' : [             
           {'cname':'dbref',
            'cbyte':(bySepNr, 0, '||')}, 
           {'cname':'author',
            'cbyte':(bySepNr, 1, '||')},
               # ...
                   ]        
     } 
     # next model dictionary, writing species.dat
     {  
       'outfile' : outfile2,
       'infiles' : (file2, file3), # using more than one file!
       'commentchar' : (';', '#'),
       'headliens' : (1, 3),
       'lineoffset' : (0, 1),  
       'linemap' : [
          {'cname':'pk',
           'cbyte':(charrange, 23, 25)}, # pick a range by index
          {'cname':'mass',
           'cbyte'(charrange, 45, 45, 1)}, # retrieved from file3!
             # ...
          {'cname':'source',
           'cbyte':(charrange, 0, 10),
                   ]
        }]

Here we define how to populate two models. The first dictionary makes 
use of the *bySepNr* line function (see below) to extract data from each 
line. The second instead relies on a line function called *charrange* to 
mix info from two input files. 


The line functions
++++++++++++++++++

Since the mapping file is a normal Python module, you are free to code
your own line functions to extract the data from each line in your
file. There are only three requirements for how a line function may
look:

* The function must take at least one argument, which holds the current line
  being processed, as a string. The import program will automatically send this to
  the function as it steps through the file. If more than one file is 
  traversed, this input will be in the form of a *list* of line
  strings (it is then up to you which one to use). 
* The function must return its extracted piece of data in a format
  suitable for the field it is to be stored in. So a function parsing
  data for a CharField should return strings, whereas one parsing for
  an IntegerField should return integer values. 
* If the function is used to populate a Many-to-Many relationship
  (that is, the key *multireference* is set in the parsing dictionary), the
  line function must return a *list* of parsed results, one for each
  reference that is to be searched for in the database and tied to the
  field. 

Below is a simple example of a line function that fulfills all these
criteria::

 def charrange(linedata, start, end):
     """
     Simple extractor that cuts out part of a line 
     based on string index
     """ 
     return linedata[start:end].strip()



In the mapping dictionary we call this with e.g. ``'cbyte' :
(charrange, 12, 17)``. The first element of the tuple is the function
object, everything else will be fed to the function as arguments.

This function assumes that linedata is a simple string, and so it will
not work if we where to re-use it for multiple in-files (linedata will
then be a list). So let's do a simple addition::


 def charrange(linedata, start, end, filenum=0):
     """
     Simple extractor that cuts out part of line(s)
     based on string index
     """ 
     if is_iter(linedata):
         # this is an iterable (i.e. a list)
         # so pick one line based on linenum
         linedata = linedata[linenum] 
     return linedata[start:end].strip()


This you can still call the same way as before, but when working with
more than one file, you can also add an extra argument to pick which
file to use the line from. 

The import tool comes with a basic set of the most common line
functions, such as extracting by line index, by separator and some
more. Just ``import linefuncs *`` from your mapping file to make them
available. You can find more info in the :ref:`linefuncs`. 

More advanced line parsing
**************************

Sometimes you need more advanced parsing. Say for example that you
need to parse two different sections of lines from one or more files
and combine them into a unique identifier that you will then use as a
key for connecting your model to another via a One-to-Many
relationship. Or maybe you want to put a value in different fields
depending on if they are bigger/smaller than a certain value. 
The default line functions in *linefuncs.py* cannot do this out of the
box.  

The solution is to write your own line function. You have the full
power of Python at your command. Often you can use the
default functions as "building blocks", linking 
them together to get what you want. Just code your custom line
functions directly in the mapping file. 

Here is an example of a line function that wants to create a unique id
by parsing different parts of lines from different files::


 def get_id_from_line(linedata, sepnr, index1, index2):
     """
     extracts id from several lines. 
       sepnr - nth separator to pick from file 1
       index1, index2 - indices marking piece to pick from file 2
        
       (file3 is always used the same way, so we hard-code the
       indices for that file.)
     """
     l1 = bySepNr(linedata[0], sepnr, ',')
     l2 = charrange(linedata[1], index1, index2)
     l3 = charrange(linedata[2], 0, 3)
     if l3 == '000':
         l3 = 'unknown'
     # create unique id
     return "%s-%s-%s" % (l1, l2, l3)


Here we made use of the default line functions as building blocks to
build a complex parsing using three different files. We also do some
checking to replace data on the spot. The end result is a string
combined from all sources. This would be called from the line mapping
dictionary with e.g. ``cbyte: (get_id_from_line, 3, 25, 29)``.

In the *imptools* directory you can find a fully functioning mapping
used for importing the VALD database. It also contains a set of custom
line functions to use for inspiration. 
