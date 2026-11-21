# SystemPulse

A small, cross-platform system monitoring dashboard built with Python, Flask, psutil and Chart.js. View CPU, memory and disk usage alongside a searchable list of running processes.

## Features

- Live CPU, RAM and disk utilization
- Running process list with PID, status, CPU and memory usage
- Search processes by name or PID
- Live CPU and memory history chart
- Basic system details and uptime
- Read-only monitoring; no process termination or service changes
- Designed for Windows, Ubuntu/Linux and macOS

## Requirements

- Python 3.9 or newer
- pip
- Internet connection to load the Chart.js and Google Fonts CDN assets (monitoring APIs run locally)

## Run on Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks virtual-environment activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe app.py` instead.

## Run on Ubuntu / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Ubuntu, install the venv package first if needed: `sudo apt install python3-venv`.

## Run on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. Stop the server with `Ctrl+C`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/system` | CPU, memory, disk and system details |
| GET | `/api/processes` | Current process list |
| GET | `/api/performance` | Current CPU and memory readings |

## Notes

- The application binds to `127.0.0.1` and is intended for local use.
- Some process details may be unavailable due to operating-system permissions. Run without administrator/root privileges unless you have a specific reason to do otherwise.
- Disk usage is reported for the root filesystem on Linux/macOS and the first detected partition on Windows.
- Chart.js and Google Fonts are loaded from public CDNs. The page and monitoring API run locally.

## License

MIT. See [LICENSE](LICENSE).
