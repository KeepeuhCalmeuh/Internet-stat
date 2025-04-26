import sys
import statistics

def process_response_times():
    response_times = []

    while True:
        try:
            # Read a line from standard input
            line = sys.stdin.readline().strip()
            if not line:
                continue

            # Convert the line to float
            response_time = float(line)

            # Ignore error codes (-1, -2)
            if response_time < 0:
                continue

            # Add the response time to the list
            if len(response_times) >= 10:
                # Remove the oldest response time if the list exceeds 10 elements
                response_times.pop(0)
                response_times.append(response_time)
            else:
                response_times.append(response_time)
            
            # Perform calculations
            mean = statistics.mean(response_times)
            variance = statistics.variance(response_times) if len(response_times) > 1 else 0
            std_dev = variance ** 0.5

            # Send the results to the main process
            # ping, mean, variance, std_dev
            sys.stdout.write(f"{response_time:.2f},{mean:.2f},{variance:.2f},{std_dev:.2f}\n")
            sys.stdout.flush()

        except ValueError:
            # Ignore invalid lines
            continue

if __name__ == "__main__":
    process_response_times()