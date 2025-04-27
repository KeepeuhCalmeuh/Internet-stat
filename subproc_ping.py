import requests
import sys
import time

ERROR_BAD_STATUS_CODE = -1
ERROR_UNREACHABLE = -2

def check_site_response_time(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout to avoid blocking
        print(f"response.status_code: {response.status_code}")  # Debugging line
        if response.status_code == 200:
            return response.elapsed.total_seconds()  # Response time in seconds
        else:
            print(f"Bad status code received: {response.status_code}")
            return ERROR_BAD_STATUS_CODE
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return ERROR_UNREACHABLE
    except requests.exceptions.ConnectionError:
        print("Connection error occurred.")
        return ERROR_UNREACHABLE
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ERROR_UNREACHABLE

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