FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./config.toml /code/config.toml
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--port", "80"]
