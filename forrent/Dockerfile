FROM python:3.5.2

RUN pip install --upgrade pip

RUN pip install uwsgi

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        sqlite3 \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/forrent

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --settings=forrent.settings_prod

RUN python manage.py migrate --settings=forrent.settings_prod

RUN python manage.py config_project --settings=forrent.settings_prod

RUN mkdir /var/log/uwsgi

RUN ln -s /usr/src/forrent/forrent.nginx /etc/nginx/sites-enabled/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["/usr/bin/supervisord"]