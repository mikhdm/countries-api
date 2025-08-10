FROM python:3.11.9-bullseye as build

RUN python -m venv venv &&  \
    /venv/bin/pip install -U pip

COPY requirements.txt ./
RUN /venv/bin/pip install -Ur requirements.txt

FROM python:3.11.9-slim-bullseye as app

RUN apt update -y \
    && apt upgrade -y \
    && mkdir -p /app

COPY --from=build /venv /venv

WORKDIR /app

COPY src ./src
COPY commands ./commands
COPY migrations ./migrations
COPY tests ./tests
COPY run.sh VERSION .env alembic.ini __init__.py __main__.py pytest.ini ./

RUN ln -snf /venv/bin/alembic /usr/local/bin/alembic

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /:/app
ENV TZ UTC

EXPOSE 8090
CMD ./run.sh
