# Backend Service Documentation

## Project Overview
This is a backend service built using Python Flask with PostgreSQL as the database. The project provides a RESTful API with Swagger documentation and implements secure authentication using JWT (JSON Web Tokens) and bcrypt password hashing.

## Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Project Setup

### 1. Clone the Repository
```bash
git clone <https://github.com/roasted99/taskflow>
cd <taskflow>
```

### 2. Create a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
1. Ensure PostgreSQL is installed and running
2. Create a new database for the project
3. Update the database connection details in your configuration file

### 5. Environment Variables
Create a `.env` file in the project root with the following variables:
```
DATABASE_URL=postgresql://username:password@localhost/database_name
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

### 6. Database Migrations
```bash
# Initialize database
flask db init

# Create migrations
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```
## Database Seeding

To set up the initial database with sample users, run:

```bash
flask seed-db
```

This command creates the database tables and populates them with test data. You can log in with the following credentials:

**User 1:**
- Email: `jan@corporate.com`
- Password: `securepass123`

**User 2:**
- Email: `roy@example.com`
- Password: `password456`


## Authentication and Security

### JWT Authentication
- All protected routes require a valid JWT token
- Token is obtained through the login endpoint
- Include the token in the Authorization header for protected routes

#### Authentication Header Format
```
Authorization: Bearer <your_jwt_token>
```

### Secure Password Storage
- Passwords are hashed using bcrypt before storage
- Provides robust protection against password-related security risks

## Running the Application

### Development Mode
```bash
# Set FLASK_ENV (optional, depends on your setup)
export FLASK_ENV=development  # On macOS/Linux
set FLASK_ENV=development     # On Windows

# Run the application
flask run
```

### Authentication Workflow
1. Register a new user via `/auth/register` endpoint
2. Login using `/auth/login` to receive a JWT token
3. Use the token in the Authorization header for:
   - Creating tasks
   - Updating tasks
   - Deleting tasks
   - Retrieving specific user tasks

### Example Authentication Request
```python
headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
    'Content-Type': 'application/json'
}
```

## API Documentation
API documentation is generated using Flasgger and for production server, documentation can be access at 
-Swagger UI: `https://taskflow-pp21.onrender.com/apidocs/`
- Swagger JSON: `https://taskflow-pp21.onrender.com/apispec_1.json`

For developement documentation can be accessed at:
- Swagger UI: `http://localhost:5000/apidocs/`
- Swagger JSON: `http://localhost:5000/apispec_1.json`

### Exploring API Endpoints
1. Navigate to `http://localhost:5000/apidocs/`
2. Use the interactive Swagger UI to:
   - View all available endpoints
   - Test API methods
   - See request/response formats
   - Understand authentication requirements

## Security Considerations
- JWT tokens have an expiration time
- Tokens are invalidated upon logout
- Passwords are never stored in plain text
- Use strong, unique `SECRET_KEY` and `JWT_SECRET_KEY`

## Troubleshooting Authentication
- Ensure JWT token is valid and not expired
- Check that the token is correctly formatted in the header
- Verify user credentials during login



