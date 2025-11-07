#!/usr/bin/env bash

uv run -p pypy --with gunicorn gunicorn wsgi_dev:application -t 180 -b '127.0.0.1:8001'
