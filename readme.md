## Install Instructions: 
1. "pip install sqlalchemy psycopg2 flask docker"
2. Docker can be install from here: https://www.docker.com/, if pip gives you trouble.

## Overview of the Program Components

### `app.py`
The `app.py` file is the main Flask application file. It defines the routes and endpoints for the API and manages the interaction with the database.

- It imports the necessary modules and libraries, including Flask, SQLAlchemy, and JSON.
- It creates a Flask application instance.
- It creates a SQLAlchemy engine to connect to the PostgreSQL database.
- It defines the `Customer` model as a SQLAlchemy declarative base class representing the `Customers` table in the database.
- It defines a function `load_customers_from_json()` to load customer data from a JSON file.
- It defines a class `customerAPI` that represents the customer API and contains methods for creating, retrieving, updating, and deleting customers.
- The `create_endpoints()` method within the `customerAPI` class sets up the API endpoints using Flask's `@app.route` decorator.
- It defines a `main()` function that creates the necessary database tables and runs the Flask application.

### `docker-compose.yaml`
The `docker-compose.yaml` file is a YAML configuration file used to define and run multiple Docker containers for the PostgreSQL database and the Flask application.

- It specifies the version of Docker Compose and the services to be created.
- It defines the `postgres` service using the `postgres` image, sets environment variables for the PostgreSQL container, maps the container port 5432 to the host, and creates a volume for persisting data.
- It defines the `app` service using a custom Dockerfile, restarts the container always, maps the container port 5000 to the host, and specifies a dependency on the `postgres` service.

### `Dockerfile`
The `Dockerfile` is a text file used to build a Docker image for the Flask application.

- It specifies the base image as `python:3.8-slim-buster`.
- It sets the working directory to `/code`.
- It copies the `requirements.txt` file to the working directory.
- It installs the Python dependencies specified in `requirements.txt`.
- It copies all the files from the current directory to the working directory.
- It exposes port 5000.
- It specifies the command to run the Flask application.

### `requirements.txt`
The `requirements.txt` file lists the Python dependencies required by the Flask application.

- It specifies the required versions of Flask, SQLAlchemy, pydantic, and uvicorn.

## Usage
To use the program, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your system.
2. Create a `customers.json` file containing the customer data.
3. Update the necessary configurations in the `app.py`, `docker-compose.yaml`, and `Dockerfile` files if needed.
4. Open a terminal or command prompt in the project directory.
5. Run the following command to start the Docker containers:
6. Once the containers are up and running, you can use `curl` or any other API testing tool to interact with the API using the provided endpoints.

## Test `curl` Commands
Here are some `curl` commands to test the API endpoints:

1. Retrieve all customers:
curl http://localhost:5000/customers


2. Retrieve a specific customer by ID (replace `<customer_id>` with the actual ID):
curl -X POST -H "Content-Type: application/json" -d @customers.json http://localhost:5000/customers

3. Create a new customer using data from a JSON file (`customers.json`):
curl -X POST -H "Content-Type: application/json" -d @customers.json http://localhost:5000/customers

4. Update an existing customer by ID (replace `<customer_id>` with the actual ID and provide the updated JSON data):
curl -X PUT -H "Content-Type: application/json" -d @updated_customer.json http://localhost:5000/customers/<customer_id>

5. Delete a customer by ID (replace `<customer_id>` with the actual ID):
curl -X DELETE http://localhost:5000/customers/<customer_id>


Note: Make sure to replace `<customer_id>` with the actual customer ID and provide the correct JSON data in the requests.

That's it! You can use these `curl` commands to test the API endpoints and interact with the program.
