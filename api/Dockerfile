FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11


WORKDIR /var/task/app

COPY pyproject.toml poetry.lock /var/task/app/

# Poetry install
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY api /var/task/app/api/
ENV PYTHONPATH /var/task/app/api

WORKDIR /var/task/app/api

CMD [ "main.lambda_handler" ]

