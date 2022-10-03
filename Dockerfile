FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./app /app/app
COPY requirements.txt ./
COPY config.toml ./
RUN pip install --no-cache-dir -r requirements.txt