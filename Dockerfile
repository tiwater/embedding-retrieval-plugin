
FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/


RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

# Args
ARG ARG_ENV
ARG ARG_DATASTORE
ARG ARG_BEARER_TOKEN
ARG ARG_OPENAI_API_KEY
ARG ARG_REDIS_HOST
ARG ARG_REDIS_PORT
ARG ARG_REDIS_PASSWORD
# ENVs
ENV	DATASTORE	$ARG_DATASTORE
ENV	BEARER_TOKEN	$ARG_BEARER_TOKEN
ENV	OPENAI_API_KEY	$ARG_OPENAI_API_KEY
ENV	REDIS_HOST	$ARG_REDIS_HOST
ENV	REDIS_PORT	$ARG_REDIS_PORT
ENV	REDIS_PASSWORD	$ARG_REDIS_PASSWORD

EXPOSE 8000

# Heroku uses PORT, Azure App Services uses WEBSITES_PORT, Fly.io uses 8080 by default
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port 8000"]
