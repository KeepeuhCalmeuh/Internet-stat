# Internet Statistics

This project is a Python-based tool for monitoring and analyzing the response times of a website. It consists of three main scripts that work together to measure response times, calculate statistical metrics, and display the results in real-time.

## Features

- **Ping a website**: Measure the response time of a given URL.
- **Statistical analysis**: Calculate the mean, variance, and standard deviation of the response times.
- **Real-time updates**: Continuously display the latest statistics in the console.

## Project Structure

- `main.py`: The main script that orchestrates the interaction between the other scripts.
- `subproc_ping.py`: A subprocess that pings the given URL and outputs the response time.
- `subproc_calc.py`: A subprocess that calculates statistical metrics based on the response times received from `subproc_ping.py`.

## How It Works

1. `main.py` starts two subprocesses:
   - `subproc_ping.py` to measure response times.
   - `subproc_calc.py` to calculate statistics.
2. The response times from `subproc_ping.py` are piped into `subproc_calc.py`.
3. `subproc_calc.py` computes the mean, variance, and standard deviation of the response times and sends the results back to `main.py`.
4. `main.py` displays the results in real-time.

## Prerequisites

- Python 3.6 or higher
- `requests` library (install using `pip install requests`)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/KeepeuhCalmeuh/Internet-stat.git
   ```
2. Navigate to the project directory:
   ```bash
   cd internet-stat
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```
2. By default, the script pings `https://github.com`. To specify a different URL, pass it as an argument:
   ```bash
   python main.py https://example.com
   ```
3. Press `Ctrl+C` to stop the script.

## Example Output

```
ping : 0.23, mean : 0.25, variance : 0.01, std_dev : 0.10
ping : 0.24, mean : 0.24, variance : 0.00, std_dev : 0.07
ping : 0.22, mean : 0.23, variance : 0.01, std_dev : 0.08
```

## Notes

- The `subproc_calc.py` script maintains a sliding window of the last 10 response times for statistical calculations.
- Negative response times indicate errors:
  - `-1`: Site is inaccessible.
  - `-2`: An exception occurred during the request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
