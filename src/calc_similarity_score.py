#!/usr/bin/env python3

from utils import calc_similarity_score, parse_infile1_infile2_args

if __name__ == '__main__':
    (file1, file2) = parse_infile1_infile2_args()
    print(calc_similarity_score(file1, file2))