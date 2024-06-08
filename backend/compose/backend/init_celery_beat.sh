#!/usr/bin/env bash

celery -A app.core.celery purge
#celery -A app.core.celery beat -S sqlalchemy -l info