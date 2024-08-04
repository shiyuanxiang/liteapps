class TopicAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.ids = {"add": [], "remove": []}
        self.remove_ids = []
        self.methods_count = {"add": 0, "remove": 0}
        self.topic_count_add = [0] * 10
        self.topic_count_remove = [0] * 10

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

    def load_ids(self, type):
        with open(type + "_ids.txt", "r") as fr:
            self.ids[type] = [int(line.strip()) for line in fr.readlines()]
        print(f"{type}_ids.txt loaded")

    def count(self):
        self.load_ids(type="add")
        self.load_ids(type="remove")
        with open(self.csv_path, "r") as fr:
            lines = fr.readlines()[1:]
            add_amount = len(self.ids["add"])
            remove_amount = len(self.ids["remove"])
            for cnt, idx in enumerate(self.ids["add"]):
                topic = int(lines[idx].split(":")[0])
                self.topic_count_add[topic] += 1
                print(
                    f"[count add] {cnt/add_amount*100:.2f}, {cnt}/{add_amount}",
                    end="\r",
                )

            for cnt, idx in enumerate(self.ids["remove"]):
                top = lines[idx].split(":")
                topic = int(top[0])
                # topic = int(lines[idx].split(":")[0])
                self.topic_count_remove[topic] += 1
                print(
                    f"[count remove] {cnt/remove_amount*100:.2f}, {cnt}/{remove_amount}",
                    end="\n",
                )

    def count_output(self):
        with open("./topic_count.txt", "w") as fw:
            fw.write(f"['+'] topic count\n")
            add_amount = len(self.ids["add"])
            remove_amount = len(self.ids["remove"])
            for topic, count in enumerate(self.topic_count_add):
                fw.write(
                    f"{self.topic2name[topic]:<32}: {count:<8}, {count/add_amount*100:.2f}\n"
                )
            fw.write(f"['-'] topic count\n")
            for topic, count in enumerate(self.topic_count_remove):
                fw.write(
                    f"{self.topic2name[topic]:<32}: {count:<8}, {count/remove_amount*100:.2f}\n"
                )

    def run(self):
        self.count()
        self.count_output()


if __name__ == "__main__":
    ta = TopicAnalyzer(csv_path="./topic_assign_refined.csv")
    ta.run()
