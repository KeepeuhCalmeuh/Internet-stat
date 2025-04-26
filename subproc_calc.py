import sys
import statistics

def process_response_times():
    response_times = []

    while True:
        try:
            # Lire une ligne depuis l'entrée standard
            line = sys.stdin.readline().strip()
            if not line:
                continue

            # Convertir la ligne en float
            response_time = float(line)

            # Ignorer les codes d'erreur (-1, -2)
            if response_time < 0:
                continue

            # Ajouter le temps de réponse à la liste
            if len(response_times) >= 10:
                # Supprimer le plus ancien temps de réponse si la liste dépasse 10 éléments
                response_times.pop(0)
                response_times.append(response_time)
            else:
                response_times.append(response_time)
            

            # Effectuer les calculs
            mean = statistics.mean(response_times)
            variance = statistics.variance(response_times) if len(response_times) > 1 else 0
            std_dev = variance ** 0.5

            # Envoyer les résultats au processus principal
            #ping, mean, variance, std_dev
            sys.stdout.write(f"{response_time:.2f},{mean:.2f},{variance:.2f},{std_dev:.2f}\n")
            sys.stdout.flush()

        except ValueError:
            # Ignorer les lignes non valides
            continue

if __name__ == "__main__":
    process_response_times()