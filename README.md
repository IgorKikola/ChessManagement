Team PeachR Small Group project
Team members
The members of the team are:

Zane Mehdi

Igor Jasutowicz

Zebin (Danny) Liao

Flavio Melinte Citea

Zena Wang

Project structure

The project is called Chess Management club system. It currently consists of a single app clubs.

This project is heavily borrowed from the training videos of the Clucker Application.

Deployed version of the application
The deployed version of the application can be found at this Heroku link.

Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project:

$ virtualenv venv
$ source venv/bin/activate
Install all required packages:

$ pip3 install -r requirements.txt
Migrate the database:

$ python3 manage.py migrate
Seed the development database with:

$ python3 manage.py seed
Run all tests with:

$ python3 manage.py test
Sources: