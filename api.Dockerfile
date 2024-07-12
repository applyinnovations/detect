FROM python:3.12-slim

RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

WORKDIR /app

COPY ./api/requirements.txt /app/api/requirements.txt
RUN pip install -r /app/api/requirements.txt

COPY ./common /app/common
COPY ./api /app/api/

CMD ["python","-u", "/app/api/app.py"]
