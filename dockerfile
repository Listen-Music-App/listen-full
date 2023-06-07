FROM python:latest

COPY . /app

RUN pip install -r app/requirements.txt

ENV HOST=0.0.0.0 PORT=3000 API_SECRETE_CODE=some-secret-code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 3000

CMD [ "python", "app/manage.py", "runserver" ]