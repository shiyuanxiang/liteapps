def read_fid(fid):
    with open(str(fid), "r") as f:
        if f.read().strip() == "":
            return False
        else:
            return True


def write_fid(fid):
    with open(str(fid), "w") as f:
        f.write("1")
