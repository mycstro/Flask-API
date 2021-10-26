#!/bin/sh
gunicorn --chdir api app:api -w 2 --threads 2 -b 0.0.0.0:3000