FROM python:3.12-bullseye

EXPOSE 8000

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY src/ .

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "python", "./manage.py", "runserver", "0.0.0.0:8000"]