
import sys
import os
import time

import Levenshtein

from urllib.request import urlretrieve

def parse_infile1_infile2_args():
    if len(sys.argv) != 3:
        print(f"Usage: '{sys.argv[0]}' <file1> <file2>")
        sys.exit(1)

    in_file1 = sys.argv[1]
    in_file2 = sys.argv[2]

    if not os.path.isfile(in_file1):
        raise FileNotFoundError(f"No such file: '{in_file1}'")

    if not os.path.isfile(in_file2):
        raise FileNotFoundError(f"No such file: '{in_file2}'")

    return in_file1, in_file2

def parse_infile_outfile_args():
    if len(sys.argv) != 3:
        print(f"Usage: '{sys.argv[0]}' <filename> <out_file>")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    if not os.path.isfile(in_file):
        raise FileNotFoundError(f"No such file: '{in_file}'")

    outdir = os.path.dirname(out_file)
    if not os.path.isdir(outdir):
        raise FileNotFoundError(f"Directory does not exist: '{outdir}'")

    return in_file, out_file

def download_file_if_not_found(url, file_path):
    if os.path.isfile(file_path):
        return
    urlretrieve(url, file_path)

def read_file_all(path: str) -> str:
    with open(path) as fp:
        return fp.read()

def calc_similarity_score(file1: str, file2: str):

    file1_str = read_file_all(file1)
    file2_str = read_file_all(file2)

    return Levenshtein.ratio(file1_str, file2_str)

def profile_func_speed(func, *args, **kwargs):
    start_time = time.perf_counter_ns()

    result = func(*args, **kwargs)

    duration_ns = time.perf_counter_ns() - start_time

    return result, duration_ns