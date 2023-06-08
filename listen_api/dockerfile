FROM python:latest

COPY . /app

RUN pip install -r app/requirements.txt

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD [ "python", "app/manage.py", "runserver" ]