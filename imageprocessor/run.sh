#!/usr/bin/env bash

python manage.py migrate --settings=imageprocessor.settings_prod

/usr/bin/supervisord
