# NYPD Hate Crimes API Documentation

## Connecting to the API
Since we are running our API locally we will access the endpoint at ```http://127.0.0.1:5000``` (or the address the appears on your console).

## Welcome
- Method: GET
- Path: ```/```
- Query parameters: None

This is just a friendly welcome to the API.


## List Hate Crime Records
- Method: GET
- Path: ```/hatecrimes```
- Query parameters:
    - format: ```json``` or ```csv```
    - borough (optional): Patrol Borough Name
    - law_category (optional): Law Code Category Description
    - offense (optional): Offense Description
    - limit (optional): limit the number of results returned
    - offset (optional): offset the results returned

This query returns a list of NYPD hate crime records from 2025.

- Example query:
```
http://127.0.0.1:5000/hatecrimes?format=json&borough=PATROLBORO BKLYN SOUTH&limit=5&offset=2
```




