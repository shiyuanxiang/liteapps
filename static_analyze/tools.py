import os
import pandas as pd


def get_files_from_dir(dir_path):
    """
    return: len(files), files
    """
    files = []
    for root, dirs, fs in os.walk(dir_path):
        for f in fs:
            files.append(os.path.join(root, f))
    return len(files), files


def id2app_name(apk_ids):
    root_dir = os.getenv("LITEAPPS_ROOT")
    apk_fp = os.path.join(root_dir, "apks/apks.csv")
    df = pd.read_csv(apk_fp)
    name_dict = dict(zip(df["apk_id"], df["app_name"]))
    return [name_dict[apk_id] for apk_id in apk_ids]
