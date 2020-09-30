#!/bin/sh
rm gunicorn.error.log >/dev/null
rm gunicorn.log >/dev/null
python -m user_service