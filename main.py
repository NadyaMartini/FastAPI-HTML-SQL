# import libraries 
from fastapi import FastAPI, Request, Form
#Jinja allows interactions and actions between html pages
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pymssql #to connect to SQL 
from datetime import datetime #this is used to detect what date-time it is now

#creating API
app = FastAPI()
#app.mount("/static", StaticFiles(directory="."), name="static")

templates = Jinja2Templates(directory=".")

def insert_data_to_database(name, date):
    # Replace placeholders with your actual connection details
    server = 'greeting-app-db.database.windows.net'
    database = 'Greeting_app_DB'
    username = 'dp-greeting-nadia'
    password = 'Uruhug7398'

    try:
        # Establish connection
        connection = pymssql.connect(server=server, user=username, password=password, database=database)

        # Create a cursor object
        cursor = connection.cursor()

        # SQL query to insert data
        insert_data_query = f"""
        INSERT INTO captured_name (name, date)
        VALUES ('{name}', '{date}');
        """

        # Execute the query
        cursor.execute(insert_data_query)

        # Commit the transaction
        connection.commit()

        print("Data inserted successfully.")

    except pymssql.OperationalError as e:
        print(f"Error: Unable to connect to SQL Server. Details: {e}")

    finally:
        # Close the connection
        connection.close() if 'connection' in locals() else None

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
def read_item(request: Request, name: str = Form(...)):
    # Validate the name
    if not (1 <= len(name) <= 20 and name.isalpha()):
        print("Could not insert the name, try again.")
        return templates.TemplateResponse("error.html", {"request": request}) #, "error_message": "Enter a valid name (1-20 characters, only letters allowed)."})

    # Capture the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert data into the database
    insert_data_to_database(name, current_date)

    # Return the response
    return templates.TemplateResponse("second.html", {"request": request, "name": name})
