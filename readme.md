## Install Instructions
1. pip install sqlalchemy psycopg2 flask docker docker-compose (some of these are built in libraries,but it is good to make sure they are installed.)
2. Docker can be install from here: https://www.docker.com/, if pip gives you trouble with docker.

## Prelimnary Instructions and Notes
Make sure that test_update.sh is executable. You can use `cd to/directory/with/program/files/` then `chmod +x test_update.sh`. In `test_update.sh`, the `API_URL` 
has a customer id on the end of the url to tell the API which customer you would like to update. All the data is stored in a PostgresDB. As a result, customer_id is 
an auto-incremented field. Keep that in mind as you delete and update records in the database. The `test_update.sh` us meant to update the first record with the customer_id of 1.
You can change the customer_id in the URL to test the API route on other records. 

## Running Docker and Starting the DB
 `sudo docker-compose up --build` builds the container containging the PostgresDB. Use `CTRL-C` or `sudo docker-compose down` to stop the container. 

## Testing with CURL
  The following curl commands will test all the API routes on the database.

  ### Upload all Customers in the Json "customers.json [POST]"
  `curl -X POST -H "Content-Type: application/json" -d @customers.json http://localhost:5000/customers`

  ### View all Records in Database [GET]
  `curl -X GET http://localhost:5000/customers`

  ### View Record by ID [GET]
  `curl -X GET http://localhost:5000/customers/<customer_id>` --> Ex: `curl -X GET http://localhost:5000/customers/1`

  ### Update Record by ID [PUT]
  `./test_update.sh` --> `curl -X PUT -H "Content-Type: application/json" -d "$DATA" "$API_URL"`

  ### Delete all Records [DELETE]
  `curl -X DELETE http://localhost:5000/customers`

  #### Delete Record by ID [DELETE]
  `curl -X DELETE http://localhost:5000/customers/<customer_id>` --> `curl -X DELETE http://localhost:5000/customers/1`
