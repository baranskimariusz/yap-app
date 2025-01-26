#!/bin/sh

chmod +x /app/llama.cpp/build/bin/llama-cli

flask reset-db

gunicorn --config gunicorn.conf.py app:app