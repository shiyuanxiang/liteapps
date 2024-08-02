import os


class PermissionAnalyzer:
    def __init__(self, permission_dir, report_file):
        self.permission_dir = permission_dir
        self.report_file = report_file
        self.permission_files = []
        self.get_permission_files()
        self.reportt_list = {}
        self.permission_count_lite = {}
        self.permission_count_full = {}
        self.dangerous_permission_count = {}
        self.dangerous_permission_list = []
        self.dangerous_permission_introduced = {}

    def get_permission_files(self):
        for root, dirs, files in os.walk(self.permission_dir):
            for file in files:
                if file.endswith(".perm"):
                    self.permission_files.append(os.path.join(root, file))

    def run(self):
        with open("dangerous_permissions", "r") as f:
            self.dangerous_permission_list = [
                line.strip().lower() for line in f.readlines()
            ]
        for d_p in self.dangerous_permission_list:
            self.dangerous_permission_count[d_p] = []

        for permission_file in self.permission_files:
            self.analyze(permission_file)
        self.output()

    def analyze(self, permission_fp):
        permission_list = []

        with open(permission_fp, "r") as f:
            for line in f.readlines():
                if line.__contains__("permission"):
                    if line.__contains__("name="):
                        permission_list.append(line.split("'")[1].strip().lower())
                    else:
                        permission_list.append(line.split(":")[1].strip().lower())
        dangerous_cnt = 0
        apk_id = int(os.path.basename(permission_fp).split(".")[0])
        for perm in permission_list:
            for d_p in self.dangerous_permission_list:
                if d_p in perm:
                    if apk_id not in self.dangerous_permission_count[d_p]:
                        self.dangerous_permission_count[d_p].append(apk_id)
                    dangerous_cnt += 1

            if apk_id % 2 == 1:
                if perm in self.permission_count_full:
                    self.permission_count_full[perm] += 1
                else:
                    self.permission_count_full[perm] = 1
            else:
                if perm in self.permission_count_lite:
                    self.permission_count_lite[perm] += 1
                else:
                    self.permission_count_lite[perm] = 1

        self.reportt_list[apk_id] = [dangerous_cnt, len(permission_list)]

    def dangerous_permission_introduced_by_lite(self):
        """
        instroduced means permission in lite but not in full.
        """
        # dp--> lite apk_ids
        for d_p, apk_ids in self.dangerous_permission_count.items():
            for apk_id in apk_ids:
                if apk_id % 2 == 0 and apk_id - 1 not in apk_ids:
                    if d_p in self.dangerous_permission_introduced:
                        self.dangerous_permission_introduced[d_p].append(apk_id)
                    else:
                        self.dangerous_permission_introduced[d_p] = [apk_id]
        self.dangerous_permission_introduced = dict(
            sorted(
                self.dangerous_permission_introduced.items(),
                key=lambda item: len(item[1]),
                reverse=True,
            )
        )
        with open(self.report_file, "a") as fw:
            fw.write(
                "\n\n[dangerous permissions introduced by lite, those appare in lite but not in full]\n"
            )
            for d_p, apk_ids in self.dangerous_permission_introduced.items():
                fw.write(f"{d_p:<35}: {len(apk_ids)}   ")
                apk_ids = sorted(apk_ids)
                for apk_id in apk_ids:
                    fw.write(f"{apk_id} ")
                fw.write("\n")

        lite2intro_cnt = {}  # lite apk_id --> introduced count
        for d_p, apk_ids in self.dangerous_permission_introduced.items():
            for apk_id in apk_ids:
                if apk_id in lite2intro_cnt:
                    lite2intro_cnt[apk_id] += 1
                else:
                    lite2intro_cnt[apk_id] = 1
        lite2intro_cnt = dict(
            sorted(lite2intro_cnt.items(), key=lambda item: item[1], reverse=True)
        )
        with open(self.report_file, "a") as fw:
            fw.write(
                "\n\n[how many dangerous permissions the lites introduced, top10, new_d_p/total_d_p]\n"
            )
            for apk_id, count in list(lite2intro_cnt.items())[:10]:
                fw.write(
                    f"{apk_id:<5}: {count}/{self.reportt_list[apk_id][0]:<5}  {count/self.reportt_list[apk_id][0]:.2f}\n"
                )

    def output(self):
        self.reportt_list = dict(
            sorted(self.reportt_list.items(), key=lambda item: item[0])
        )
        abnormal_list = []
        with open(self.report_file, "w") as f:
            f.write("[apk_id: dangerous/total permission count]\n")
            for apk_id, msg in self.reportt_list.items():
                f.write(f"{apk_id:<5}: {msg[0]}/{msg[1]}\n")
                if (
                    apk_id % 2 == 1
                    and (apk_id + 1) in self.reportt_list
                    and self.reportt_list[apk_id][0] < self.reportt_list[apk_id + 1][0]
                ):
                    abnormal_list.append(
                        f"{apk_id}-{apk_id+1}: {self.reportt_list[apk_id][0]}, {self.reportt_list[apk_id+1][0]}"
                    )
            f.write(f"\n[abnormal count]: {len(abnormal_list)}\n")
            for abnormal in abnormal_list:
                f.write(f"{abnormal}\n")

            f.write("\n\n[permission count lite] top 10\n")
            permission_count_lite = dict(
                sorted(
                    self.permission_count_lite.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            for permission, count in list(permission_count_lite.items())[:10]:
                f.write(f"{permission:<20}: {count}\n")

            f.write("\n\n[permission count full] top 10\n")
            permission_count_full = dict(
                sorted(
                    self.permission_count_full.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            for permission, count in list(permission_count_full.items())[:10]:
                f.write(f"{permission:<20}: {count}\n")

            f.write("\n\n[dangerous permission count]\n")
            self.dangerous_permission_count = dict(
                sorted(
                    self.dangerous_permission_count.items(),
                    key=lambda item: len(item[1]),
                    reverse=True,
                )
            )
            for d_p, _list in self.dangerous_permission_count.items():
                f.write(f"{d_p:<35}: {len(_list)}   ")
                _list = sorted(_list)
                for apk_id in _list:
                    f.write(f"{apk_id} ")
                f.write("\n")

        self.dangerous_permission_introduced_by_lite()


def main():
    permission_analyzer = PermissionAnalyzer(
        "extracted_permission", "analyzed_permission"
    )
    permission_analyzer.run()


if __name__ == "__main__":
    main()
