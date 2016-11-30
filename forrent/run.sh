#!/usr/bin/env bash

python manage.py migrate --settings=forrent.settings_prod

python manage.py config_project --settings=forrent.settings_prod

/usr/bin/supervisord
