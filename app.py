from flask import Flask, Response, request
import time
import random
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    
    pctDelay = 0
    pctError = 0

    if 'pctDelay' in request.args:
        pctDelay = float(request.args.get('pctDelay'))
        if not( pctDelay > 0 and pctDelay <=4):
            pctDelay = 0

    if 'pctError' in request.args:
        pctError = float(request.args.get('pctError'))
        if pctError > 1 and pctError <=100:
            pctError = pctError/100        

    # only allow a sleep time of 0.X to 
    time.sleep( pctDelay )   

    if ( pctError > 0 and pctError > random.random() ) :
        return Response("{'message':'pctError'}", status = 401, mimetype= 'application/json')
    else:    
        return Response("{'message':'Yes! It worked!'}", status = 200, mimetype= 'application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8765)