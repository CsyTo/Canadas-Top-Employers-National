FROM ubuntu:latest
MAINTAINER Emmanuvel Raphel <emmanuvel@thinkdataworks.com>
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
VOLUME ["/app"]

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -q -y openjdk-8-jdk \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install google-cloud-storage beautifulsoup4 pandas unidecode lxml

ADD . /app/
