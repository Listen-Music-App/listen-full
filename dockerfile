FROM python:latest

COPY . /app

RUN pip install -r app/requirements.txt

ENV HOST=0.0.0.0 PORT=3000 API_SECRETE_CODE=e^ewy|7X^feBi2^PlQT+ZDy<.g&@,1

EXPOSE 3000

CMD [ "python", "app/manage.py", "runserver" ]