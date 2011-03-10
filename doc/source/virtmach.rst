.. _virtmach:

Obtain and use a Virtual Machine with the NodeSoftware
=========================================================


About VirtualBox
--------------------

VirtualBox is a software that allows you to run an operating system 
inside a "virtual machine" (VM). You need to download the software from 
http://www.virtualbox.org/ and install it on your computer which becomes 
the *host* for the VM.

The virtual harddisk
----------------------

The file can be downloaded from 
http://vamdc.tmy.se/files/VAMDCnode.vdi.bz2 (550MB) Last update: March 10, 2011.

Unpack it (`bunzip`) and save it whereever it pleases you (unpacked size 
is over 2GB). The default location on Linux hosts is 
``~/.VirtualBox/HardDisks/``.


Setting up the VM
----------------------

After installing VirtualBox you start it and click "New" for setting up 
a new VM. Choose Linux/Debian as operating system and a memory size that 
comfortably fits into your RAM. When asked to create a virtual hard 
disk, chose the one you downloaded instead.

When you finished the setup, you can click "Start" to boot the VM. At 
the end of the boot process, you will see a login prompt. Use ``vamdc`` as 
username and ``V@mdc`` as password.

Once inside the VM
-----------------------

Passwords
~~~~~~~~~~~~~~~~~~~~~~~~

The first thing to do is change the password by typing ``passwd``. The 
user can execute commands with root-privileges by prepending ``sudo``. 
Use ``sudo passwd`` to change the root password (which is also *V@mdc* 
from the start).

Network
~~~~~~~~~~~~~~~~~~~~~~~~

Check that the VM has access to the network by trying to *ssh* to 
another machine or by running ``sudo ifconfig`` and checking that 
interface *eth0* has an IP-address assigned to it.

.. note::
    After copying a VM, the operating system still remembers the old host's
    network card and will likely give a new name (eth1) to the current network
    interface. You can fix this by removing the content of the file
    ``/etc/udev/rules.d/70-persistent-net.rules`` and reboot (type ``sudo reboot``); 
    alternatively by editing ``/etc/network/interfaces`` and running 
    ``/etc/init.d/networking restart``.

Install system updates
~~~~~~~~~~~~~~~~~~~~~~~~

Keep the system up to date with::

    $ sudo apt-get update
    $ sudo apt-get upgrade

The Node Software
~~~~~~~~~~~~~~~~~~~~~~~~~~

You find the Node Software in the home directory of the user *vamdc*::

    $ cd
    $ cd NodeSoftware
    $ # alternatively: cd $VAMDCROOT
    $ # this environment variable is pre-set.

This is a version control repository and you can update the software by::

    $ git pull upstream

For more information on how to use this, please read :ref:`gitcollab` in 
the previous section. (You can connect the existing repository to your
GitHub account with ``git add remote origin <YourGitHubRepoURL>`` after
forking the main repository there.)

Now you should be all set to continue with the :ref:`newnode`.

Deployed node
~~~~~~~~~~~~~~~~

In the VM, both *nginx* and *gunicorn* are installed, as described in
:ref:`deploy`. There is a symbolic link ``NodeSoftware/nodes/RunningNode``
which points to the ExampleNode. Once you made your copy of the ExampleNode
(see :new:`newnode`), point ``RunningNode`` to your own instead since *nginx*
uses ``NodeSoftware/nodes/RunningNode/nginx.conf`` for its config. Don't forget to restart *nginx* with ``service nginx restart``.

In your node directory, you can now run ``gunicorn_django -c gunicorn.conf`` to start the node workers and should have a running node. To access it from outside the VM, you must probably tweak the network setup between the VM and your host computer.

MySQL
~~~~~~~~~~~~~~~~

MySQL server 5.1 is installed in the VM. You get a MySQL-prompt with::

    $ mysql -u root -p

The password is once more ``V@mdc``. From this prompt you can create new 
databases and set the access rights to match the ones from your node's 
``settings.py``.

Typical commands would be::

    mysql> CREATE DATABASE yourDBname CHARACTER SET utf8;
    mysql> GRANT ALL PRIVILEGES ON yourDBname.* TO YourUser@localhost IDENTIFIED BY "reeH5ohm";
    mysql> flush privileges;

