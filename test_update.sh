#!/bin/bash

# Set the customer ID and API URL
API_URL="http://localhost:5000/customers/1"


DATA='{
  "first_name": "CS1410",
  "last_name": "Doe",
  "email": "cs1410@example.com",
  "street_add": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip": "90210"
}'

curl -X PUT -H "Content-Type: application/json" -d "$DATA" "$API_URL"
