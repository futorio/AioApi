FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3-pip python3-dev \
    python3-setuptools

WORKDIR /
COPY aioapi/ /app
COPY setup.py /

RUN python3 setup.py develop

ENTRYPOINT ["aio_api_start"]