FROM python:3
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser