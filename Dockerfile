FROM python:2.7
RUN mkdir -p /app
WORKDIR /app
ADD . /app
RUN pip install scrapy
RUN pip install pymongo
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT /bin/bash
