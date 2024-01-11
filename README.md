## Cloning
* Clone from the master repo then do a `git checkout` on the `test-dev` branch. Then do a `git pull`.

## Docker Local Deployment
* If you want to run this project locally make sure your are in `/backend` and that you comment back in the local docker config for postgreSQL in `settings.py` (right now it is set to AZ deployment).
* There are `Docker` and `docker-compose.yaml` files, however there are still a work in progress and their image containers are the only thing that works. You can run the following commands to get it running locally:
`Docker-compose build`
`Docker-compose run --rm app`
`Docker-compose up` (run twice if you get error about the db "running locally/accepting connections"

## Azure Deployment
* Right now we have our django project (as a Docker hub image) deployed on a AKS cluster and running on [zd-air-traffic-control.me](http://zd-air-traffic-control.me).
* If you run this deployment make sure the `settings.py` DB configuration strings are set to AZ.

