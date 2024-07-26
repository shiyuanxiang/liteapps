import os
import subprocess


def get_permission(apk_path):
    cmd = "aapt dump permissions " + apk_path
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    permission_list = result.stdout.decode("utf-8").splitlines()
    return permission_list


def write_permission_to_log(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".apk") or file.endswith(".xapk"):
                print(f"[extract permisssion] {file}")
                apk_path = os.path.join(root, file)
                perm_path = (
                    os.path.join("./extracted_permission", file.split(".")[0]) + ".perm"
                )
                permission_list = get_permission(apk_path)
                with open(perm_path, "w") as f:
                    for permission in permission_list:
                        f.write(permission + "\n")


def main():
    root_dir = os.getenv("LITEAPPS_ROOT")
    apks_dir = os.path.join(root_dir, "apks/apks")
    write_permission_to_log(apks_dir)


if __name__ == "__main__":
    main()
