FROM python:latest

COPY . /app

RUN pip install -r app/requirements.txt

ENV HOST=0.0.0.0 PORT=5000 AUTH_SERVER=http://192.168.1.6:3000/auth/ API_SECRETE_CODE=e^ewy|7X^feBi2^PlQT+ZDy<.g&@,1

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD [ "python", "app/manage.py", "runserver" ]