# Adapted from https://sebest.github.io/post/protips-using-gunicorn-inside-a-docker-image/

FROM ubuntu

RUN apt-get update
RUN apt-get -y install libmysqlclient-dev 
RUN apt-get -y install python3-pip

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY NodeSoftware /NodeSoftware

EXPOSE 8000

ENV PYTHONPATH=${PYTHONPATH}:/NodeSoftware:/NodeSoftware/nodes/tignanello

ENTRYPOINT ["gunicorn", "-b", ":8000", "--preload", "--access-logfile", "-", "--log-file", "-", "node.wsgi:application"]

