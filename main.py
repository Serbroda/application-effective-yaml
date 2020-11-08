import getopt
import os
import sys

import hiyapyco
import zipfile

args = {}


def get_args():
    args["cwd"] = os.getcwd()
    args["extract"] = False
    args["strict-order"] = False
    args["args-passed-direction"] = "UNKNOWN"

    full_args = sys.argv
    arg_list = full_args[1:]
    short_opts = "chf:j:eo:st:"
    long_opts = ["cwd", "help", "files=", "jar-files=", "out=", "extract", "target-dir", "strict-order"]

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
            print("                        comma separated list of yaml files. Order matters!")
            print("  -j FILE_IN_JAR_LIST, --jar-files FILES_IN_JAR_LIST")
            print("                        comma separated list of yaml files specified inside a jar "
                  "(e.g test.jar:application.yml). Order matters!")
            print("  -o FILE, --out FILE   create output file with merged results")
            print("  -e, --extract         extracts the files specified in -j argument")
            print("  -t DIRECTORY, --target-dir DIRECTORY")
            print("                        target directory to extract the files in (default=cwd)")
            print("  -s, --strict-order    by default the jar files will always be taken before the local files. "
                  "If the strict-order is set the files which are passed first will merge first")
            print
            print("examples:")
            print("  # get content of two merged yamls and write to result.yml")
            print("  application-effective-yaml.py -f test1.yml,test2.yml -o result.yml")
            print
            print("  # get content of two files inside a jar")
            print("  application-effective-yaml.py -j ./test.jar:application.yml,./test.jar:application-test.yml")
            print
            print("  # get content of a file inside a jar and local file and extract the file from jar")
            print("  application-effective-yaml.py -j ./test.jar:application.yml -f ./test1.yml -e")
            print
            print("  # extract a file from a jar to the sub directory test")
            print("  application-effective-yaml.py -j ./test.jar:application.yml -e -t ./test/")
            print
            exit(0)
        elif current_arg in ("-f", "--files"):
            args["files"] = current_value.split(",")
            if args["args-passed-direction"] == "UNKNOWN":
                args["args-passed-direction"] = "FILES"
        elif current_arg in ("-j", "--jar-files"):
            args["jar-files"] = current_value.split(",")
            if args["args-passed-direction"] == "UNKNOWN":
                args["args-passed-direction"] = "JARS"
        elif current_arg in ("-o", "--out"):
            args["out"] = current_value
        elif current_arg in ("-e", "--extract"):
            args["extract"] = True
        elif current_arg in ("-t", "--target-dir"):
            args["target"] = current_value
        elif current_arg in ("-s", "--strict-order"):
            args["strict-order"] = True

    if "target" not in args:
        args["target"] = args["cwd"]

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
                            with open(os.path.join(args["target"], name), "wb") as of:
                                of.write(file_content)

        finally:
            jarzip.close()

    return file_content


def merge_yamls(file_contens):
    merged_yaml = hiyapyco.load(file_contens, method=hiyapyco.METHOD_MERGE)
    return hiyapyco.dump(merged_yaml)


def read_jar_contents():
    contents = []
    if "jar-files" in args:
        for f in args["jar-files"]:
            jar_file_split = f.split(':')
            jar_file = os.path.join(args["cwd"], jar_file_split[0])
            contents.append(read_file_in_jar(jar_file, jar_file_split[1]))
    return contents


def read_file_contents():
    contents = []
    if "files" in args:
        for f in args["files"]:
            file_path = os.path.join(args["cwd"], f)
            contents.append(read_file(file_path))
    return contents


def read_all_contents():
    contents = []
    if args["strict-order"] and args["args-passed-direction"] == "FILES":
        contents.append(read_file_contents())
        contents.append(read_jar_contents())
    else:
        contents.append(read_jar_contents())
        contents.append(read_file_contents())
    return contents


def main():
    global args
    args = get_args()
    yaml_contents = read_all_contents()

    if len(yaml_contents) > 0:
        merged_result = merge_yamls(yaml_contents)
        print(merged_result)
        if "out" in args:
            with open(os.path.join(args["cwd"], args["out"]), "wb") as of:
                of.write(merged_result)
    else:
        print("No content found or specified")
        exit(1)


if __name__ == "__main__":
    main()
