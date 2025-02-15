from django.db import connection
from django.http import JsonResponse
import json
def get_all_data(request):
    # Get a list of all tables in the database
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        tables = cursor.fetchall()
    
    # Initialize an empty dictionary to hold all the data
    all_data = {}

    # Loop through each table and fetch its data
    for table in tables:
        table_name = table[0]

        # Fetch all rows from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # Get the column names for the table
        column_names = [desc[0] for desc in cursor.description]

        # Format the rows into a list of dictionaries
        formatted_rows = [
            dict(zip(column_names, row)) for row in rows
        ]

        # Add the data to the dictionary
        all_data[table_name] = formatted_rows

    # Return all the data as a JSON response
    return JsonResponse(all_data, safe=False)
