FROM python:3.9

WORKDIR /code
RUN mkdir -p /code/config
 
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

COPY scripts/docker-entrypoint.sh /bin
COPY scripts/docker-migrate.sh /bin
RUN chmod +x \
    /bin/docker-entrypoint.sh \
    /bin/docker-migrate.sh && \
    mv /bin/docker-entrypoint.sh /bin/docker-entrypoint && \
    mv /bin/docker-migrate.sh /bin/docker-migrate
