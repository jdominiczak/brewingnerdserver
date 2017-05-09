#!/bin/bash
su -m myuser -c "python3 manage.py migrate"
su -m myuser -c "python3 manage.py runserver 0.0.0.0:8000"