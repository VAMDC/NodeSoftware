This is a minimal example of an atomic-spectroscopy database, derived from the Chianti-7 database and associated node of VAMDC. Data providers intending to make a new, atomic-spectroscopy node could start with this code and modify it to fit their data.

Data on Hydrogen, Helium and Oxygen ions are included. Only the energy-level and line data are provided. There are no bibliographic sources, and no collisional data. 

There are two data files, states.in and lines.in. These are ASCII tables provided by the Chianti project (not the publicly-available files in which Chianti data are traditionally distributed) and need to be transformed to the set of columns needed for the tignanello database. The imptools package of the node software can make this transformation, informed by the file mapping.py in this node. See the node-software manual for the invocation.

Having transformed the input tables into the files states.out and lines.out, these can be loaded into the MySQL database. The script schema.sql creates the empty tables within the current database (i.e. you should create and select the database "tignanello" first). The script ingest.sql loads the data from states.out and lines.out into the database, and then extracts the species table from the states table (it is vastly simpler to do this with the RDBMS than with the VMDC import package).

The rest of the this node follows normal, VAMDC conventions. There is a settings.py file in this directory and node files (node/models.py, node/dictionaries.py and node/queryfunc.py) matched to the database. The query-function (node/queryfunc.py) is a cut-down version of the current code for chianti.
