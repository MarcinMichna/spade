FROM python:3.8-slim-buster

WORKDIR /app

ADD main.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]

