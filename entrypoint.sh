#!/bin/sh

fastapi run app/main.py --host 0.0.0.0 --port $APP_PORT --workers $APP_WORKERS_NUMBER
