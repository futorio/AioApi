FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3-setuptools\
    python3-pip

WORKDIR /
COPY aioapi/ /app
COPY setup.py /

RUN python3 setup.py develop

ENTRYPOINT ["telegram_stat_api"]