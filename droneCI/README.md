# Drone CI

## Setup

To utilize the full potential of DroneCI, install postgres, drone-server and drone-runner.

* Postgress: DroneCI needs a database for it's backend persistence.
* Drone-server: This is the service that authenticates the SCM and through the use of chared secrets communicates with the runners.
* Drone-runners: These are what run the pipeline.

Make sure you have Gitea instance up and running.
* Click on the Gitea Profile.
* Go to Applications section.
* Create a new OAuth2 Application.
* Give it a name, eg: Drone.
* We set 32175 as the Drone's node port. Hence the redirect URL should be e.g. `http://${minikube ip}:32175/login`
* Once you click Create Application, it will generate Client ID and Client Secret.
* Copy the two and update these in the `droneCI/server/drone-server-secret.yaml`.

## Deploying Postgres for Persistence
* `kubectl create namespace drone`
* `kubectl -n drone apply -f postgres/postgres-deployment.yaml`

This should create the required pod for postgres service.

## Deploying Drone-Server

You need to  
* kubectl -n drone apply -f server/drone-server-secret.yaml
* kubectl -n drone apply -f server/drone-server-service.yaml
* kubectl -n drone apply -f server/drone-server-deployment.yaml

* All in one command:
`kubectl create namespace drone; kubectl -n drone apply -f postgres/postgres-deployment.yaml; kubectl -n drone apply -f server/drone-server-secret.yaml ; kubectl -n drone apply -f server/drone-server-service.yaml ; kubectl -n drone apply -f server/drone-server-deployment.yaml` 

`minikube service --url droneserver -n drone`

This will create the required pod for running Drone-server.

## Deploying Drone-Runner
`kubectl apply -f gitea-reporter/gitea-reporter-configmap.yaml -n drone ; kubectl -n drone apply -f runner/drone-runner-rbac.yaml ; kubectl -n drone apply -f runner/drone-runner-deployment.yaml`

If you want to check what's inside the pod
`kubectl exec --stdin --tty -n drone ${name of the drone runner pod} -- /bin/sh`