.. _importing:

How to get your data into the database
=========================================

In the previous chapter, we have learned how to define the database layout
and tell the framework to create the database accordingly. The following
describes how to fill this database with data that previously resided
in one or many ascii tables.

.. note::
    There are many ways to achieve this and you are certainly free to
    fill the database in any way you want, if you already know how to
    do it.

The strategy we adopt is to use the database's own import mechanisms 
which are many times faster for large amounts of data than manually 
inserting data row by row.

The import thus becomes a two-step process:

#. create one ascii file per data model, each of which has columns
   that exactly will match the columns in the database.
#. run one SQL command for each of these files to load it into the
   matching database table.


Since you might already have step 1 finished or might be able to get it 
with your own data handling tools, let's have a look at step 2 first.


Loading ascii data into the database
------------------------------------------

In the following, we assume that you use MySQL as your database engine 
(this is also our recommendation when a new database is set up for the first 
time). Other engines have similar mechanisms for bulk loading data.

The mysql command we use looks like this::

    mysql> LOAD DATA INFILE '/path/to/data.file' into table <TAB>;

where <TAB> is the name of the database table corresponding to the
file being loaded. 

.. note:: The table names have a prefix *node_*, i.e. the table 
    for a model called *State* will be called *node_state*, unless you 
    specify the table name in the model's definition. You can see a list
    of all tables by giving mysql the command *SHOW TABLES;*.

The LOAD DATA command has several more options and switches for setting 
the column delimiter, skipping header lines and the like. Mathematical 
or logical operations can be run on the columns too, before the data 
get inserted into the database.

You can read all about LOAD DATA at http://dev.mysql.com/doc/refman/5.1/en/load-data.html

A more complete example would look like::

    mysql> LOAD DATA INFILE '/path/transitions.dat' IGNORE INTO TABLE transitions COLUMNS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' IGNORE 1 LINES;


Preparing the input files
----------------------------------

In the not so unlikely case that the data are not yet in a format
exacly matching the database layout, the Node Software ships with a
*rewrite tool* to convert your data into such a format. The output will be ascii
files that can be loaded as described in the previous section and will
 fulfill the following criteria:

* One file per database table. LOAD DATA cannot update existing rows.
* Same number of columns in the file as in the table and in the right order. Although LOAD DATA can take a list of columns to circumvent this restriction, it makes sense to get this right.
* Links between the tables are in place. The key values that link tables (e.g. states and transitions) should be already in the ascii files (even though they *can* still be generated with LOAD DATA by using some SQL magic).
* A consistent delimiter between the columns (no fixed record length) and consistent quoting.
* Empty (NULL) values are written as *\\N*, not 0 or anything else. (Can also be fixed later if this is the only thing missing)


The tool can be used to convert almost any 
format of file. It's easiest to convert files with its records stored
as *lines* (one line per record), but the tool also supports
blocks of data stretching several lines. 

To use the rewrite tool, you need to tell it how your original data 
files are named and how they are structured. This is done in something 
called a *mapping file*. The mapping file describes how the rewriter 
should extract data from your custom text files. It will then use your
data models (which you should have defined by now) to create output
files in a format the database can import. 


Starting the rewrite

