#!/bin/bash

gunicorn app:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000