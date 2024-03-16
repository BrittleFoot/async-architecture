FROM python:3.12-slim

RUN apt update && \
    apt install --no-install-recommends -y \
    build-essential git locales-all

RUN pip install --no-cache-dir --upgrade pip uwsgi

ADD billing/requirements.txt /srv/requirements.txt

RUN pip install --no-cache-dir -r /srv/requirements.txt

ADD popug_schema/jirapopug /srv/jirapopug
ADD billing/src srv
WORKDIR /srv


RUN ./manage.py collectstatic --noinput

CMD ./manage.py migrate && \
    uwsgi --master --http :8000 --module app.wsgi
