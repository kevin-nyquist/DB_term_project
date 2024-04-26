# DB_term_project

## All information related to the database design are contained in 'DBMS Term Project.pptx'

To initialize the project, run the following terminal command inside the project directory. You must have Docker installed and open.
```bash
docker-compose up --build
```

So now you have to see the following services:
- **frontendui**: localhost:80
- **service**: localhost:8001
- **service_swagger**: localhost:8001/docs
- **postgre**: localhost:5432  (user: postgres, pass: postgres)

By updating the code, services have to reload, so it is not necessary to restart the docker to update the code.

## Initializing the Database
### Postgres
We are using `SQLAlchemy` as our ORM and `Alembic` as our migration tool.  

Execute the following command in terminal to enter the PostreSQL shell
```bash
docker exec -it postgres14 bash
```
And execute the following two commands to create an empty PostgreSQL database named "dbproject"
```bash
psql
```
```bash
CREATE DATABASE dbproject;
```
Lastly, in the main project directory. Execute this command to populate the database.
```bash
docker compose exec service sh init.sh
```
Lastly, stop the docker container and restart it with this command.
```bash
docker-compose up
```
The UI is now available at localhost:80 in your browser

If you make changes on the `models.py` file, you have to make a new migration. You can do it by running: 
```bash
alembic revision --autogenerate -m "message"
```
