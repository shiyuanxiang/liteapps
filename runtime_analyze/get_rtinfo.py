import subprocess
import time
import sys
import argparse
from datetime import datetime
from tools import *
import os


def run_adb_command(command):
    """Run an ADB command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def collect_runtime_info(package_name, fid, interval=5, log_file=None):
    with open(log_file, "w") as f:
        while True:
            if read_fid(fid) is True:
                os.remove(f"{fid}")
                return
            # Collect CPU info
            cpu_info = run_adb_command(
                f"adb shell dumpsys cpuinfo | grep {package_name}"
            )
            f.write("CPU Info:\n")
            f.write(cpu_info + "\n")

            # Collect Memory info
            mem_info = run_adb_command(
                f'adb shell dumpsys meminfo {package_name} | grep -A 14 "App Summary"'
            )
            f.write("Memory Info:\n")
            f.write(mem_info + "\n")

            # Get process information
            ps_info = run_adb_command(f"adb shell ps | grep {package_name}")
            f.write("Process Info:\n")
            f.write(ps_info + "\n")

            # Extract PID from the ps_info
            pid = ps_info.split()[1] if ps_info else None

            if pid:
                # Collect top info for the process
                top_info = run_adb_command(f"adb shell top -n 1 | grep {pid}")
                f.write("Top Info:\n")
                f.write(top_info + "\n")

                # Collect logcat info for the process
                logcat_info = run_adb_command(f'adb logcat -d | grep "pid {pid}"')
                f.write("Logcat Info:\n")
                f.write(logcat_info + "\n")

                # Kill the process with SIGQUIT (signal 3)
                kill_result = run_adb_command(f"adb shell kill -3 {pid}")
                f.write("Kill Result:\n")
                f.write(kill_result + "\n")

            f.write("=" * 50 + "\n")
            f.flush()
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Collect runtime information for a specific package at regular intervals."
    )
    parser.add_argument("package_name", help="The name of the package to monitor.")
    parser.add_argument(
        "interval", type=int, help="The interval (in seconds) to collect info."
    )
    parser.add_argument("--fid", type=int, help="status file id.")
    args = parser.parse_args()
    package_name = args.package_name
    interval = args.interval
    fid = args.fid
    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{package_name}_{fid}_{interval}s_{start_time}.rtlog"
    collect_runtime_info(package_name, fid, interval, log_file)


if __name__ == "__main__":
    main()
