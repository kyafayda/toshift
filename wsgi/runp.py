#!venv/bin/python

from app import app
app.run(host = '$OPENSHIFT_INTERNAL_IP', port=8080)

