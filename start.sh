#!/bin/bash

# Start Gunicorn
echo Starting Gunicorn.
exec gunicorn brewingnerd.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers 3