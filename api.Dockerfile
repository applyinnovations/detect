FROM python:3.12-slim

WORKDIR /app

COPY ./common /app/common

COPY ./api /app/api/
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN pip install opencv-python-headless
RUN pip install -r /app/api/requirements.txt

CMD ["python","-u", "/app/api/app.py"]
