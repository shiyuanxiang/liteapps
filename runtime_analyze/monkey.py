import subprocess
import sys
import argparse
from datetime import datetime
from tools import *


def run_adb_command(command):
    """Run an ADB command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def run_monkey(package_name, events, fid, log_file, **monkey_options):
    """Run the Android Monkey tool on a specific package."""
    options_str = " ".join(
        f"{key} {value}" for key, value in monkey_options.items() if value is not None
    )

    if monkey_options.get("-d"):
        options_str += f" -d {monkey_options['-d']}"

    command = f"adb shell monkey -p {package_name} {options_str} -v {events}"

    with open(log_file, "w") as f:
        process = subprocess.Popen(
            command, shell=True, stdout=f, stderr=subprocess.STDOUT
        )
        process.communicate()
        write_fid(fid)


def main():
    parser = argparse.ArgumentParser(
        description="Run Android Monkey test on a specific package with custom options."
    )
    parser.add_argument("package_name", help="The name of the package to test.")
    parser.add_argument(
        "events", type=int, help="The number of events to send to the package."
    )
    parser.add_argument("--fid", type=int, help="status file id.")
    parser.add_argument(
        "--throttle",
        type=int,
        default=None,
        help="Delay between events in milliseconds.",
    )
    parser.add_argument(
        "--pct-touch", type=int, default=None, help="Percentage of touch events."
    )
    parser.add_argument(
        "--pct-motion", type=int, default=None, help="Percentage of motion events."
    )
    parser.add_argument(
        "--pct-trackball",
        type=int,
        default=None,
        help="Percentage of trackball events.",
    )
    parser.add_argument(
        "--pct-syskeys", type=int, default=None, help="Percentage of system key events."
    )
    parser.add_argument(
        "--pct-appswitch",
        type=int,
        default=None,
        help="Percentage of app switch events.",
    )
    parser.add_argument(
        "--pct-anyevent",
        type=int,
        default=None,
        help="Percentage of any other types of events.",
    )
    parser.add_argument(
        "-d", type=int, help="Debug level. Set the debug level for detailed output."
    )

    args = parser.parse_args()
    package_name = args.package_name
    events = args.events
    fid = args.fid
    monkey_options = {
        "--throttle": args.throttle,
        "--pct-touch": args.pct_touch,
        "--pct-motion": args.pct_motion,
        "--pct-trackball": args.pct_trackball,
        "--pct-syskeys": args.pct_syskeys,
        "--pct-appswitch": args.pct_appswitch,
        "--pct-anyevent": args.pct_anyevent,
        "-d": args.d,
    }

    start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{package_name}_{fid}_{start_time}.mklog"
    run_monkey(package_name, events, fid, log_file, **monkey_options)


if __name__ == "__main__":
    main()
