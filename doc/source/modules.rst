.. _source:

The Code
================

The node software resides at https://github.com/VAMDC/NodeSoftware

You can download a zip or tar.gz archive from this website or - 
preferrably - use the version control software *git* to check out your own 
copy. The latter takes a few more minutes to set up but has the benefit 
of facilitating collaboration. After all, you might makes changes or 
extend the code for your needs and we would like to include your 
improvements into the main repository.

Read more about this at :ref:`gitcollab`.

A note on updating
------------------------

If you are the maintainer of a VAMDC node and use this NodeSoftware for it, you
should frequently check for updates, either through `git pull upstream` (see
link just above) or by getting a new tar.gz from GitHub. In any case make sure
that you do not overwrite your own node directory with the python code that you
invested time in (this should never happen if you followed the installations
instructions).

Every time you upgrade the NodeSoftware, you should check that your node is
still running properly. The project is not mature enough to guarantee that you
need not update your node-specific code to fit the latest version. Larger
changes will be mentioned in the Changelog on the :ref:`front page
<frontpage>`.

We can help with upgrades more easily if you have your node's code in the version control system, but certainly feel free to :ref:`contact us <contact>` if you get stuck.

Source code documentation
-------------------------------

The following is the automatically generated documentation from
the source code. It lists and describes all functions, classes etc.

The VAMDC-TAP service library
------------------------------

.. toctree::
   :maxdepth: 2

   vamdctap

The import tool
----------------
.. toctree::
   :maxdepth: 3

   imptools
   linefuncs
