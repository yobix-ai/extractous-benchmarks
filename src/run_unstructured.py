#!/usr/bin/env python3

from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy

from utils import parse_infile_outfile_args


def run_unstructured(file_path, output_file_path):
    output_file = open(output_file_path, "w")

    elements = partition(file_path, strategy=PartitionStrategy.FAST)

    # Write output
    for element in elements:
        output_file.write(element.text)
        output_file.write("\n\n")

    output_file.flush()
    output_file.close()
    return output_file_path

if __name__ == '__main__':
    (file, out_file) = parse_infile_outfile_args()
    run_unstructured(file, out_file)