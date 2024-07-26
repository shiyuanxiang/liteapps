import random
import os
import subprocess
import sys
import argparse


def run(package_name, events, inteval):
    fid = 0
    while True:
        fid = random.randint(1, 1000)
        if not os.path.exists(f"{fid}"):
            with open(f"{fid}", "w") as f:
                f.write("")
            break

    monkey_command = f"python monkey.py {package_name} {events} --fid {fid}"
    print(f"Running: {monkey_command}")
    subprocess.Popen(
        monkey_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    get_rtinfo_command = f"python get_rtinfo.py {package_name} {inteval} --fid {fid}"
    print(f"Running: {get_rtinfo_command}")
    subprocess.Popen(
        get_rtinfo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def main():
    parser = argparse.ArgumentParser(
        description="Run Android Monkey test on a specific package with runtime information collection."
    )
    parser.add_argument(
        "-p",
        "--package_name",
        default="com.android.chrome",
        help="The name of the package to test.",
    )
    parser.add_argument(
        "-e",
        "--events",
        type=int,
        default=1000,
        help="The number of events to send to the package.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=5,
        help="The interval (in seconds) to collect info.",
    )

    args = parser.parse_args()
    package_name = args.package_name
    events = args.events
    interval = args.interval

    run(package_name, events, interval)


if __name__ == "__main__":
    main()
