#!/usr/bin/env python3

import pypdfium2 as pdfium  # Importing pypdfium2
from utils import parse_infile_outfile_args


def run_pymupdf(file_path, output_file_path):
    output_file = open(output_file_path, "w")

    # Open the PDF file
    pdf = pdfium.PdfDocument(file_path)
    for page_num in range(len(pdf)):
        # Load the page
        page = pdf[page_num]
        # Extract text from the page
        text_page = page.get_textpage()
        # Extract text from the whole page
        text_all = text_page.get_text_bounded()

        # Write the text to the output file
        output_file.write(text_all)
        output_file.write("\n\n")

    output_file.flush()
    output_file.close()
    return output_file_path

if __name__ == '__main__':
    (file, out_file) = parse_infile_outfile_args()
    run_pymupdf(file, out_file)