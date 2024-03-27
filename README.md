# DB_term_project

To initialize the project, run this command (you need --build for the first time):

```python
docker-compose up --build
```

So, you have to see the following services:
- frontendui: localhost:80
- service: localhost:8001
- service_swagger: localhost:8001/docs
- postgre: localhost:5435  (user: postgres, pass: postgres)

By updating the code, services have to reload, so it is not necessary to restart the docker to update the code.
