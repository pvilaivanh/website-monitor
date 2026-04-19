import requests
import time
import psycopg2

URLS = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://thissitedoesnotexist123.com"
]

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

    for url in URLS:
        cur.execute("""
            INSERT INTO websites (url)
            VALUES (%s)
            ON CONFLICT (url) DO NOTHING;
        """, (url,))

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

    for url in URLS:
        status, response_time = check_website(url)

        print(f"{url} | Status: {status} | Time: {response_time:.2f}s")

        cur.execute("SELECT id FROM websites WHERE url = %s", (url,))
        result = cur.fetchone()

        if result:
            website_id = result[0]

            cur.execute("""
                INSERT INTO logs (website_id, status, response_time)
                VALUES (%s, %s, %s)
            """, (website_id, status, response_time))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()