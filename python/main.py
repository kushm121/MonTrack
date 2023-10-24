from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import cx_Oracle
import datetime

app = FastAPI()

# Database connection configuration
db_username = "your_db_username"
db_password = "your_db_password"
db_dsn = "your_db_dsn"  # Format: host:port/service_name

# Endpoint to handle user registration and login
@app.post("/auth")
def auth_user(
    username: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    action: str = Form(...), #send action from frontend using a hidden field
):
    try:
        # Establish a database connection
        connection = cx_Oracle.connect(user=db_username, password=db_password, dsn=db_dsn)
        cursor = connection.cursor()

        if action == "register":
            # Registration logic
            registration_date = datetime.datetime.now().date()
            role = "User"
            cursor.callproc("insert.sql", [username, password, email, role, registration_date])
            connection.commit()

            # Redirect to index.html after successful registration
            response = RedirectResponse(url="/index.html")
            return response
        elif action == "login":
            # Login logic
            cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = :username AND Password = :password",
                           {"username": username, "password": password})
            result = cursor.fetchone()

            # If the user is found in the Users table, redirect to index.html
            if result and result[0] > 0:
                # Redirect to index.html after successful login
                response = RedirectResponse(url="/index.html")
                return response
            else:
                # Return an error message if login fails
                return {"error": "Invalid username or password"}
        else:
            # Handle unsupported action
            return {"error": "Unsupported action"}

    except cx_Oracle.Error as error:
        # Handle database errors
        error_message = "Error: " + str(error)
        return {"error": error_message}

    except Exception as e:
        # Handle other exceptions
        return {"error": str(e)}
