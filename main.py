import getopt
import os
import sys

import hiyapyco

args = {}


def get_args():
    args["cwd"] = os.getcwd()

    full_args = sys.argv
    arg_list = full_args[1:]
    short_opts = "hf:"
    long_opts = ["help", "files="]

    arguments, values = getopt.getopt(arg_list, short_opts, long_opts)

    for current_arg, current_value in arguments:
        if current_arg in ("-h", "--help"):
            print("Help...")
            exit(2)
        elif current_arg in ("-f", "--files"):
            args["files"] = current_value.split(",")

    return args


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def merge_yamls(fileContens):
    merged_yaml = hiyapyco.load(fileContens)
    return hiyapyco.dump(merged_yaml)


def main():
    args = get_args()
    yaml_contents = []

    for f in args["files"]:
        file_path = os.path.join(args["cwd"], f)
        yaml_contents.append(read_file(file_path))

    print(yaml_contents)
    # print(merge_yamls([
    #     read_file('./__test__/test1.yml'),
    #     read_file('./__test__/test2.yml')
    # ]))


if __name__ == "__main__":
    main()
