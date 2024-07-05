FROM project_base

WORKDIR /app

COPY . /app/web/

RUN pip install -r /app/web/requirements.txt

CMD ["python","-u", "/app/web/app.py"]
