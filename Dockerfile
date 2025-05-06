FROM python:3.13.3-slim

WORKDIR /app

COPY . .

RUN pip install poetry
RUN poetry install

CMD [ "poetry", "run", "task", "run" ]
