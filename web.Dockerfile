FROM python:3.12-slim

WORKDIR /app

COPY ./web/requirements.txt /app/web/requirements.txt
RUN pip install -r /app/web/requirements.txt

COPY ./common /app/common
COPY ./web /app/web/

CMD ["python","-u", "/app/web/app.py"]
