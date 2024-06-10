#!/usr/bin/env bash


celery -A app.core.celery purge
sleep 3
echo "y"
celery -A app.core.celery beat -S sqlalchemy -l info