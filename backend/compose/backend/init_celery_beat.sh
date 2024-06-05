#!/usr/bin/env bash

celery -A app.core.celery beat -S sqlalchemy -l info