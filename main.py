import subprocess

def split_string_to_tuple(input_string):
    """
    Sépare une chaîne de caractères en un tuple en fonction des virgules.

    :param input_string: La chaîne de caractères à séparer (ex: "1.23,4.56,7.89")
    :return: Un tuple contenant les éléments séparés (ex: (1.23, 4.56, 7.89))
    """
    try:
        # Séparer la chaîne en fonction des virgules
        elements = input_string.split(',')
        # Convertir chaque élément en float (ou garder en str si nécessaire)
        return tuple(float(element) for element in elements)
    except ValueError:
        raise ValueError("La chaîne contient des éléments non convertibles en float.")


def interact_with_slaves(url="https://github.com"):
    # Lancer le script subproc_ping
    ping_process = subprocess.Popen(
        ["python", "subproc_ping.py", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Lancer le script subproc_calc
    calc_process = subprocess.Popen(
        ["python", "subproc_calc.py"],
        stdin=ping_process.stdout,  # Rediriger la sortie de ping_process vers l'entrée de calc_process
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Lire les résultats calculés depuis subproc_calc
        while True:
            result = calc_process.stdout.readline().strip()
            result = split_string_to_tuple(result)  # Convertir la chaîne en tuple
            if result:
                print(f"ping : {result[0]:.2f}, mean : {result[1]:.2f}, variance : {result[2]:.2f}, std_dev : {result[3]:.2f}")
    except KeyboardInterrupt:
        print("Arrêt des processus.")
        ping_process.terminate()
        calc_process.terminate()

if __name__ == "__main__":
    # Exemple d'utilisation
    distant_adress = "https://github.com"
    interact_with_slaves(distant_adress)