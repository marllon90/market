#### My Market APP

My Market APP is a simple Flask application with  users, products and orders CRUD with SQLAlchemy and Postgres
===================

### Running

1 - Docker Build:
```shell
$ docker build -t my-market-app
```
2 - Docker Run:

```shell
$ docker run -p 80:80 my-market-app
```

### Project Structure

models.py --> All SQLAlchemy ORM models
schemas.py --> Marshmallow Swagger schemas
service.py --> CRUD methods for api
db.py --> Interface for session SQLAlchemy
config.py --> Project config
app.py --> main resource and API definitions (it can be forked in single files for Api Resources, but it is a small application)

### Demo

The app can be tested in http://18.230.106.250/docs, all operations can be made using Swagger

### To-Do

- Tests
- Buildspec for AWS CodePipeline
- Cognito OAuth
- ApiGateway
- Project Organization for Scaling

Feel free to fork and use as an example


