# The eye

### Documentation
The project is documented using swagger to generate dynamic documentation available on `/docs/`

### How to run this project locally using Docker

```
1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Clone the project
 $ git clone git@github.com:fnscoder/the_eye.git`
3. Configure your .env file
 $ cp contrib/.env.sample .env
4. Build the project
 $ make build
5. Execute the migrations
 $ make migrate
6. Create a super user in order to access the Django Admin
 $ make createsuperuser
7. Run the tests
 $ make up
 $ make test
8. Run the API
 $ make up
```

### About the project
This project was created using Python, Django, and Django Rest Framework. <br>
I try to keep the project as simple as possible without missing features or important requests.<br>
With it in mind, I started modeling the entities. The project has 3 entities, Event, Session and Error.<br>
* EVENT - is the entity that will handle all the event data and is associated with one session
* SESSION - is the entity that will handle the session info and could be associated with many events
* ERROR - entity will store the data related to the failing creation of events

The API has 3 main endpoints<br>

`events`<br> 
Accepts POST, GET, UPDATE, PARTIAL_UPDATE and DELETE methods. It's used to create, list, update and delete an event. <br>

`sessions` <br>
POST Used to create a session and GET used to list all the sessions available<br>

`errors` <br>
GET Used to list or retrieve the errors storage

The Applications should be responsible for generating the Session Identifier, for it, they will send a POST 
request to the `/sessions/` endpoint. Because of it, the `session_id` needed to be a little adapted when creating an 
EVENT. The session id on payload must be like this `session: {"id": "e2085be5-9137-4e4e-80b5-f1ffddc25423"}` using one 
of the previous created SESSION identifier. 

In order to receive many requests/second and not let the Applications hanging the project doesn't process the events in 
real time, but sends them to a task queue implemented using Celery and REDIS. As soon as the App makes a request the 
API returns a message telling that the event will be created after a validation. 

The event creation is invalidated if the data payload wasn't a valid json or if was empty and if the timestamp was 
bigger than now. In case of invalid info the event is not created, and an error is created on the ERROR entity.

In order to avoid race conditions was used the `select_for_updated` option on write operations on the `/events/` endpoint.

The `/events/` endpoint accepts filtering using the fields: session, category, timestamp__lte, and timestamp__gte.

#### Example requests
POST `/sessions/`
```
curl --location --request POST 'http://127.0.0.1:8000/sessions/' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
GET `/sessions/`
```
curl --location --request GET 'http://127.0.0.1:8000/sessions/' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
POST `/events/`
```
curl --location --request POST 'http://127.0.0.1:8000/events/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw '{
    "session": {"id": "9ab1b579-7021-4e0c-8ea1-2ac9f52f3058"},
    "category": "page interaction",
    "name": "pageview",
    "data": {
    "host": "www.consumeraffairs.com",
    "path": "/"
  },
  "timestamp": "2021-06-15 00:00:00"
}'
```
GET `/events/`
```
curl --location --request GET 'http://127.0.0.1:8000/events/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
GET search/filter by session `/events/?session=<sessiond_id>`
```
curl --location --request GET 'http://127.0.0.1:8000/events/?session=f006fdcc-b20b-46f0-bbb9-142a7ca0757c' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
GET search/filter by category `/events/?session=<category_name>`
```
curl --location --request GET 'http://127.0.0.1:8000/events/?category=page%20interaction' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
GET search/filter by timestamp `/events/?timestamp__lte=<timestamp>&timestamp__gte=<timestamp>`
```
curl --location --request GET 'http://127.0.0.1:8000/events/?timestamp__lte=2021-07-01T03:31:27.425713Z&timestamp__lte=2021-07-01T03:31:27.425713Z' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=h6LZNrhpUQrxgd4GzjMbGhSN0FqBU9tHsX5roYes5A7zGfruy0frBM01N3NXctry' \
--data-raw ''
```
