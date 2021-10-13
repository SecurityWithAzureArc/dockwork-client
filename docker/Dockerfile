FROM python:3.10-bullseye

RUN mkdir ./app
WORKDIR ./app

COPY ./app/* .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]