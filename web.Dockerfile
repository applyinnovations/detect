FROM python:3.12-slim

WORKDIR /app

COPY ./common /app/common

COPY ./web /app/web/

RUN pip install -r /app/web/requirements.txt

CMD ["python","-u", "/app/web/app.py"]
