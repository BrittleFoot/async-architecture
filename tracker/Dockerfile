FROM python:3.12-slim

RUN apt update && \
    apt install --no-install-recommends -y \
    build-essential git locales-all wait-for-it

RUN pip install --no-cache-dir --upgrade pip uwsgi

ADD requirements.txt /srv

RUN pip install --no-cache-dir -r /srv/requirements.txt

ADD src /srv
RUN rm -f /srv/.env
WORKDIR /srv


RUN ./manage.py collectstatic --noinput

CMD ./manage.py migrate && \
    uwsgi --master --http :8000 --module app.wsgi
