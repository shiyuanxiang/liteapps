import os


def refine(csv_path, output_path):
    with open(output_path, "w") as fw:
        with open(csv_path, "r") as fr:
            lines = fr.readlines()
            amount = len(lines)
            fw.write("topic: method\n")
            x = 0
            for cnt, line in enumerate(lines[1:]):
                if cnt % 2 == 0 and "," in line:
                    x += 1
                    depart_loc = line.find(",")
                    topic = line[:depart_loc].strip()
                    method = line[depart_loc + 2 :].strip()
                    if method.__contains__("="):
                        method = method.replace('"', "")
                        method = method.split("=")[-1]
                    fw.write(f"{topic}:{method}\n")

            print(f"total: {x}")


def check(path):
    with open(path, "r") as fr:
        for line in fr.readlines():
            if line.count(":") > 1:
                print(f"Error: {line}")


if __name__ == "__main__":
    csv_path = "./topic_assign.csv"
    output_path = "./topic_assign_refined.csv"
    refine(csv_path, output_path)
    check(output_path)
