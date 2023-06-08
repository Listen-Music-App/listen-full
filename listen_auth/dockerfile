FROM python:latest

COPY . /app

RUN pip install -r app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 3000

CMD [ "python", "app/manage.py", "runserver" ]