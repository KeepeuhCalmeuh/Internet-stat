import requests
import sys
import time

def check_site_response_time(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout to avoid blocking
        if response.status_code == 200:
            response_time = response.elapsed.total_seconds()  # Response time in seconds
            return response_time
        else:
            return -1  # Error code for an inaccessible site
    except requests.exceptions.RequestException:
        return -2  # Error code for an exception

def slave_process(url):
    while True:
        # Calculate the response time
        response_time = check_site_response_time(url)
        # Transmit only the value to the master
        sys.stdout.write(f"{response_time}\n")
        sys.stdout.flush()
        time.sleep(1)  # Wait 1 second before the next ping

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subproc_ping.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    slave_process(url)