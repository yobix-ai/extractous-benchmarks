#!/usr/bin/env python3

from PyPDF2 import PdfReader
from utils import parse_infile_outfile_args


def run_pypdf2(file_path, output_file_path):
    output_file = open(output_file_path, "w")

    reader = PdfReader(file_path)
    for page in reader.pages:  # iterate the document pages
        output_file.write(page.extract_text())
        output_file.write("\n\n")

    output_file.flush()
    output_file.close()
    return output_file_path

if __name__ == '__main__':
    (file, out_file) = parse_infile_outfile_args()
    run_pypdf2(file, out_file)