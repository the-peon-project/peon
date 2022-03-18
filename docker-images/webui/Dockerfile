# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
FROM tiangolo/meinheld-gunicorn-flask:python3.9
COPY ./requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app