Once you have defined the mapping file as described in the following 
section, you need to place yourself in the *imptools/* directory (this
is so the rewriter can find all its dependencies) and then give the
mapping file as an argument to the *imptools/run_rewrite.py* program::

    $ python run_rewrite.py ../nodes/MyNode/mapping_mynode.py


Depending on the amount of data, the conversion might take some
time. The result will be a set of ascii output files.


The mapping file
----------------

The mapping file is a standard Python file and describes how the
rewriter reads the raw data. *imptools/mapping_sample.py* is a minimal
mapping file one can build from. A much more complete example is found
in the *nodes/ExampleNode* directory.

The mapping file must define a variable 
called *mapping* which contains a list of definitions that describe
how the rewriter should parse each text file and correlate the data to
the data models.

Let's start a sample mapping file. It starts by defining some
convenient variables storing input/output filenames (just to make it
easier to refer to them further down). We also include
*imptools/linefuncs.py* which holds helper methods for parsing data. 
The only mandatory part is the *mapping* list::

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


The ``mapping`` variable is a list of Python *dictionaries*. A
standard python dictionary is written as ``{key:value, key2:value2,
... }`` and is a very efficient means of storing data. One of
these keys, *linemap*, tself points to a list with further dictionaries. The
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


The *key* s and *value* s of
each dictionary describes how to populate one output 
file using any number of source text files. Remember that each such
output file is to be read into the database later and will populate
one database table -- that is one "model" in your schema. 

=============  =========================================================
**key**        **value**
-------------  ---------------------------------------------------------
*Mandatory*
outfile        The name of the file that should be created. Note that
               each such output file will be read into one database
               model. 
infiles        Input file(s). This may also accept a list of multiple
               file names. More than one file may
               be relevant if the raw data is stored in multiple files
               related to each other by line number. 
linemap        A list of dictionaries defining how to parse each line/block 
               of the file(s) into its components (see the next table
               below for defining the linemap list)
.
*Optional*
headlines      Number of header lines at the top of the 
               input file() (default: 0). If more than one infile is
               used, this must be a list of headlines, as many as
               there are files.
commentchar    Which comment symbol is used in the input
               file(s) to indicate a line to ignore (default is: '#').
               As above, this must be a list
               if more than one filename is read. 
cnull          Values in the input file(s) that should be
               considered 'null' and ignored (no default). As above,
               this must be a list if more than one filename is read. 
errline        Whole lines in the input file(s) that should 
               be considered non-valid and ignored (no default). As
               above, this must be a list if more than one filename is
               read. 
linestep       A step length (in number of lines) when reading the
               input file. Default (0) means stepping
               one line at a time. A linestep of 1 means skipping every
               other line. If more than one file is read at a time,
               this must be a list of the same length as there are
               files. So a lineoffset of [0,2] would mean that
               while every line is read in the first file, only every
               third is used in the second file.
lineoffset     A starting offset when reading a file, after headers have
               been skipped. So a lineoffset of 3 would first skip the
               header (if any), then another 3 lines. This is most
               useful in combination with linestep, to make sure the
               first line of data is read from the right start 
               point. If many files are read, this must be given as a
               list of offsets, as many as there are files. 
startblock     This is a string or a list of strings to be interpreted
               as starting sentinels for data records stretching over 
               more than one line. So if every data block is wrapped
               in BEGIN ... END clauses, you should put "BEGIN" here. 
               (default is the line break character). The variables
               *linestep*  and *lineoffset* will step through full
               blocks if so given. 
endblock       This is a string or list of strings to be interpreted
               as ending sentinels for data records stretching over
               more than one line. So if every data block is wrapped
               in BEGIN ... END clauses, you should put "END"
               here. (default is the line break character). If blocks
               are only separated by a single sentinel 
               (e.g. ... RECORD ... RECORD ... ), simply put the same
               sentinel ("RECORD" in this example)  as both startblock
               and endblock.  

=============  =========================================================

A note about reading multiple files at the same time: The only main use for
this is really if your raw data is related to data in other files by
*record number only* (i.e. by counting line number or maybe block number). If you
cannot use line numbers since you use, say, an ID string to relate data
in one file to that in another, you should read the files as separate
reads. Exactly how the read will looks depend on your planned database
layout and the models you need to
populate. */nodes/vald/mapping_vald3.py* contains an advanced example
of reading upper and lower atomic States from a file in two passes, using ID
hashes to relate them to a second model (Transitions).   


