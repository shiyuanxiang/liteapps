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

    def get_permission_files(self):
        for root, dirs, files in os.walk(self.permission_dir):
            for file in files:
                if file.endswith(".perm"):
                    self.permission_files.append(os.path.join(root, file))

    def run(self):
        for permission_file in self.permission_files:
            self.analyze(permission_file)
        self.output()

    def analyze(self, permission_fp):
        dangerous_permission_list = []
        permission_list = []
        with open("dangerous_permissions", "r") as f:
            dangerous_permission_list = [line.strip().lower() for line in f.readlines()]
        with open(permission_fp, "r") as f:
            for line in f.readlines():
                if line.__contains__("permission"):
                    if line.__contains__("name="):
                        permission_list.append(line.split("'")[1].strip().lower())
                    else:
                        permission_list.append(line.split(":")[1].strip().lower())
        dangerous_cnt = 0
        apk_id = int(os.path.basename(permission_fp).split(".")[0])
        for permission in permission_list:
            if any(
                dangerous_permission in permission
                for dangerous_permission in dangerous_permission_list
            ):
                dangerous_cnt += 1

            if apk_id % 2 == 1:
                if permission in self.permission_count_full:
                    self.permission_count_full[permission] += 1
                else:
                    self.permission_count_full[permission] = 1
            else:
                if permission in self.permission_count_lite:
                    self.permission_count_lite[permission] += 1
                else:
                    self.permission_count_lite[permission] = 1

        self.reportt_list[apk_id] = [dangerous_cnt, len(permission_list)]

    def output(self):
        self.reportt_list = dict(
            sorted(self.reportt_list.items(), key=lambda item: item[0])
        )
        abnormal_list = []
        with open(self.report_file, "w") as f:
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


def main():
    permission_analyzer = PermissionAnalyzer(
        "extracted_permission", "analyzed_permission"
    )
    permission_analyzer.run()


if __name__ == "__main__":
    main()
