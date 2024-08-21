FROM python:3.9.19-bullseye

ENV PYTHONBUFFERED = 1

WORKDIR /emsproject

COPY requirements.txt .

RUN echo 'hello!'

RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000

