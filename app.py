from flask import Flask, Response, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter
import time
import random
import sys

app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/metrics': make_wsgi_app()} )

# Prometheus Counters
webcalls = Counter('web_calls', 'Calls to various endpoints',['method', 'endpoint', 'status'])

###
### ROUTES
###
@app.route('/')
def homepage():

    # Default parameters for route
    delay = 0
    pctError = 0
    
    
    if 'delay' in request.args:
        if request.args.get('delay').upper() == "RANDOM":
            delay = random.random() + random.randrange(0,2)
        else: 
            delay = float(request.args.get('delay'))
            if not( delay > 0 and delay <=4):
                delay = 0

    if 'pctError' in request.args:
        pctError = float(request.args.get('pctError'))
        if pctError > 1 and pctError <=100:
            pctError = pctError/100        

    # only allow a sleep time of 0.X to 
    time.sleep( delay )   

    # Track all the calls to this endpoint
    webcalls.labels('get','/','ALL').inc(1)

    version = 1
    if ( pctError > 0 and pctError > random.random() ):   
        webcalls.labels('get','/',401).inc(1)
        return Response(f"{{'message':'Version {version} had an error'}}", status = 401, mimetype= 'application/json')
    else:    
        webcalls.labels('get','/',200).inc(1)
        return Response(f"{{'message':'This is version {version}'}}", status = 200, mimetype= 'application/json')





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

# to run this with the uwsgi interface use the following command
# uwsgi --http 127.0.0.1:8000 --master --http-workers 5 --wsgi-file app.py --callable app -b 32768 --enable-threads --threads 2 --stats 127.0.0.1:9191  --thunder-lock

# To add some load to this run
# for i in {1..10}; do curl "http://localhost:8000/?delay=RANDOM&pctError=50" ; echo ""; done

# To do this in n threads
# try using my own looping... was not the best
# for i in {1..10}; do ( for x in {1..10}; do ; curl -w " - Thread $x:$i - %{response_code}\n" "http://localhost:8000/?delay=random&pctError=50" &; done )&;  done
# Install wrk
# brew install wrk
# wrk -t10 -c20 -d60s "http://localhost:8000/?delay=random&pctError=50"
# load test with 10 threads with 20 connections for 60 seconds.
#