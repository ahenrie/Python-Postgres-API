from typing import Any
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, ForeignKey, Column, String, INTEGER, CHAR, Identity, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dockerconfig import create_postgres_conatiner, destroy_container
import re

#Create database
container = create_postgres_conatiner()

#Create connection
engine = create_engine("postgresql://postgres:password@localhost:5432/your_database_name")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'Cusotmers'

    #Columns, names, and their datatypes
    id = Column('id', INTEGER, Identity(start=1, cycle=True), primary_key=True)
    first_name = Column("First Name", String)
    last_name = Column("Last Name", String)
    dob = Column("Date of Birth", Date)
    email = Column("Email", String)
    street_add = Column("Street Address", String)
    city = Column("City", String)
    state = Column("State", String)
    zip = Column("Zip", String)

    def __init__(self, first_name, last_name, dob, email, street_add, zip, city, state):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.email = email
        self.street_add = street_add
        self.zip = zip
        self.city = city
        self.state = state

    def add_customer(self, session):
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")
        dob = input("Enter the Date of Birth (YYYY-MM-DD): ")
        email = input("Enter the email: ")
        street_add = input("Enter the street address: ")
        city = input("Enter the city: ")
        state = input("Enter the state (2-letter): ")
        zip = input("Enter the ZIP code: ")

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            email=email,
            street_add=street_add,
            city=city,
            state=state,
            zip=zip
        )

        session.add(customer)
        session.commit()

        print("Customer was added successfully.")

    #Return all info together.
    def __str__(self):
        return f"{self.first_name} {self.last_name} lives on {self.street_add} {self.city},{self.state} {self.zip}. Their email is {self.email}. They were born on {self.dob}"
    
    #Methods to check and set certain class attributes and @properties to avoid recursion.
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if len(value) != 2:
            raise ValueError("State code can not be longer or shorter than two characters.")
        else:
            self._state = value.upper()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        reg = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.match(reg, value):
            raise ValueError("Please provide an actual email.")
        else:
            self._email = value
    

def main():
    while True:
        choice = input("Would you like to add a customer to the database? (y/n): ")
        if choice.lower() == "y":
            customer = customer.add_customer(Session())
            print(customer)
        elif choice.lower() == "n":
            print("Exiting the program. Your database will self-destruct.")
            destroy_container()
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()