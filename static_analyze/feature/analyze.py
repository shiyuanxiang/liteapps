class TopicAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.add_ids = []
        self.methods_count = {"add": 0, "remove": 0}
        topic_0 = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        self.topic_count = {
            "add": topic_0,
            "remove": topic_0,
        }
        self.topic2name = {
            0: "Media and Ad Handling",
            1: "UI Elements and Graphics",
            2: "Media and Adapters",
            3: "User Interface Components",
            4: "Initialization and Setup",
            5: "Ads and Parcelization",
            6: "Audio and Media Handling",
            7: "Icon and Ad Management",
            8: "Media Sessions and Receivers",
            9: "Event Handling in Media and Ads",
        }

    def load_add_ids(self):
        with open("./add_ids.txt", "r") as fr:
            self.add_ids = [int(line.strip()) for line in fr.readlines()]
            self.methods_count["add"] = len(self.add_ids)

    def count(self):
        with open(self.csv_path, "r") as fr:
            lines = fr.readlines()[1:1000000]
            amout = len(lines)
            self.methods_count["remove"] = amout - self.methods_count["add"]
            for cnt, line in enumerate(lines):
                topic = int(lines[cnt].split(":")[0])
                if cnt in self.add_ids:
                    self.topic_count["add"][topic] += 1
                else:
                    self.topic_count["remove"][topic] += 1

                print(f"[count] {cnt/amout*100:.2f}, {cnt}/{amout}", end="\r")

    def output(self):
        # count
        with open("./topic_count.txt", "w") as fw:
            self.topic_count["add"] = dict(sorted(self.topic_count["add"].items()))
            self.topic_count["remove"] = dict(
                sorted(self.topic_count["remove"].items())
            )
            fw.write(f"['+'] topic count\n")
            for topic, count in self.topic_count["add"].items():
                fw.write(
                    f"{self.topic2name[topic]:<32}: {count:<8}, {count/self.methods_count['add']*100:.2f}\n"
                )
            fw.write(f"['-'] topic count\n")
            for topic, count in self.topic_count["remove"].items():
                fw.write(
                    f"{self.topic2name[topic]:<32}: {count:<8}, {count/self.methods_count['remove']*100:.2f}\n"
                )

    def run(self):
        self.load_add_ids()
        self.count()
        self.output()


if __name__ == "__main__":
    ta = TopicAnalyzer(csv_path="./topic_assign_refined.csv")
    ta.run()
