import os


def refine(csv_path, output_path):
    with open(output_path, "w") as fw:
        with open(csv_path, "r") as fr:
            lines = fr.readlines()
            amount = len(lines)
            fw.write("topic: method\n")
            for cnt, line in enumerate(lines[1:]):
                if line.__contains__(":"):
                    line = line.split("=")[1].replace('"', "")
                if line.__contains__(","):
                    depart_loc = line.find(",")
                    topic = line[:depart_loc].strip()
                    method = line[depart_loc + 2 :].strip()
                    fw.write(f"{topic}:{method}\n")
                    print(f"{cnt/amount*100:.2f}%,  {cnt}/{amount}", end="\r")


def check(path):
    with open(path, "r") as fr:
        for line in fr.readlines():
            if line.count(":") > 1:
                print(f"Error: {line}")


if __name__ == "__main__":
    csv_path = "./ta_100000.csv"
    output_path = "./ta_100000_refined.csv"
    refine(csv_path, output_path)
    # check(output_path)
