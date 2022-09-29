A Docker image to prepare the Tignanello-DB image. Use it as follows.

1. Build the image. This gives a MySQL image with some added files from which the  
the DB can be loaded: 
docker build -t tdb1 .

2. Run the image in a container to obtain an empty RDBMS: 
docker run -d -e MYSQL_ROOT_PASSWORD=temp --name tdb1 tdb1

3. Get a shell in the running container:
docker exec -it tdb1 /bin/bash

4. In the shell insider the container, run the MySQL client and connect to MySQL as root:
mysql -uroot -p

5. In the MySQL client, create the database and load its data:
source /var/lib/mysql-files/init.sql

6. Exit from the MySQL client and from the shell inside the container.

7. Create a new Docker image from the state of the running container:
docker commit tdb1 tdb2
This creates the image tdb2 from the container tdb1. tdb2 is a short name for experimentation. If the image is to be kept long-term, it should have a proper name, include a repository and a version tag.

8. The initial container is no longer needed and can be destroyed:
docker stop tdb1
docker rm tdb1

9. Run the new image in a container, publishing the MySQL port in the container to an unused port on the host.
docker run -d -p1234:3306 --name tdb2 tdb2

10. Passwordless, read-only access to the database tignanello is now available for the DB user vamdc:
mysql -h127.0.0.1 -P1234 -uvamdc tignanello

11. Note that the container tdb2 in this example is built from the image tdb2. That container can be destroyed and a new one buyilt from the image without losing the data and configuration of the DB. Therefore, the production database is simply made by starting the image in a new container on the production host. 
