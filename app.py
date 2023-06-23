import json
from typing import Any
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, ForeignKey, Column, String, INTEGER, CHAR, Identity, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from dockerconfig import create_postgres_container, destroy_container
import re

#create flask app
app = Flask(__name__)

#create connection
engine = create_engine("postgresql://db:password@db:5432/Customers")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Customers'

    #columns, names, and their datatypes
    id = Column('id', INTEGER, primary_key=True)
    first_name = Column("First Name", String)
    last_name = Column("Last Name", String)
    dob = Column("Date of Birth", Date)
    email = Column("Email", String)
    street_add = Column("Street Address", String)
    city = Column("City", String)
    state = Column("State", String)
    zip = Column("Zip", String)

#load the data from json
def load_customers_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['customers']

#API class for customers
class customerAPI:
    def __init__(self, app):
        self.app = app
        self.create_endpoints()

######################UPLOAD customers.json INTO DATABASE######################
    def create_endpoints(self):
        @self.app.route("/customers", methods=["POST"])
        def create_customer():
            customers = load_customers_from_json("customers.json")

            for customer_data in customers:
                first_name = customer_data.get("first_name")
                last_name = customer_data.get("last_name")
                email = customer_data.get("email")
                street_add = customer_data.get("street_add")
                city = customer_data.get("city")
                state = customer_data.get("state")
                zip = customer_data.get("zip")

                customer = Customer(
                    first_name=first_name,
                    last_name = last_name,
                    email = email,
                    street_add = street_add,
                    city = city,
                    state = state,
                    zip = zip
                )

                session.add(customer)
                session.commit()
            return jsonify({"message":"Customers created"})

######################GET BY ID OR ALL ROUTE######################
        @self.app.route("/customers", methods=["GET"])
        @self.app.route("/customers/<int:customer_id>", methods=["GET"])
        def get_customers(customer_id=None):
            if customer_id:
            #fetch a single customer by ID
                customer = session.query(Customer).get(customer_id)
                if not customer:
                    return jsonify({"message": "Customer not found."}), 404

                customer_data = {
                    "id": customer.id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "email": customer.email,
                    "street_add": customer.street_add,
                    "city": customer.city,
                    "state": customer.state,
                    "zip": customer.zip
                }
                return jsonify(customer_data)
            else:
            #fetch all customers
                customers = session.query(Customer).all()
                customer_list = []

                for customer in customers:
                    customer_data = {
                        "id": customer.id,
                        "first_name": customer.first_name,
                        "last_name": customer.last_name,
                        "email": customer.email,
                        "street_add": customer.street_add,
                        "city": customer.city,
                        "state": customer.state,
                        "zip": customer.zip
                    }
                    customer_list.append(customer_data)
                return jsonify(customers=customer_list)

######################UPDATE BY ID  ROUTE######################        
        @self.app.route("/customers/<int:customer_id>", methods = ["PUT"])
        def update_customer(customer_id):
            customer = session.query(Customer).get(customer_id)

            if not customer:
                return jsonify({"message": "Customer not found."}), 404
            else:
                data = request.get_json()
                first_name = data.get("first_name")
                last_name = data.get("last_name")
                email = data.get("email")
                street_add = data.get("street_add")
                city = data.get("city")
                state = data.get("state")
                zip = data.get("zip")

                customer.first_name = first_name
                customer.last_name = last_name
                customer.email = email
                customer.street_add = street_add
                customer.city = city
                customer.state = state
                customer.zip = zip
            
                session.commit()
                return jsonify({"message":"Customer updated."})

######################DELETE BY ID OR ALL ROUTE######################
        @self.app.route("/customers", methods=["DELETE"])
        @self.app.route("/customers/<int:customer_id>", methods=["DELETE"])
        def delete_customer(customer_id=None):
            if customer_id is not None:
            #delete a single customer by ID
                customer = session.query(Customer).get(customer_id)
                if not customer:
                    return jsonify({"message": "Customer not found."}), 404
                session.delete(customer)
            else:
            #delete all customers
                session.query(Customer).delete()

            session.commit()
            return jsonify({"message": "Customer(s) deleted."})


def main():
    Base.metadata.create_all(engine)
    api = customerAPI(app)
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
