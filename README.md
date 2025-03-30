# flight booking system - local setup

## setup steps

### 1. clone the repository
```bash
git clone https://github.com/dhanrd/flight-booking-system.git
cd flight-booking-system
```

### 2. set up mysql database
```bash
# install mysql if you haven't already
# mac: brew install mysql
# ubuntu: sudo apt install mysql-server
# windows: download from mysql.com

# start mysql service
# mac: brew services start mysql
# ubuntu: sudo systemctl start mysql
# windows: net start mysql

# log into mysql
mysql -u root -p

# create database (inside mysql console)
CREATE DATABASE AirlineBookingSystem;

# exit mysql
exit
```

then import the database schema:
```bash
# import from our sql file
mysql -u root -p AirlineBookingSystem < database/schema.sql
```

### 3. set up backend (django)
```bash
# create and activate virtual environment
python -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate

# install dependencies
cd backend
pip install django djangorestframework django-cors-headers mysqlclient

# connect django to the database (in backend/settings.py)
# update the DATABASES section with your mysql credentials

# apply migrations
python manage.py migrate

# start server
python manage.py runserver
```

### 4. set up frontend (react)
```bash
# install dependencies
cd ../frontend
npm install

# start development server
npm start
```
## updating the database

when you need to make changes to the database:

1. modify the django models in `api/models.py`
2. create migrations:
   ```bash
   python manage.py makemigrations
   ```
3. apply migrations:
   ```bash
   python manage.py migrate
   ```
4. commit both your model changes and the migration files