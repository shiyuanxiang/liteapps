import os
import sys
import argparse
import subprocess
import pandas as pd


def parse_apk(apk_path, apk_id):
    print("parsing " + apk_path)
    res_dir = "./decompiled/" + apk_id
    env_dir = "./env"

    cmd = "java -jar " + env_dir + "/apktool.jar d " + apk_path + " -o " + res_dir
    subprocess.call(cmd, shell=True)
    print("[apktool] success")

    cmd = "unzip -o " + apk_path + " -d " + "tmp_dir"
    subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL)
    print("[unzip] success")

    jar_path = "./jar/" + apk_id + "_output.jar"
    cmd = (
        "sh "
        + env_dir
        + "/dex-tools-v2.4/d2j-dex2jar.sh tmp_dir/classes.dex -o "
        + jar_path
    )
    subprocess.call(cmd, shell=True)
    print("[dex2jar] success")

    cmd = "rm -rf tmp_dir " + res_dir + "/smali* " + res_dir + "/lib"
    subprocess.call(cmd, shell=True)
    print("[clean] success")


def main():
    df = pd.read_csv("../apks/apks.csv")
    for idx, row in df.iterrows():
        if df.at[idx, "decompiled"] == "true":
            continue
        apk_id = row["apk_id"]
        apk_path = os.path.join("../apks/apks/", row["apk_name"])
        parse_apk(apk_path, str(apk_id))
        df.at[idx, "decompiled"] = "true"
    df.to_csv("../apks/apks.csv", index=False)
    print("[decompile] success")


if __name__ == "__main__":
    main()
