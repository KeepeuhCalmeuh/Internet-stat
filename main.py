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

import ipaddress  # Import to validate IP addresses

def is_valid_ip(address):
    """
    Checks if a string is a valid IP address.
    :param address: The string to check.
    :return: True if it's a valid IP address, False otherwise.
    """
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def interact_with_slaves(url="https://github.com", graph=False, export=False):
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

    unreachable_count = 0

    # Initialize graphing if graph=True
    if graph:
        import matplotlib.pyplot as plt  # Import Matplotlib for graphing
        from collections import deque  # Import deque for efficient sliding window
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots()
        ping_values = deque(maxlen=100)  # Store up to 100 pings
        line, = ax.plot([], [], label="Ping (ms)")
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1000)  # Adjust as needed for expected ping range
        ax.set_xlabel("Ping Count")
        ax.set_ylabel("Ping (ms)")
        ax.legend()

    if export:
        import csv
        import os  # Import os to check if the file exists
        from datetime import datetime  # Import datetime for timestamping

        logs_dir = "Logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Sanitize the URL for use in the filename
        sanitized_url = url.replace("://", "_").replace("/", "_").replace(":", "_")
        csv_file_path = os.path.join(logs_dir, f"ping_results_{sanitized_url}_{timestamp}.csv")

        csv_file = open(csv_file_path, mode="w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Ping (ms)", "Mean (ms)", "Variance", "Std Dev (ms)"])
        csv_file.flush() # Ensure the header is written immediately

    try:
        print("ping: ", url)
        # Read the calculated results from subproc_calc
        while True:
            result = calc_process.stdout.readline().strip()
            if result == "Unreachable":
                print("The site is unreachable.")
                unreachable_count += 1
                if unreachable_count >= 6:  # Stop after 6 unsuccessful attempts
                    print("The site is still unreachable after 6 attempts. Stopping the process.")
                    ping_process.terminate()
                    calc_process.terminate()
                    break
            elif result == "Error":
                print("Error in requests.exceptions.RequestException")
                unreachable_count = 0
            else:
                result = split_string_to_tuple(result)  # Convert the string to a tuple
                print(f"ping: {result[0]:.2f} ms, mean: {result[1]:.2f} ms, std_dev: {result[3]:.2f} ms, (variance: {result[2]:.2f})")
                
                # Update graph if graph=True
                if graph:
                    ping_values.append(result[0])  # Append the latest ping value
                    line.set_data(range(len(ping_values)), list(ping_values))
                    ax.set_xlim(0, max(100, len(ping_values)))
                    ax.set_ylim(0, max(1000, max(ping_values) + 50))  # Adjust Y-axis dynamically
                    plt.gcf().canvas.manager.set_window_title(f"{url}   ping: {result[0]:.2f} ms, mean: {result[1]:.2f} ms, std_dev: {result[3]:.2f} ms, (variance: {result[2]:.2f})")
                    plt.pause(0.1)  # Pause to update the graph
                
                # Export results to CSV if export=True
                if export:
                    csv_writer.writerow(result)
                    csv_file.flush() # Ensure data is written to the file

    except KeyboardInterrupt:
        print("Stopping processes.")
        ping_process.terminate()
        calc_process.terminate()
        if graph:
            plt.close()  # Close the graph window
        if export:
            csv_file.close()

if __name__ == "__main__":
    # Default URL if no argument is provided
    remote_address = "https://github.com"
    graph = False
    export = False

    # Parse command-line arguments
    for arg in sys.argv[1:]:
        if arg.startswith("graph="):
            graph = arg.split("=")[1].lower() == "true"
        if arg.startswith("export="):
            export = arg.split("=")[1].lower() == "true"
        else:
            # Ensure the argument is not an option before using it as a URL
            if not arg.startswith("graph=") and not arg.startswith("export="):
                remote_address = arg
                if is_valid_ip(remote_address):
                    print(f"The IP address {remote_address} is valid.")
                    # Add "http://" in front of the IP address if no scheme is present
                    remote_address = f"http://{remote_address}"
                else:
                    print(f"The URL {remote_address} will be used.")

    print(f"Using address: {remote_address}")
    print(f"Graph mode: {'enabled' if graph else 'disabled'}")
    print(f"Export mode: {'enabled' if export else 'disabled'}")

    interact_with_slaves(remote_address, graph, export)