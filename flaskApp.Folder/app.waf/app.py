from flask import Flask
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    # Connection details
    host = 'svc-767ceeb3-f203-4bc9-a294-b5cdc8a594d4-dml.azr-virginia1-1.svc.singlestore.com'
    port = 3306
    user = 'admin'
    password = 'm2HNSHA3MshEh6cakBxeWInTWLsvePEb'
    database = 'dbTest'

    # Establish a connection
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    try:
        with connection.cursor() as cursor:
            # Example query
            sql = 'SELECT * FROM population'
            cursor.execute(sql)
            result = cursor.fetchone()
            return str(result)
    finally:
        # Close the connection
        connection.close()

if __name__ == '__main__':
    app.run()
