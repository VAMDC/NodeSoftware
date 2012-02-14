.. _limitations:

Known limitations
==================

In general, the NodeSoftware tries to be forgiving with faulty input data from
the nodes' databases and will do its best to return a valid and complete XML
document. However it relies on the content of the connected dabase and the
connection to the schema via the models and dictionaries. Errors in these
cannot be compensated by the software itself and can result in invalid output
data. All nodes are encouraged to check the validity of their XML output
against the current XSAMS, for example with the help of the TAPValidator
application.

The NodeSoftware does and will not offer the full possibilities of the XSAMS
since choices and simplifications have to be made in the implementation. These
deliberate limitations include:

* Treating isotopes and ions of atoms as different species, repeating the element information instead of nesting several ions within each isotope, and nesting the ions within each element.
* Only allowing one set of quantum numbers per atomic or molecular state. If a node wishes to return several different descriptions of the quantum numbers per state, this needs to be implemented in a custom fashion for this node. 
* Only one set of line broadening parameters per transtion and per type (instrumental, natural, pressure, doppler) is allowed at this time. The next release of the software will include the possibility to give several pressure-broadenings per transition.

A full list of outstanding issues is available at the development repository at https://github.com/VAMDC/NodeSoftware/issues where anybody is welcome to file bugs or wishlist-items.
