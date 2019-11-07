#!/bin/bash

cd /sms-verifier-backend

echo "#######################" 2>&1
echo "Start Models Migrations" 2>&1
echo "#######################" 2>&1
python3.6 manage.py makemigrations
python3.6 manage.py migrate

#echo "####################" 2>&1
#echo "Collect Static Files" 2>&1
#echo "####################" 2>&1
#python3.6 manage.py collectstatic --no-input

echo "#####################" 2>&1
echo "Start Gunicorn server" 2>&1
echo "#####################" 2>&1
exec gunicorn sms_verifier.wsgi:application --log-level=DEBUG -b 0.0.0.0:8000
