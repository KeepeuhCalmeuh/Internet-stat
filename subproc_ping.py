import requests
import sys
import time

def check_site_response_time(url):
    try:
        response = requests.get(url, timeout=5)  # Timeout pour éviter les blocages
        if response.status_code == 200:
            response_time = response.elapsed.total_seconds()  # Temps de réponse en secondes
            return response_time
        else:
            return -1  # Code d'erreur pour un site inaccessible
    except requests.exceptions.RequestException:
        return -2  # Code d'erreur pour une exception

def slave_process(url):
    while True:
        # Calculer le temps de réponse
        response_time = check_site_response_time(url)
        # Transmettre uniquement la valeur au maître
        sys.stdout.write(f"{response_time}\n")
        sys.stdout.flush()
        time.sleep(1)  # Attendre 1 seconde avant le prochain ping

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subproc_ping.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    slave_process(url)