import os
import re


class Comparator:
    def __init__(self, dp):
        self.fps = [
            os.path.join(dp, "value"),
            os.path.join(dp, "drawable"),
            os.path.join(dp, "layout"),
        ]

    def run(self):
        for fp in self.fps:
            with open(fp, "r") as f:
                _dict = self.get_dict(f)
                self.compare(_dict, fp)

    def add_to_all(self, _all, attr):
        if _all == None:
            _all = attr
        else:
            for key, val in attr.items():
                if key in _all:
                    _all[key] += val
                else:
                    _all[key] = val
        return _all

    def compare(self, _dict, fp):
        output_fp = fp + "_compared"
        all_lite = None
        all_full = None
        abnormal_count = {}
        abnormal_pairs = 0
        with open(output_fp, "w") as f:
            for apk_id, attr in _dict.items():
                if apk_id % 2 == 1:
                    all_full = self.add_to_all(all_full, attr)

                    if apk_id + 1 in _dict:
                        f.write(f"[pair]: {apk_id}-{apk_id + 1}\n")
                        if_abnormal = False
                        for key, val in attr.items():
                            if key in _dict[apk_id + 1]:
                                if val < _dict[apk_id + 1][key]:
                                    if_abnormal = True
                                    f.write(
                                        f"-- {key}: {val} < {_dict[apk_id + 1][key]}\n"
                                    )
                                    if key in abnormal_count:
                                        abnormal_count[key] += 1
                                    else:
                                        abnormal_count[key] = 1
                        if if_abnormal:
                            abnormal_pairs += 1
                else:
                    all_lite = self.add_to_all(all_lite, attr)
            f.write(f"[abnormal_pairs] {abnormal_pairs}\n")
            f.write(f"[all]: lite\n")
            for key, val in all_lite.items():
                f.write(f"-- {key}: {val}\n")
            f.write(f"[all]: full\n")
            for key, val in all_full.items():
                f.write(f"-- {key}: {val}\n")
            abnormal_count = dict(
                sorted(abnormal_count.items(), key=lambda x: x[1], reverse=True)
            )
            f.write(f"[abnormal_count]\n")
            for key, val in abnormal_count.items():
                f.write(f"-- {key}: {val}\n")

    def get_val(self, line):
        return int(float(line.split(":")[1].strip()))

    def get_key_val(self, line):
        match = re.match(r"-- \[(\w+)\] (\w+): (\d+)", line)
        if match:
            key = match.group(1) + "_" + match.group(2)
            val = int(match.group(3))
            return key, val
        else:
            return None, None

    def get_dict(self, f):
        _dict = {}
        apk_id = -1
        for line in f.readlines():
            if line == "\n" or line == "-- [dir_size] nan: nan\n":
                continue
            elif line.__contains__("apk"):
                apk_id = int(line.split(":")[1].split(".")[0])
                _dict[apk_id] = {"dir_size": 0}
            elif line.__contains__("dir_size"):
                _dict[apk_id]["dir_size"] += self.get_val(line)
            else:
                key, val = self.get_key_val(line)
                if key and val:
                    _dict[apk_id][key] = val
        return _dict


def main():
    comparator = Comparator("./analyzed")
    comparator.run()


if __name__ == "__main__":
    main()
