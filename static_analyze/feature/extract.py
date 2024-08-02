import os


def extract_step1():
    root_dir = os.getenv("LITEAPPS_ROOT")
    diffuse_dir = os.path.join(root_dir, "static_analyze/diffuse/diffuse_dir")
    for root, dirs, files in os.walk(diffuse_dir):
        for cur, file in enumerate(files):
            start_line = 0
            end_line = 0
            with open(os.path.join(root, file), "r") as fr:
                lines = fr.readlines()
                for cnt, line in enumerate(lines):
                    if line.startswith("METHODS:"):
                        start_line = cnt
                    elif line.startswith("FIELDS:"):
                        end_line = cnt
                        break
                with open(os.path.join("./methods", file), "w") as fw:
                    fw.writelines(lines[start_line + 2 : end_line])
            print(f"[progress] {cur+1}/{len(files)}")


def write2txt(_dict, fpt):
    for key, val in _dict.items():
        for v in val:
            fpt.write(f"{v}\n")


def extract_step2():
    # new is lite
    _all = {}
    add = {}
    remove = {}
    for root, dirs, files in os.walk("./methods"):
        for cur, file in enumerate(files):
            _all[file] = []
            add[file] = []
            remove[file] = []
            with open(os.path.join(root, file), "r") as fr:
                lines = fr.readlines()
                for line in lines:
                    if line.count(".") > 3:
                        m = line.strip()[2:]
                        _all[file].append(m)
                        if line.startswith("  +"):
                            add[file].append(m)
                        else:
                            remove[file].append(m)

            print(f"[progress] {cur+1}/{len(files)}")

    with open("./all.txt", "w") as fw:
        write2txt(_all, fw)
    with open("./add.txt", "w") as fw:
        write2txt(add, fw)
    with open("./remove.txt", "w") as fw:
        write2txt(remove, fw)


def main():
    extract_step2()


if __name__ == "__main__":
    main()
