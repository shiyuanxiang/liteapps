import os


def get_manifest_files():
    root_dir = os.getenv("LITEAPPS_ROOT")
    decompiled_dir = os.path.join(root_dir, "static_analyze/decompiled")
    for root, dirs, files in os.walk(decompiled_dir):
        for _dir in dirs:
            manifest_fp = os.path.join(root, _dir, "AndroidManifest.xml")
            if os.path.exists(manifest_fp):
                manifest_new_fp = os.path.join("./manifest/", f"{_dir}.xml")
                os.rename(manifest_fp, manifest_new_fp)
                print(f"[extracted] {manifest_new_fp}")
        break


def main():
    get_manifest_files()


if __name__ == "__main__":
    main()
