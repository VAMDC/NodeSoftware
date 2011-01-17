.. _importing:

How to use the import tool
==========================

The VAMDC package ships with an *import tool* for importing 
custom text files into a standard database. The tool can be used to
import almost any format of file as long as it stores its records as
*lines* (blocks of data stretching several lines in the file are 
currently not supported). 

Using the tool consists of defining two main components: 

* A set of *Django database models*. A "model" in this context is a snippet of Python code
  that describes the layout of a database table and its fields. The Django framework abstracts the
  process allowing for wide support for different databases with the
  same interface. The various database models you use are always
  defined in *YourNode/node/models.py*. How to define your database
  models are described in :ref:`newnode`.
* A *mapping file*. The mapping file describes how the importer should
  extract data from your custom text files and store that into the right database model. You
  should usually import helper functions from *imptools/linefuncs.py*
  to do much of the work for you. There is a sample mapping file in
  the *imptools/* directory, you can copy that to your Node to
  edit. 

Starting the import
-------------------

Once you have prepared your database models and defined the mapping
file as described in the following 
section, you give the full path to your mapping file as an argument
to the *imptools/run_import.py* program::
<<<<<<< HEAD


    $ python run_import.py /vamdc/YourNode/mapping_mydata.py
=======
 shell> python run_import.py /vamdc/YourNode/mapping_mydata.py
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
  

The mapping file
----------------

The mapping file describes how the importer should parse the lines of
any number of text files and put the result in the correct database
tables and fields. You must at this point have set up your database
models. 

.. note:: 
   During this tutorial we use a node *MyNode* located in the top
   vamdc directory. The mapping file will be called called
   *MyNode/mapping_mynode.py*.

The mapping file is a standard Python file. It must contain a variable
*mapping* pointing to a list. You also need to ``import`` the the
relevant database models from your node. Finally, you will probably
want to use some of the helper functions found in *imptools/linefuncs.py*
.. ::
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
   # Mapping file for MyNode importing
  
   # import models and help functions. 
   from MyNode.node import models
   from linefuncs import * 

   # the names of the input files
   basepath = "/vamdc/MyNode/raw_data/" 
   file1 = basepath + raw_file1.txt
   file2 = basepath + raw_file2.txt
   file3 = basepath + raw_file3.txt

   mapping = [ ... ]  # described below
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
(run_import sets up the paths so you can import directly from the
imptools directory)

The ``mapping`` list
+++++++++++++++++++++

The ``mapping`` variable is a list of Python *dictionaries*. A python
dictionary is written as ``{key:value, key2:value2, ... }``. One of
these keys, *linemap*, is itself a list with further dictionaries. The
structure looks like this::
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
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
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
The keys and values of each dictionary describes how to populate one database 
model using any number of source text files.  

=============  =========================================================
**key**        **value**
-------------  ---------------------------------------------------------
*Mandatory*
model          Database model to populate. 
fname          Input file(s). If more than one file is used, this
               should be a list of filenames.          
linemap        A list of dictionaries defining how to parse each line 
               of the file(s) into its components; the result of each 
               dictionary will be inserted into a database field.
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
updatematch    A field name to use to obtain keys
               for referencing other tables in the database
               (e.g. One-To-Many and Many-To-Many relationships)
=============  =========================================================

If you are using more than one input file to populate a given model
(for example if you read one piece of data from each file and combines
them),  you need to supply lists to all entries identifying features
in the files, such as *commentchar*, *cnull* etc. If you do not the
importer will return errors. Note that in order to correlate several
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
cname               The database field. This must match an actual field
                    name on your database model.
cbyte               A tuple ``(linefunction, arguments)``. This defines a
                    function capable of parsing the line(s) to produce
                    the data needed to feed to the field *cname*. The only
                    provision of a linefunction is that it should take 
                    an argument *linedata* as its first argument. This
                    contains the current line to parse, or a list of lines
                    if more than one input files where read simultaneously.
*Optional*
references          A tuple ``(linked_model, identifying_field)``. This is only to be
                    used if the field *cname* is defined on the model as a One-To-Many
                    relationship (a ForeignKey). The data parsed with
                    *cbyte* above will then not be inserted in this field -
                    instead the result is used as a search criterion: The database will be
                    searched for instances of *linked_model* with an
                    *identifying_field* value equal to the parsed result.
multireferences     A tuple ``(linked_model, identifying field).``
                    This is similar to *references* above, but is used
                    on a Many-to-many relation (ManyToManyField). This
                    will use the result from the line function in
                    *cbyte* to search and connect any number of
                    matching model instances to this field. Note: For this
                    to work, the linefunction you use *must* return a
                    list of keys to match for, one for each model
                    intance you want to relate to this field. 
debug               This will activate verbose error messages for this
                    parsing only. Useful for finding problems with the mapping. 
==================  =========================================================

Continuing our example, here's of how this could look in the mapping
file (the line breaks are technically not needed, but make things easier to
read).

::
   
   mapping = [
     # first dictionary, populating model 'References'
     {
       'model': models.References,
       'fname': file1,
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
     # next model dictionary, populating a model 'Species'
     {  
       'model' : models.Species,
       'fname' : (file2, file3), # using more than one file!
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
           'references': (models.References, 'dbref')} 
                   ]
        }]
<<<<<<< HEAD


=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
Here we define how to populate two models. The first dictionary (for
the *References* model) makes use of the *bySepNr* line function (see
below) to extract data from each line. The *Species* mapping
instead relies on a line function called *charrange* to mix info
from two input files. It also  references back to the *References*
model using an id that can presumably be found in the input file. 

The line functions
++++++++++++++++++

Since the mapping file is a normal Python module, you are free to code
your own line functions to extract the data from each line in your
file. There are only three requirements for how a line function may
look:
<<<<<<< HEAD


=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
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
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
 def charrange(linedata, start, end):
     """
     Simple extractor that cuts out part of a line 
     based on string index
     """ 
     return linedata[start:end].strip()
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
In the mapping dictionary we call this with e.g. ``'cbyte' :
(charrange, 12, 17)``. The first element of the tuple is the function
object, everything else will be fed to the function as arguments.

This function assumes that linedata is a simple string, and so it will
not work if we where to re-use it for multiple in-files (linedata will
then be a list). So let's do a simple addition::
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
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
<<<<<<< HEAD



=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
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
<<<<<<< HEAD


=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
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
<<<<<<< HEAD


=======
>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
Here we made use of the default line functions as building blocks to
build a complex parsing using three different files. We also do some
checking to replace data on the spot. The end result is a string
combined from all sources. This would be called from the line mapping
dictionary with e.g. ``cbyte: (get_id_from_line, 3, 25, 29)``.

In the *imptools* directory you can find a fully functioning mapping
used for importing the VALD database. It also contains a set of custom
line functions to use for inspiration. 
<<<<<<< HEAD
=======






>>>>>>> 9a228c5d0c8682e097ae14c3fb159d4af735a09a
