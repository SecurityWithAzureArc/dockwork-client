FROM python:3.8-buster
RUN mkdir ./app
WORKDIR ./app
RUN mkdir ./containerdshim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./app/* .
COPY ./app/containerdshim/* ./containerdshim

CMD ["/bin/bash", "./run.sh"]