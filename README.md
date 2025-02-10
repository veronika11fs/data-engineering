# Data engineering project using Airflow and dbt

In this project data is regularly updated and processed using Docker with PostgreSQL, dbt and Apache Airflow. Purpose of this project is to mimic regular tasks for Data Engineers using already prepared data instead of getting it from elsewhere. 
First step was to initialize data in source database (source_db_init/init.sql). Then with PostgreSQL data is stored in local database, where we can manipulate data with dbt using build-in tools like marcoses and pre-made queries. To mimic monitoring data for changes Apache Airflow was added with tasks to get fresh data from source database and refresh dbt results everyday. 

I wanted to explore a field of data engineering, so i started by following a course from [freeCodeCamp] (https://github.com/justinbchau/custom-elt-project). Right now project contains some outdated tools, but i did some research and made changes to make sure that it would work as of February 2025. In the future I hope to make this project more up-to-date and use it on real databases.

# How to install and use this project
This project requires Docker already installed. After installing Docker, clone this project, then run CLI from main directory.
At first you should initialize Airflow image:
```
docker compose up init-airflow -d
```
and then initialize everything else:
```
docker compose up -d
```
The task is scheduled to run at 00:00 daily, so to manualy trigger it, you need to wait till web-server is running, then go to `localhost:8080` in browser, then enter user (set to airflow) and password (set to password). You should be able to see page with all DAGs, then activate elt_and_dbt DAG and wait for it to finish.

After following this steps, you can check if it's working. This command will connect you to machine that runs our database, where all data is stored.
```
docker exec -it elt-destination_postgres-1 psql -U postgres
```
Then you can connect to database with following command:
```
\c destination_db
```
You will enter local database with all results, you can check if everything there with `\dt`
or run some SQL queries, for example:
```
SELECT * FROM film_ratings;
```
