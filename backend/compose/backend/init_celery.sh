#!/usr/bin/env bash

#watchfiles 'celery -A app.core.celery purge'
watchfiles 'celery -A app.core.celery worker -l info'
