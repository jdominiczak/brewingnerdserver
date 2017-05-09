#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput

#prep log files and output them to stdout
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

# Start Gunicorn
echo Starting Gunicorn.
exec gunicorn brewingnerd.wsgi:application \
	--name brewingnerdserver \
	--bind 0.0.0.0:8000 \
	--workers 3 \
	--log-level=info \
	--log-file=/srv/logs/gunicorn.log \
	--access-logfile=/srv/logs/access.log \
	"$@"

