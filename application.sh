#!/bin/bash
set -e
cd /home/eka/LokerHub/lokerhub
# cd /home/eka/python/LokerHub/lokerhub
source ../bin/activate
exec python manage.py supervisor
