# pull official base image
FROM python:3.10-slim-buster

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . .