import getopt
import os
import sys

import hiyapyco
import zipfile

args = {}


def get_args():
    args["cwd"] = os.getcwd()
    args["extract"] = False

    full_args = sys.argv
    arg_list = full_args[1:]
    short_opts = "chf:j:eo:"
    long_opts = ["cwd", "help", "files=", "jar-files=", "extract" "out-dir="]

    arguments, values = getopt.getopt(arg_list, short_opts, long_opts)

    for current_arg, current_value in arguments:
        if current_arg in ("-h", "--help"):
            print("usage: application-effective-yaml.py [-h] [-f FILE_LIST] [-j FILES_IN_JAR_LIST] [-e] [-o DIRECTORY]")
            print
            print("Merges multiple yaml files to get the effective content")
            print
            print("arguments:")
            print("  -c DIRECTORY, --cwd DIRECTORY")
            print("                        current working directory")
            print("  -h, --help            show this help message end exit")
            print("  -f FILE_LIST, --files FILE_LIST")
            print("                        comma separated list of yaml files. order matters!")
            print("  -j FILE_IN_JAR_LIST, --jar-files FILES_IN_JAR_LIST")
            print("                        comma separated list of yaml files specified in a jar (e.g test.jar:application.yml). order matters!")
            print("  -e, --extract         extracts the files specified in -j argument")
            print("  -o DIRECTORY, --out-dir DIRECTORY")
            print("                        output directory to extract the files in (default=cwd)")
            print
            print("examples:")
            print
            print("# get content of two merged yamls")
            print("application-effective-yaml.py -f test1.yml,test2.yml")
            print
            print("# get content of two files in a jar")
            print("application-effective-yaml.py -j ./test.jar:application.yml,./test.jar:application-test.yml")
            print
            print("# get content of a file in a jar and local file and extract the file from jar")
            print("application-effective-yaml.py -j ./test.jar:application.yml -f ./test1.yml -e")
            print
            print("# extract a file from a jar to the sub directory test")
            print("application-effective-yaml.py -j ./test.jar:application.yml -e -o ./test/")
            print
            exit(0)
        elif current_arg in ("-f", "--files"):
            args["files"] = current_value.split(",")
        elif current_arg in ("-j", "--jar-files"):
            args["jar-files"] = current_value.split(",")
        elif current_arg in ("-e", "--extract"):
            args["extract"] = True
        elif current_arg in ("-o", "--out-dir"):
            args["out"] = current_value

    if "out" not in args:
        args["out"] = args["cwd"]

    return args


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def read_file_in_jar(jar_file, name):
    file_content = ""
    with zipfile.ZipFile(jar_file, 'r') as jarzip:
        try:
            lst = jarzip.infolist()
            for zi in lst:
                fn = zi.filename
                if fn.endswith(name):
                    with jarzip.open(fn) as jarzipfile:
                        file_content = jarzipfile.read()
                        if args["extract"]:
                            with open(os.path.join(args["out"], name), "wb") as of:
                                of.write(file_content)

        finally:
            jarzip.close()

    return file_content


def merge_yamls(file_contens):
    merged_yaml = hiyapyco.load(file_contens)
    return hiyapyco.dump(merged_yaml)


def main():
    global args
    args = get_args()
    yaml_contents = []

    if "jar-files" in args:
        for f in args["jar-files"]:
            jar_file_split = f.split(':')
            jar_file = os.path.join(args["cwd"], jar_file_split[0])
            yaml_contents.append(read_file_in_jar(jar_file, jar_file_split[1]))

    if "files" in args:
        for f in args["files"]:
            file_path = os.path.join(args["cwd"], f)
            yaml_contents.append(read_file(file_path))

    if len(yaml_contents) > 0:
        print(merge_yamls(yaml_contents))
    else:
        print("No content found or specified")
        exit(1)


if __name__ == "__main__":
    main()
