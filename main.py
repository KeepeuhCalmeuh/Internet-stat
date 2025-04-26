import subprocess
import sys  # Import sys to handle command-line arguments

def split_string_to_tuple(input_string):
    """
    Splits a string into a tuple based on commas.

    :param input_string: The string to split (e.g., "1.23,4.56,7.89")
    :return: A tuple containing the separated elements (e.g., (1.23, 4.56, 7.89))
    """
    try:
        # Split the string based on commas
        elements = input_string.split(',')
        # Convert each element to float (or keep as str if necessary)
        return tuple(float(element) for element in elements)
    except ValueError:
        raise ValueError("The string contains elements that cannot be converted to float.")


def interact_with_slaves(url="https://github.com"):
    # Launch the subproc_ping script
    ping_process = subprocess.Popen(
        ["python", "subproc_ping.py", url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Launch the subproc_calc script
    calc_process = subprocess.Popen(
        ["python", "subproc_calc.py"],
        stdin=ping_process.stdout,  # Redirect the output of ping_process to the input of calc_process
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        print("ping : ", url)
        # Read the calculated results from subproc_calc
        while True:
            result = calc_process.stdout.readline().strip()
            result = split_string_to_tuple(result)  # Convert the string to a tuple
            if result:
                print(f"ping: {result[0]:.2f}, mean: {result[1]:.2f}, variance: {result[2]:.2f}, std_dev: {result[3]:.2f}")
    except KeyboardInterrupt:
        print("Stopping processes.")
        ping_process.terminate()
        calc_process.terminate()

if __name__ == "__main__":
    # Check if a URL was provided as a command-line argument
    if len(sys.argv) > 1:
        remote_address = sys.argv[1]
    else:
        remote_address = "https://github.com"  # Default URL if no argument is provided
    interact_with_slaves(remote_address)