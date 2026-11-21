"""SystemPulse: a small, read-only system monitoring dashboard."""
from datetime import datetime, timezone
import platform
import socket
import time

import psutil
from flask import Flask, jsonify, render_template

app = Flask(__name__)
BOOT_TIME = psutil.boot_time()


def system_stats():
    memory = psutil.virtual_memory()
    partitions = psutil.disk_partitions()
    if platform.system() == "Windows":
        disk_path = next((p.mountpoint for p in partitions if p.fstype), "C:\\")
    else:
        disk_path = "/"
    disk = psutil.disk_usage(disk_path)
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": memory.percent,
        "memory_used": memory.used,
        "memory_total": memory.total,
        "disk_percent": disk.percent,
        "disk_used": disk.used,
        "disk_total": disk.total,
        "uptime_seconds": max(0, int(time.time() - BOOT_TIME)),
        "hostname": socket.gethostname(),
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": psutil.cpu_count(logical=True) or 0,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def process_list():
    items = []
    for proc in psutil.process_iter(["pid", "name", "status", "memory_percent"]):
        try:
            info = proc.info
            items.append({
                "pid": info.get("pid"),
                "name": info.get("name") or "Unknown",
                "status": info.get("status") or "unknown",
                "cpu_percent": proc.cpu_percent(interval=None),
                "memory_percent": round(info.get("memory_percent") or 0, 2),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(items, key=lambda item: item["cpu_percent"], reverse=True)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/system")
def api_system():
    return jsonify(system_stats())


@app.get("/api/processes")
def api_processes():
    return jsonify(process_list())


@app.get("/api/performance")
def api_performance():
    memory = psutil.virtual_memory()
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": memory.percent,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    # Local-only by default: do not expose system information to the network.
    app.run(host="127.0.0.1", port=5000, debug=False)