The *linemap* key points to another list with dictionaries. This is the
actual operating piece of code and describes exactly how to parse each
line or block (or lines/blocks, if more than one input file is read
simultaneously). Each dictionary works for a single database field in
your current model and describes exactly how to parse the
current line/block so as to produce a value in that field.

==================  =========================================================
**linemap_key**     **value**
------------------  ---------------------------------------------------------
*Mandatory*
cname               The name of the field in your database model.
cbyte               A tuple ``(linefunction, arguments)``. This names a
                    function capable of parsing the line(s) to produce
                    the data needed to feed to the field *cname*. The only
                    provision of a linefunction is that it should take 
                    an argument *linedata* as its first argument. This
                    will contain the current line/block to parse, or a list of lines/blocks
                    if more than one input file were read
                    simultaneously. You can define your own
                    linefunctions directly in the mapping file. A host 
                    of commonly needed line functions (such as reading
                    a particular index range or the Nth separated
                    section etc) come with the package and can be used
                    directly by importing from *imptools/linefuncs.py*.
.
*Optional*
filenum             This is an integer or a list of integers used only when more than one
                    file is read simultaneously. It allows you to specify
                    the index/indices of the file/files to be
                    parsed. Default is file 0. Note: If you need to somehow
                    merge data from two or more files to produce one
                    value, you need to write a custom line function
                    for this and then use this setting to specify which
                    files should be used. 
cnull               Indicates what should be interpreted as NULL data.
                    If this string is found, the `\N` symbol will be stored in
                    the output file instead.
debug               This will activate verbose error messages for this
                    parsing only. Useful for finding problems with the mapping. 
==================  =========================================================

Continuing our example, here's how this could look in the mapping
file (the line breaks are technically not needed, but make things easier to
read). Note also that we imported linefuncs.py earlier, making the
line functions *bySepNr* and *charrange* available (among many others)::
   
   mapping = [
     # first dictionary, writing into outfile1 (defined above) from an
     # input file file1.  
     {
       'outfile': outfile1,
       'infiles': file1,
       'headlines' : 3,
       'commentchar' : '#',
       'linemap' : [             
           {'cname':'dbref',
            'cbyte':(bySepNr, 0, '||')}, # get 0th part of record separated by ||
           {'cname':'author',
            'cbyte':(bySepNr, 1, '||')}, # get 1st part of record separated by ||
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


The line functions
++++++++++++++++++

Since the mapping file is a normal Python module, you are free to code
your own line functions to extract the data from each line/block in your
file. There are only three requirements for how a line function may
look:

* The function must take at least one argument, which will hold the
  current line or block being processed, as a string. The import
  program will automatically send this to  the function as it steps
  through the file. If you read multiple input files *and* supplied
  multiple *linenum* values in the mapping, this first argument will
  also be a list with the corresponding lines/blocks. It's up to the
  custom function to handle this list properly.
* The function must return its extracted piece of data in a format
  suitable for the field it is to be stored in. So a function parsing
  data for a CharField should return strings, whereas one parsing for
  an IntegerField should return integer values. 

Below is a simple example of a line function::

 def charrange(linedata, start, end):
     """
     Simple extractor that cuts out part of a line 
     based on string index.
     """               
     return linedata[start:end].strip()


In the mapping dictionary we will call this with e.g. ``'cbyte' :
(charrange, 12, 17)``. The first element of the tuple is the function
object, everything else will be fed to the function as arguments.

The default line functions coming with the package will handle most
common use cases. Just ``import linefuncs *`` from your mapping file
to make them available. You can find more info in the :ref:`linefuncs`. 


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


 from imptools.linefuncs import *

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
combined from all sources. 

This function assumes linedata is a list. It must thus be called from
a mapping where at least three files are read and where *filenum* is
given as a list specifying which files' lines/blocks are to be sent to
the function. From the mapping dictionary we would then call this with
e.g. ``cbyte: (get_id_from_line, 3, 25, 29)``. 


See *nodes/ExampleNode* for more examples of mappings and linefuncs..
