#!/bin/bash

export FLASK_APP=flasktemplate
export FLASK_DEBUG=true
flask initdb
flask run
