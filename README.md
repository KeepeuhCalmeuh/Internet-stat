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
- `matplotlib` library (install using `pip install matplotlib`)

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
3. To enable graph mode, add the argument `graph=true`:
   ```bash
   python main.py https://example.com graph=true
   ```
4. Press `Ctrl+C` to stop the script.

## Example Output

```
No address provided. Using the default URL: https://github.com
ping:  https://github.com
Graph mode: disabled
ping: 72.34 ms, mean: 72.34 ms, std_dev: 0.00 ms, (variance: 0.00)
ping: 57.77 ms, mean: 65.05 ms, std_dev: 10.30 ms, (variance: 106.10)
ping: 58.99 ms, mean: 63.03 ms, std_dev: 8.08 ms, (variance: 65.32)
ping: 335.90 ms, mean: 131.25 ms, std_dev: 136.59 ms, (variance: 18657.56)
ping: 67.98 ms, mean: 118.59 ms, std_dev: 121.63 ms, (variance: 14793.77)
```
![Illustration_Graph](Illustration_Graph.png)

## Notes

- The `subproc_calc.py` script maintains a sliding window of the last 10 response times for statistical calculations.
- Negative response times indicate errors:
  - `-1`: not good response.status_code.
  - `-2`: unreachable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
