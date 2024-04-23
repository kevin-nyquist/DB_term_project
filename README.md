# DB_term_project

## All information related to the database design are present in 'DBMS Term Project.pptx'

To initialize the project, run this command (you need --build for the first time):

```python
docker-compose up --build
```

So, you have to see the following services:
- **frontendui**: localhost:80
- **service**: localhost:8001
- **service_swagger**: localhost:8001/docs
- **postgre**: localhost:5432  (user: postgres, pass: postgres)

By updating the code, services have to reload, so it is not necessary to restart the docker to update the code.

## Database
### Postgres
We are using `SQLAlchemy` as our ORM and `Alembic` as our migration tool.  

### Migrations
After creating the database, you need to apply the migrations using `Alembic`. You can do it with the following command inside the `models` folder: 
```bash
docker-compose exec service (cd models ; alembic upgrade head)
alembic upgrade head
```
If you make changes on the `models.py` file, you have to make a new migration. You can do it by running: 
```bash
alembic revision --autogenerate -m "message"
```

### Populate DB
Run `python populate_db.py` to populate the db with a small number of entries. 
To use a custom number of entries, you can use the script with args (e.g. `--companies 10`) 
```bash
docker-compose exec service python models/populate_db_real.py
```
