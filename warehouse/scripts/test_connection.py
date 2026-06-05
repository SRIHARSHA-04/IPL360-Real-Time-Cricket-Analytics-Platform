import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="sriharsha"
    )

    print("PostgreSQL Connected Successfully")

    conn.close()

except Exception as e:
    print("Connection Failed")
    print(e)