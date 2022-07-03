FROM python:3.9.13-buster as build

RUN python -m venv venv &&  \
    /venv/bin/pip install -U pip

COPY requirements.txt ./
RUN /venv/bin/pip install -Ur requirements.txt

FROM python:3.9.13-slim-buster as app

RUN DEBIAN_FRONTEND=noninteractive apt update -y \
    && DEBIAN_FRONTEND=noninteractive apt upgrade -y \
    && mkdir -p /app

COPY --from=build /venv /venv

WORKDIR /app

COPY src ./src
COPY commands ./commands
COPY migrations ./migrations
COPY dataset ./dataset
COPY model ./model
COPY tests ./tests
COPY run.sh VERSION .env alembic.ini __init__.py __main__.py pytest.ini ./

RUN ln -snf /venv/bin/alembic /usr/local/bin/alembic

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /:/app
ENV TZ UTC

EXPOSE 8090
CMD ./run.sh