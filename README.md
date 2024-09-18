# Extractous Benchmarks

This repository contains datasets and source code for benchmarking three libraries for text extraction from PDF documents:

- `unstructured.io`
- `extractous`
- `PyPDF2`

The benchmarking suite focuses on evaluating the performance and memory efficiency of these libraries in extracting text from various types of PDF documents.

## Dataset

The dataset used for benchmarking is based on the [KG-RAG Datasets](https://github.com/docugami/KG-RAG-datasets/tree/main/sec-10-q/data/v1/docs). It consists of SEC filings for major companies in PDF format. These documents are diverse in structure and complexity, making them suitable for evaluating the text extraction capabilities of different libraries.

* The dataset files are stored in the `dataset/sec10-filings` directory within this repository.
* The corresponding ground truth files used to evaluate the quality of the extraction are in `dataset/sec10-ground-truth`

## Requirements
- GNU Bash (for running benchmark scripts)
- Python 3.8 or later
- [Poetry](https://python-poetry.org/) for dependency management
- [Matplotlib](https://matplotlib.org/) for plotting results
- [`hyperfine`]() (for measuring execution time)
- [`jq`]() (for processing JSON data)

### Installing Additional Linux Requirements

You can install `hyperfine` and `jq` on Linux using the following commands:

```bash
sudo apt-get update
sudo apt-get install hyperfine jq
```

### Install the dependencies using Poetry:

```bash
poetry install
```

### Running Benchmarks
The main benchmarking script is `benchmarks.sh`, which will execute the text extraction for each library and collect the results.
This script will output the results into a new directory under `results` tagged with the current date eg: `sec10-filings_18_09_2024`.

To run the benchmarks, execute the following command:

```bash
./benchmarks.sh
```

### Plotting Results
After running the benchmarks, you can visualize the results using the `plot_results.py` script. 
This script generates plots that compare the performance of the libraries in terms of speed and memory usage.
The plots will be saved in the provided directory

To plot the results, run:

```bash
./plot_results.py results/sec10-filings_18_09_2024
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or new features to propose.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.
