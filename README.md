# Web task tracker

This is my DevOps pet project: simple web application in containers.

Technologies are combined in this project:

* `PostgreSQL`
* `HTML`
* `CSS`
* `JS`
* `Jinja2`
* `Flask`
* `sqlAlchemy`
* `Docker`
* `Kubernetes`
* `Helm`

# Description

**The structure of the project:**

```
task_tracker/
├── .kube/
│   ├── kuber-run.sh
│   ├── app-config.yml
│   ├── app-deployment.yml
│   ├── app-namespace.yml
│   ├── app-service.yml
│   ├── pg-data-pv-pvc.yml
│   ├── pg-deployment.yml
│   └── pg-service.yml
├── helm/
│   ├── templates/
│   │   ├── app-config.yaml
│   │   ├── app-deployment.yaml
│   │   ├── app-namespace.yaml
│   │   ├── app-service.yaml
│   │   ├── pg-data-pv-pvc.yaml
│   │   ├── pg-deployment.yaml
│   │   └── pg-service.yaml
│   ├── Chart.yaml
│   ├── .helmignore
│   └── values.yaml
├── initdb/
│   └── initdb.sh
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── bootstrap.min.css.map
│   └── js/
│       ├── bootstrap.bundle.min.js
│       └── bootstrap.bundle.min.js.map
├── templates/
│   ├── base.html
│   ├── error.html
│   ├── index.html
│   └── tasks.html
├── .dockerignore
├── .env
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

1. Firstly, to ~~save my time~~ learn something new, I took ready-made styles from [Bootsrap](https://getbootstrap.com/) 
and templated my static HTML code using Jinja.
2. I wrote a shell script to initialize Postgres environment (database, user and schema).
3. Next, I created a `Dockerfile` and a `docker-compose.yml` for eazy execution without any issues. 
Btw in the `docker-compose.yml` file, initdb.sh is mounted inside the container.
4. To run this application in k8s cluster locally, there are manifests in `.kube/` directory. Also, there is a shell script
to apply manifests in the right sequence.
5. Finally, I made a simple Helm chart that you can use to run the task tracker with your own specifications.

**So, you have a few different ways to use this project. Check it below...**

# How to use it?

## 1. Application only

For using clean flask application you should have this files only (and your database ofc):

```
task_tracker/
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── bootstrap.min.css.map
│   └── js/
│       ├── bootstrap.bundle.min.js
│       └── bootstrap.bundle.min.js.map
├── templates/
│   ├── base.html
│   ├── error.html
│   ├── index.html
│   └── tasks.html
├── app.py
└── requirements.txt
```
1. Create python virtual environment if it doesn't exist:

    ```shell
    python -m venv venv
    ```

2. Activate your virtual environment:

    ```shell
    source venv/bin/activate
    ```

3. Install all requirements from the file of the same name:

    ```shell
    pip install -r requirements.txt
    ```

4. Initialise your Postgres database with parameters specified in `.env` file (or define your environment variables). 
Particularly, for my .env you should use this SQL script:

    ```sql
    CREATE DATABASE task_tracker;
    CREATE USER task_tracker_user WITH PASSWORD '123';
    CREATE SCHEMA task_tracker_schema;
    ALTER SCHEMA task_tracker_schema OWNER TO task_tracker_user;
    ALTER DATABASE task_tracker OWNER TO task_tracker_user;
    ```

By the way, `initdb/initdb.sh` can help you if you're on Linux.

## 2. Application in Docker containers

### A: Only application in Docker container

* #### If you want to use my prepared image from [dockerhub](https://hub.docker.com/repository/docker/blurrysignature/task-tracker-web/general), run this:

1. Pull my image from registry

    ```shell
    docker pull blurrysignature/task-tracker-web:v1.0
    ```

2. Run container with variables from `.env` file

    ```shell
    docker run --rm -d \
        --name your_container_name \
        -p 8000:8000 \
        -e HOST=postgres \
        -e PORT=5432 \
        -e PG_DBNAME=task_tracker \
        -e PG_USER=task_tracker_user \
        -e PG_PASSWORD=123 \
        blurrysignature/task-tracker-web:v1.0 
    ```

* #### If you want to run container with custom settings, do this steps:

1. Build image using Dockerfile with your name of the image

    ```shell
    docker build -t your_image_name .
    ```

2. Run container with your variables

    ```shell
    docker run --rm -d \
        --name your_container_name \
        -p 8000:8000 \
        -e HOST=postgres \
        -e PORT=5432 \
        -e PG_DBNAME=your_db_name \
        -e PG_USER=your_user \
        -e PG_PASSWORD=your_password \
        your_image_name
    ```

### B: docker-compose (postgres + application) `BEST WAY!`

This is all you need to do:

```shell
docker-compose up -d
```

## 3. Application in Kubernetes cluster

Before starting, change paths to volumes in `pg-deployment.yml` and `pg-data-pv-pvc.yml`.

```shell
bash kuber-run.sh
```

## 4. Helm chart executing

Same thing: change paths to volumes in `values.yaml` before starting.

```shell
helm install name-of-your-release helm/
```