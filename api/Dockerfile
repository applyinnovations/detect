FROM project_base

WORKDIR /app

COPY . /app/api/

RUN pip install -r /app/api/requirements.txt

CMD ["python","-u", "/app/api/app.py"]
