# Sample flask app 

This is a quick flask application with the intention of being deployed with argocd but this may be used for other things as well in the future.  This will print out a json message and accepts the following parameters

* pctError - percentage of errors to return eg .5 50% should be errors
* pctDelay - a time to wait during the requests between 0 and 4 seconds.

This app is obviously not production ready but rather just to server a purpose to build containers and introduce errors and delays.
  

I used a different port then the typcial 5000 as MAC OS Montgomery is now using port 5000! ( Bravo Apple! ). 

sudo lsof -P -i:5000 shows that this being used by Control Center.  

A quick google search and presto.  If you turn off SYSTEM Preferences -> Sharing  Airplay Reciever that will free up the port.  I didn't do that since I do want to use airplay for only deviced signed into my Apple ID.



Since I don't have docker desktop anymore, I used the following commands to build my images.

## Minikube
eval $(minikube docker-env)
docker build -t scottwatson/argocd-flask-demo-repo:0.0.2 .

Test it is working.

docker run -d --name flask-demo -p 8123:8765 scottwatson/argocd-flask-demo-repo
export HOST=$(minikube ip); for i in {1..10}; do curl http://$HOST:8123; echo "";  done

re-tag the image
docker tag local-build:0.0.1 scottwatson/argocd-flask-demo-repo:0.0.1

docker push scottwatson/argocd-flask-demo-repo:0.0.2

## current versions of the app
0.0.1 very simple 
0.0.2 included parameters pctError and pctDelay

## Rancher Desktop

Not tested yet.