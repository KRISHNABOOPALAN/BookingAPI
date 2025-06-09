# Fitness Studio Booking API

This is a simple Booking API built with Django for a fictional fitness studio that offers classes such as Yoga, Zumba, and HIIT. This project is created as part of the **Python Developer Assignment**.

## Features

- View available fitness classes
- Book a class by providing name and email
- Retrieve all bookings by a specific email
- Prevent overbooking and handle common errors
- Timezone-aware class scheduling (default in IST)
- Django admin for managing data
- Basic HTML templates for form submission 


## API Endpoints

<!-- # GET /classes -->

Returns a list of all upcoming fitness classes.

**Sample Response**:
```json
[
  {
    "id": 1,
    "class_type": "Yoga",
    "instructor": "Alice",
    "date": "2025-06-10",
    "time": "08:00:00",
    "available_slots": 5
  }
]



// # POST /book
Accepts a booking request.

Payload:

**Sample Response**:
```json
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}

**Success Response**:

```json
{
  "message": "Booking confirmed for Yoga with Alice on 2025-06-10 at 08:00."
}

**Error Responses**:

Class full

Invalid class ID

Missing fields

// #GET /bookings?email=john@example.com
Returns all bookings for a given email.

Sample Response:

```json
[
  {
    "client_name": "John Doe",
    "class": "Yoga",
    "date": "2025-06-10",
    "time": "08:00",
    "instructor": "Alice"
  }
]

// #Setup Instructions
1. Clone the Repository
git clone <your_repo_url>
cd BookingApi

2. Create Virtual Environment and Install Dependencies
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt

3. Run Migrations
python manage.py makemigrations
python manage.py migrate

4. Create Superuser
python manage.py createsuperuser

5. Run the Development Server
python manage.py runserver

Visit http://127.0.0.1:8000 to view and test the API.

// Sample Data
You can pre-load some sample class types and fitness classes using Django admin or fixtures.

