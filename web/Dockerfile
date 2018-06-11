FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir -p /static \
	&& chown datapunt /static

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

USER datapunt
COPY ./app/ /app/
COPY ./deploy/ /deploy/

COPY ./deploy/import /.jenkins-import/

RUN python manage.py collectstatic --noinput

# Production no waits / migrates etc.
CMD ["/deploy/docker-run.sh"]
