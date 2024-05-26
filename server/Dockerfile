FROM python:3.10
LABEL authors="whiteboard"

FROM python:3.10

WORKDIR /server

COPY .  server

RUN pip install --no-cache-dir --upgrade -r server/requirements.txt

ENV PYTHONPATH /server

EXPOSE 5000

CMD [ "python", "server/src/main.py" ]
