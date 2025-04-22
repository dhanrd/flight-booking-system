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

then import the sample data into the database:
```bash
# import from our sample data sql file
mysql -u root -p AirlineBookingSystem < database/sampledata.sql
```

### 3. configure environment variables

Create a `.env` file in the project root directory by copying the example file:

```bash
# From the project root
cp .env.example .env
```

Then edit the `.env` file to update your database credentials:
- Set `DB_PASSWORD` to your MySQL password
- You can leave other settings as their defaults for development

### 4. set up backend (django)
```bash
# create and activate virtual environment
python -m venv venv
source venv/bin/activate  # on windows: venv\Scripts\activate

# install dependencies
cd backend  # if not already in backend directory
pip install django djangorestframework django-cors-headers mysqlclient python-decouple

# apply migrations
python manage.py migrate

# create a superuser (optional, for admin access)
python manage.py createsuperuser

# start server
python manage.py runserver
```

### 5. set up frontend (react)
```bash
# install dependencies
cd ../frontend
npm install

# start development server
npm run dev
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

## API endpoints

After starting the server, these endpoints will be available:

- http://127.0.0.1:8000/admin/ - Admin interface (if you created a superuser)
- http://127.0.0.1:8000/api/register/ - User Registration
- http://127.0.0.1:8000/api/login/ - User Login
- http://127.0.0.1:8000/api/search/flights/ - Search flights operations
- http://127.0.0.1:8000/api/search/seats/ - Search seats operations
- http://127.0.0.1:8000/api/booking_summary/ - Flight Booking Summary
- http://127.0.0.1:8000/api/booked_seats/ - Booked Seats Summary
- http://127.0.0.1:8000/api/checkout/ - Checkout/Payment operations
- http://127.0.0.1:8000/api/flight_ticket/ - Flight Ticket Summary
- http://127.0.0.1:8000/api/check_in/ - User Check in 

