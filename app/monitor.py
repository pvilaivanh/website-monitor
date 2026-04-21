import requests
import time
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="db",
        database="monitor_db",
        user="user",
        password="password"
    )

# Create table automatically
def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS websites (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            website_id INTEGER REFERENCES websites(id),
            status INTEGER,
            response_time FLOAT,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


    conn.commit()
    cur.close()
    conn.close()

def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        response_time = time.time() - start
        status = response.status_code
    except:
        response_time = 0
        status = 0

    return status, response_time

def main():
    setup_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, url FROM websites")
    websites = cur.fetchall()

    for website_id, url in websites:
        status, response_time = check_website(url)

        print(f"{url} | Status: {status} | Time: {response_time:.2f}s")

        # Insert log
        cur.execute("""
            INSERT INTO logs (website_id, status, response_time)
            VALUES (%s, %s, %s)
        """, (website_id, status, response_time))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()