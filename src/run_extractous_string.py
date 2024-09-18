#!/usr/bin/env python3

from extractous import Extractor
from utils import parse_infile_outfile_args


def extractous_string(file_path, output_file_path):
    output_file = open(output_file_path, "w")

    result = Extractor().extract_file_to_string(file_path)

    # Write output
    output_file.write(result)

    output_file.flush()
    output_file.close()
    return output_file_path

if __name__ == '__main__':
    (file, out_file) = parse_infile_outfile_args()
    extractous_string(file, out_file)