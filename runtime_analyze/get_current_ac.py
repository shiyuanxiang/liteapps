# run adb shell dumpsys activity top | grep ACTIVITY
import subprocess


def get_current_ac():
    result = subprocess.run(
        "adb shell dumpsys activity top | grep ACTIVITY",
        shell=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main():
    print(get_current_ac())


if __name__ == "__main__":
    main()
