.. _addit:

Miscellaneous
=================

There are a few more bits and peices that are both good to know
and maybe necessary for a particular node setup.


.. _unitconv:

Unit conversions for Restrictables
---------------------------------------------


.. _specialrestr:

Treating a Restrictable as a special case
---------------------------------------------


Using a custom model method for filling a Returnable
-----------------------------------------------------

tbw

Handling the Requestables better
----------------------------------

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

Adding more views or apps to your node
------------------------------------------

tbw


The Django admin interface
---------------------------

tbw

