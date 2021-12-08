How to set up a VAMDC node to test the asynchronous/SQLite prototype
--------------------------------------------------------------------

Constraints:
	⁃	Assumes Python node-software.
	⁃	Assumes compatibility with  recent versions of the node-software.
	⁃	Requires Python 3 and recent versions of Django.
	-   Collisional data and physical environments not supported yet.
	
	
Process:
	1.	Check out the async branch of VAMDC/NodeSoftware from GitHub to get the changes to vamdctap. They are not in the master branch.
	2.	Ensure that your node works in this environment for traditional — synchronous/XSAMS — query before trying the new stuff.
	3.	Install some SQLite tools for looking at the results. Command-line tools from https://www.sqlite.org/download.html. GUI from https://sqlitebrowser.org.
	4.	Update settings.py to set the cache directory (see below for details).
	5.	Update dictionaries.py to set the columns for the tables (see below for details).
	6.	Run the node for local test: python manage.py runserver.
	7.	Using Firefox, go to http://localhost:8000/tap/async/form to enter your query. The rest of the async operation can be driven from the browser. If you have the DB-browser GUI configured to open .sqlite files, Firefox will open results in that tool when you click a results link. This is very nice for a quick look at results.
	8.	Please don’t put this version into production!


Setting the cache directory:
In settings.py, set the variable RESULTS_CACHE_DIR to the absolute path of a directory to hold the results of queries. E.g.

	RESULTS_CACHE_DIR='/Users/guy/VAMDC/async/cache'

Create the directory. This should be allowed to hold up to a few 100 MB of results for test, and rather more for production. The node software creates in here files named with UUIDs and the file-name extension .sqlite: each one is the result of one query. The node software deletes queriy results after 24 hours to reclaim space.

F
illing the dictionaries:
Add a dictionary to your dictionaries module for each table you want to fill in the SQLite results. This is the tricky part.

You don’t need to change any of the existing dictionaries used for the synchronous query.

The supported dictionaries so far are:
	ATOMS_COLUMNS, 
	ATOMSTATES_COLUMNS,
	MOLECULES_COLUMNS,
	MOLECULESTATES_COLUMNS,
	PARTICLES_COLUMNS,
	RADTRANS_COLUMNS,
	SOURCES_COLUMNS. 
	
Support for collisional data is to follow later.

In each dictionary, the keys are the names of the columns created in the table. You can pick any names, but it seems helpful to use names from the VAMDC dictionary where they match your data. The values are 2-tuples. The first element in each tuple is the type of the column in SQLite. The second is a python fragment specifying how to get the data out of the Django model that your query function generates; that’s the same query function used in the synchronous query to fill XSAMS, the one that returns a dictionary of Django QuerySets like Atoms, Atomstates, RadTrans, etc.

This is an example of a directory from the Chianti-7 copy I’ve been using to test.

ATOMS_COLUMNS = {
    'AtomId': ('INTEGER', 'id'),
    'AtomSymbol': ('CHAR(2)', 'atomsymbol'),
    'AtomNuclearCharge': ('INTEGER', 'atomnuclearcharge'),
    'AtomIonCharge': ('INTEGER', 'atomioncharge'),
    'InChI': ('TEXT', 'inchi'),
    'InChIkey': ('TEXT', 'inchikey'),
}

Note that SQLite is very flexible about types. You can use either highly-specific types like CHAR(2), or general types like TEXT. You could even declare all the columns as TEXT and it would (probably) work, stringifying all the data as they are inserted. But please don’t do this: I suggest distinguishing, text, integer and floating point (FLOAT type) columns.

The second element in the tuple for a column is subtle. The vamdctap module, the common part of the node software, is iterating through the QuerySet provided by your query-function, obtaining in each iteration a Django Model object representing a row of output; the Model objects are instance of the classes in the models.py of your node, so their detail are node-specific. The Python fragment that you specify is treated as an attribute of that object. E.g., if you specify atomsymbol in ATOM_COLUMNS, vamdctap will evaluate row.atomsymbol where row is an instance of your atoms class in models.py. The fragment can refer directly to a data member of the model class, or to a method of that class. See the chianti node in the node software for examples of each approach.

Note that both elements of the tuple are strings and need to be quoted as such.