#!/usr/bin/env python3

from extractous import Extractor, PdfOcrStrategy, PdfParserConfig
from utils import parse_infile_outfile_args


def extractous_stream(file_path, output_file_path):
    output_file = open(output_file_path, "wb")

    pdf_config = PdfParserConfig().set_ocr_strategy(PdfOcrStrategy.NO_OCR)
    extractor = Extractor().set_pdf_config(pdf_config)
    reader = extractor.extract_file(file_path)

    # Write output
    BUFFER_SIZE = 1024 * 1024 # 1MB buffer
    buffer = reader.read(BUFFER_SIZE)
    while len(buffer) > 0:
        output_file.write(buffer)
        buffer = reader.read(BUFFER_SIZE)

    output_file.flush()
    output_file.close()
    return output_file_path

if __name__ == '__main__':
    (file, out_file) = parse_infile_outfile_args()
    extractous_stream(file, out_file)