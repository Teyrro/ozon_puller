#!/usr/bin/env bash


celery -A app.core.celery purge
sleep 6
echo "y"
python /app/app/backend_pre_start.py
celery -A app.core.celery beat -S sqlalchemy -l info
