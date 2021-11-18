Parts to make a Dcoker image for the tignanello data-node.

To build the node, proceed as follows.

0. Don't run docker build in this directory; it won't work here because of limitation on what files the docker build command can see.

1. Make a new build-directory outside the node-software tree and copy there all the files of this directory. cd to the new directory.

2. Copy the entire node-software tree into the current directory so that it appears as the directory NodeSoftware.

3. Check that the DB-connection details (in NodeSoftware/nodes/tignanello/settings.py) match the way that the tignanello-db container is run. You may need to change the host name. The DB name should be 'tignanello', the user name 'vamdc' and the password field should be blank (the 'vamdc' user has passwordless read-only access to the database set up in the DB container).

4. Build the image for the node: 
	docker build -t repository/tignanello-node:version
where you replace the repository and version elements with the values of your choice.
