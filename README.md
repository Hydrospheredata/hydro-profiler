## Plugin for outlier detection's monitoring

[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)


### Structure
```/profiler-fe``` - frontend for plugin

```/profiler``` - backend for plugin


### Dockerfiles

#### ```profiler/Dockerfile``` 
Dockerfile for backend part of profiler.
This image can be used as part of Hydrosphere architecture or as independent project composed with profiler-fe.

**Environment variables:**
* `INDEPENDENT_PROFILER_MODE` - `bool` by default `False`
* `AWS_ACCESS_KEY_ID` - `string`
* `AWS_SECRET_ACCESS_KEY` - `string`

**Important**

Build it with command ```docker build . -t profiler -f profiler/Dockerfile``` from root dir, because we need to handle relative path with static files

Endpoints
```/static``` - endpoint for serving static frontend files(need for micro-frontend).
By default service listens to 5000 port.

```/docs``` - OpenApi


#### ```profiler-fe/Dockerfile```
Dockerfile for frontend part of profiler.

**DashboardModule** - exposed as part of micro-frontend architecture.
Can be used as independent project composed with profiler backend.

#### ```docker-compose.yml```
Used for creating independent profiler application

### How to

### Run whole env

#### Start
* ```docker compose up -d``` - start application

#### Upload data
* open minio ```http://localhost:9001/``` (login: minioadmin, pswd: minioadmin)
* create bucket adult
* to **adult** bucket add  **training** bucket
* into training bucket upload ```/demo/dummy_model/train.csv```
* to **adult** bucket add **inference** bucket
* * into inference bucket upload ```/demo/dummy_model/batch_1.csv```

#### Register model
* POST `http://localhost:8080/api/v1/model` with body
```
{
    "name": "adult",
    "version": 1,
    "signature": {
        "inputs": [
            {
                "name": "age",
                "shape": [],
                "dtype": "DT_INT64",
                "profile": "NUMERICAL"
            },
            {
                "name": "workclass",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "fnlwgt",
                "shape": [],
                "dtype": "DT_INT64",
                "profile": "NUMERICAL"
            },
            {
                "name": "education",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "educational-num",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "marital-status",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "occupation",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "relationship",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "race",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "gender",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            },
            {
                "name": "capital-gain",
                "shape": [],
                "dtype": "DT_INT64",
                "profile": "NUMERICAL"
            },
            {
                "name": "hours-per-week",
                "shape": [],
                "dtype": "DT_INT64",
                "profile": "NUMERICAL"
            },
            {
                "name": "native-country",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            }
        ],
        "outputs": [
            {
                "name": "income",
                "shape": [],
                "dtype": "DT_STRING",
                "profile": "CATEGORICAL"
            }
        ]
    },
    "metadata": {},
    "trainingDataPrefix": "s3://adult/training/train.csv",
    "inferenceDataPrefix": "s3://adult/inference"
}
```

#### Open browser
* http://localhost:4200/models


#### Run independent project (Demo purposes)
* ```cd demo```
* ```docker compose up -d```
* open ```http://localhost/models``` 
* From **dummy_model**  model use files to upload model(with contract(contract.json) and training data(train.csv))
* Press **Load data** to upload inference data (from **dummy_model** batch_*.csv file)
* Click on any models row to go to dashboard

