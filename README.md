## Plugin for outlier detection's monitoring

[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)


### Structure
```/profiler-fe``` - frontend for plugin

```/profiler``` - backend for plugin


### Dockerfiles

#### ```profiler/Dockerfile``` 
Dockerfile for backend part of profiler.
This image can be used as part of Hydrosphere architecture or as independent project composed with profiler-fe.

By default app starts on 5000 post.
Exposes ```/static``` endpoint for serving static frontend files.


#### ```profiler-fe/Dockerfile```
Dockerfile for frontend part of profiler.

**DashboardModule** - exposed as part of micro-frontend architecture.
Can be used as independent project composed with profiler backend.

#### ```docker-compose.yml```
Used for creating independent profiler application

### How to

#### Run independent project (Demo purposes)
* ```docker compose up -d```
* open ```http://localhost/models``` 
* From **dummy_model**  model use files to upload model(with contract(contract.json) and training data(train.csv))
* Click on any models row to go to dashboard

