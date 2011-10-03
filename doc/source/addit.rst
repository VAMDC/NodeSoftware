.. _addit:

Miscellaneous
=================

There are a few more bits and pieces that are both good to know
and maybe necessary for a particular node setup.


.. _unitconv:

Unit conversions for Restrictables
---------------------------------------------

It is possible in ``dictionaries.py`` to apply a function to the values that
come in the WHERE-clause of a query together with the Restrictables::

    from vamdctap.unitconv import *
    RESTRICTABLES = {\
    'RadTransWavelength':'wave',
    'RadTransWavenumber':('wave',invcm2Angstr),

Here we give a two-tuple as the right-hand-side of the Restrictable *RadTransWavenumber* where the first element is the name of the model field (as usual) and the second is the function that is to be applied.

.. note::
    The second part of the tuple needs to be the function itself, not its name as a string. This allows you to write custom functions in the same file, just above where you use them.

.. note::
    The common functions for unit conversion reside in ``vamdctap/unitconv.py``. This set is far from complete and you are welcome to ask for additions that you need.

.. _specialrestr:

Treating a Restrictable as a special case
---------------------------------------------

Perhaps a unit conversion (see above) is not enough to handle a Restrictable, e. g. because you do not have the quantity available in your database but know it anyway. Suppose a database has information on one atom only, say iron. For the output one would simply hardcode the information on iron in the Returnables as constant strings. For the query on the other hand, you would like to support AtomSymbol but have no field in your database to check against - after all it would be useles to have a database column that is the same everywhere.

The solution here is to manipulate the set of restrictions by hand instead of letting *sql2Q()* handle it automatically. *sql2Q()* is a shorthand function that does these steps after each other:

1. Use *splitWhere(sql.where)* to split the WHERE statement in two:

* a structure that represents the logical structure of the query.
* a dictionary with numbers as keys and a list as values that each contain the Restrictable, the operator and the arument(s).
* For example, the query *SELECT ALL WHERE RadTranswavelenth > 3000 and RadTranswavelenth < 3100 and (AtomSymbol = 'Fe' OR AtomSymbol = 'Mg')* would return the two variables like 

 * *['r0', 'and', 'r1', 'and', '(', 'r2', 'or', 'r3', ')']*
 * *{'1': [u'RadTranswavelength', '<', u'3100'], '0': [u'RadTranswavelength', '>', u'3000'], '3': [u'AtomSymbol', '=', u"'Mg'"], '2': [u'AtomSymbol', '=', u"'Fe'"]}*

2. Go through the Restrictables and apply the unit conversion functions that were specified with the mechanism above.

3. Make use of the information in ``dictionaries.py`` to rewrite the restrictions into the native format.

4. Merge the individual restrictions together with their logic connection again and evaluate the whole shebang.

So, in summary, the call *q=sql2Q(sql)* at the start of the query function can be replaced by::

    logic,rs,count = splitWhere(sql.where)
    rs = applyRestrictFus(rs)
    qdict = restriction2Q(rs)
    q = mergeQwithLogic(qdict,logic)

Now, depending on what you want to do, you can manipulate the variables at any intermediate step. To continue the example, we insert the following right after the call to *splitWhere()*::

    ids = [r for r in rs if rs[r][0]=='AtomSymbol'] # find the numbers where the Restrictable is AtomSymbol
    for id in ids:
        #to be continued.        
        
    
.. note::
    We are aware that this is not very comfortable yet and are thinking of a better solution. Suggestions are welcome. :)

.. _specialreturnable:

Using a custom model method for filling a Returnable
-----------------------------------------------------

Sometimes it is necessary to do something with your data before returning them
and then it is not possible to directly use the field name in the
right-hand-side of the Returnable. Now remember that the string there simply
gets evaluated and that your models can not only have fields but also custom
methods. Therefore the easiest solution is to write a small method in your
class that returns what you want, and then call this function though the
returnable.

For example, assume you for some reason have two energies for your states and want them both returned into the Returnable *AtomStateEnergy* which can handle vectors as input. Then, in your ``models.py``, you do::

    class State(Model):
        energy1 = FloatField()
        energy2 = FloatField()

        def bothenergies(self):
            return [self.energy1, self.energy2]

And correspondingly in your RETURNABLES in ``dictionaries.py``::

    RETURNABLES = {\
        ...
        'AtomStateEnergy':'AtomState.bothenergies()',
        }

.. note::
    Use this sparingly since it adds some overhead. For doing simple calculations like unit conversions it is usually better to do them once and for all in the database, instead of doing them for every query.

.. _manualrequestables:

Handling the Requestables better
----------------------------------

