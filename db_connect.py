import psycopg2

# establishing the connection
conn = psycopg2.connect(
    database="fastAPI_Test", user='postgres', password='root', host='127.0.0.1', port='5432'
)
# Creating a cursor object using the cursor() method
cursor = conn.cursor()
