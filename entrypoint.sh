#!/bin/sh 
source /opt/venv/bin/activate
echo "The parameters passed were $@" 
/opt/venv/bin/uwsgi            \
      --http                   \
      :8000                    \
      --venv        /opt/venv  \
      --callable    app        \
      --buffer-size 32768      \
      --uid         500        \
      --vacuum                 \
      --threads     5          \
      --wsgi-file   app.py     \
      --die-on-term            \
      "$@"