The XML generator is aware of the Requestables and it only returns the parts of the schema that are wanted. Therefore the nodes need in principle not care about this. However, there are two issues that can interfere:

* If a node imposes volume limitations, this can lead to false results. For
  example, when a client asks for "SELECT SPECIES" without any restriction and a
  node's query function usually finds out the species for a set of transitions,
  which gets truncated, then only the species for the first few transitions in
  the database are returned.
* Again taking "SELECT SPECIES" as example, this can lead to performance issues
  if a node's query stategy is to impose the restrictions onto the most numerous
  model fist, since this query then corresponds to selecting everything and
  afterwards throwing everything away except the species information.

The solution is to make the queryfunction aware of the Returnables. The are attached to the object **sql** that comes as input. For example, one can test if the setup of atomic states is needed like this::

    needAtomStates = not sql.requestables or 'atomstates' in sql.requestables

and then use the boolean variable **needAtomStates** to skip parts of the
QuerySet building.  This test checks first, if we have requestables at
all (otherwise "ALL" is default) and then whether 'atomstates' is one
of them.

.. note::
    The query parser tries to be smart and adds the Requestables that are implied by another
    one. For example it adds 'atomstates' and 'moleculestates' when the client asks for
    'states'. Therefore it is enough to test for the most explicit one in the query functions.

.. note::
    The keywords in **sql.requestables** are all lower-case!

.. _relatedname:

Setting the related name of a field
-----------------------------------

When you have a *ForeignKey* called *key1* in a *ModelB* which points *ModelA*, 
the fields from *ModelA* become accessible by *b.key1.fieldFromModelA* in 
a selection *b* of *ModelB*. This is using the ForeignKey in **forward 
direction**.

Django also automatically adds a field to *ModelA* that contains all the 
instances of *ModelB* that point to a specific instance *a* of *ModelA*. 
This field is by default called as the referenced model plus *_set*. So 
*a.modelb_set* would hold all the ModelBs that reference *a*. This is 
using the ForeignKey in **inverse direction**.

You can change the name of the inverse field by giving the argument 
*related_name='bla'* to the definition of the ForeignKey in the model. 
When you have more than one ForeignKey from one model to the same other 
model, you **must** set the related_name because the automatic naming 
cannot give the same name twice.

A typical example for this are the upper and lower states for a 
transition where it makes sense to have two ForeignKeys in the 
Transition model, e.g. called *upstate* and *lostate*, each pointing to 
an entry in the State model. Now one sets the related_names of these 
ForeignKeys to something like *'transitions_with_this_upstate'* and 
*'transitions_with_this_lostate'* respectively. Thereby, for any state 
*s* the transitions that have *s* as upper state can be retrieved by 
*s.transitions_with_this_upstate*.

Inserting custom XML into the generator
------------------------------------------

There can arise situations where it might be easier for a node to create a
piece of XML itself than filling the Returnable and letting the generator
handle this. This is allowed and the generator checks every time it loops over
an object, if the loop variable, e.g. `AtomState`  has an attribute called
`XML`. If so, it returns `AtomState.XML()` instead of trying to extract the
values from the Retunable for the current block of XSAMS. Note the *execution*
of `.XML()` which means that this needs to be coded as a function/method in
your model, not as an attribute.



.. _returnresult:

How to skip the XSAMS generator and return a custom format
----------------------------------------------------------

Currently, only queries with *FORMAT=XSAMS* are officially supported. Since
some nodes wanted to be able to return other formats (that are only useful for
their community, for example to inculde binary data like an image of a
molecule) there is a mechanism to to do this. 

Whenever *FORMAT* is something else than *XSAMS*, the NodeSoftware checks whether there is a function called *returnResults()* in a node's ``queryfunc.py``. If so, it completely hands the responsibility to assemble the output to this function.

.. note::
    This means that you have to return a HttpResponse object from it and
    know a little more about Django views. In addition you are on your own
    to assembe your custom data format.

.. _moredjango:

Making more use of Django
------------------------------------------

Django offers a plethora of features that we do not use for the purpose of
a bare VAMDC node but that might be useful for adding custom funcitonality.
For example you could:

* Use the included **admin-interface** to browse and manipulate the content of your database.
* Add a custom query form that is suited specifically for the most common use case of your data.
* Add a web-browsable view of your data.

For more information on all this have a look into Django's excellect documentation at https://docs.djangoproject.com/

For extending your node beyond the VAMDC-TAP interface, you would normally add a second *app* to your node directory, besides the existing one called *node*. Then you simply tell your ``urls.py`` to serve the new app at a certain URL.
