FROM python:3.5.2

RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/imageprocessor

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate --settings=imageprocessor.settings_prod

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]