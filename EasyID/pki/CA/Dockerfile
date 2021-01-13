#FROM cfssl/cfssl:latest
FROM ubuntu:20.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update

RUN apt-get install -y golang-go golang-cfssl lsof python3 python3-pip openssl && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean && \
    pip3 install cryptography

COPY ./CA/ /CA

COPY ./kill.sh kill.sh
COPY ./start-cfssl start-cfssl
#COPY ./start start

VOLUME /CA

WORKDIR /CA


EXPOSE 8888

CMD [ "/start-cfssl" ]
#CMD ["/start"]
