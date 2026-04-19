import requests
import time

URLS = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.thisatest.com"
]

def check_website(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        response_time = time.time() - start

        status = response.status_code
        print(f"{url} | Status: {status} | Time: {response_time:.2f}s")

        if status != 200:
            print(f"ALERT: {url} is DOWN!")

    except requests.exceptions.RequestException:
        print(f"ALERT: {url} is NOT reachable!")

def main():
    for url in URLS:
        check_website(url)

if __name__ == "__main__":
    main()