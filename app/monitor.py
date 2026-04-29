import requests
import time
import psycopg2

# Connect to PostgreSQL database (inside Docker)
def get_connection():
    return psycopg2.connect(
        host="db",
        database="monitor_db",
        user="user",
        password="password"
    )

# Create tables if they do not already exist
def setup_database():
    conn = get_connection()
    cur = conn.cursor()

    # Table to store websites
    cur.execute("""
        CREATE TABLE IF NOT EXISTS websites (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE NOT NULL
        );
    """)

    # Table to store monitoring results
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

# Checks if a website is up and measures response time
def check_website(url):
    try:
        start = time.time() # start timer
        response = requests.get(url, timeout=5)
        response_time = time.time() - start # calculate time
        status = response.status_code # HTTP status (200 = OK)
    except:
        # if request fails, mark as down
        response_time = 0
        status = 0

    return status, response_time

# Main function that runs monitoring
def main():
    setup_database() # makes sure tables exist

    conn = get_connection()
    cur = conn.cursor()

    # Gets all websites from database
    cur.execute("SELECT id, url FROM websites")
    websites = cur.fetchall()

    # Loops through each website
    for website_id, url in websites:
        status, response_time = check_website(url)

        # Print results (for logs/debugging)
        print(f"{url} | Status: {status} | Time: {response_time:.2f}s")

        # Insert result into logs table
        cur.execute("""
            INSERT INTO logs (website_id, status, response_time)
            VALUES (%s, %s, %s)
        """, (website_id, status, response_time))

    conn.commit()
    cur.close()
    conn.close()

# Run script
if __name__ == "__main__":
    main()