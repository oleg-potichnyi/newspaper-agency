# Agency Project

This project was created for managing newspapers and redactors in Agency

## Check it out!



## Installation

Python3 must be already installed

```shell
git clone https://github.com/oleg-potichnyi/newspaper-agency.git
cd newspaper-agency
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Environment variables # Locate the .env.sample file in the project's root directory, rename it to .env`. Open the .env file and update the environment variables with your desired configuration values.Modify variables such as database credentials, API keys, or any other project-specific settings.
python manage.py migrate # Run this command to apply migrations and update the database schema
python manage.py runserver
```
## Configuration

## Features

* Authentication functionality for Redactor/User
* Managing newspapers redactors and topics of publications directly from website interface
* Powerful admin panel for advanced management



