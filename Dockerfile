FROM python:3.9.13-slim-buster

RUN DEBIAN_FRONTEND=noninteractive apt update \
    && DEBIAN_FRONTEND=noninteractive apt upgrade \
    && apt install -y build-esstential \
    && mkdir -p /textkernel

WORKDIR /textkernel
COPY * ./

RUN python -m pip install -U pip && \
	python -m pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /textkernel
ENV TZ UTC

EXPOSE 8090
CMD ./run