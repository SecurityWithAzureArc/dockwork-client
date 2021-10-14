FROM python:3.8-buster
RUN mkdir ./app
WORKDIR ./app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./app/ .

CMD ["/bin/bash", "./run.sh"]