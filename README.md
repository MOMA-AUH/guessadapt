# guessadapt

[![Conda Version](https://img.shields.io/conda/vn/MOMA-AUH/guessadapt?cacheSeconds=300)](https://anaconda.org/MOMA-AUH/guessadapt) [![Conda Downloads](https://img.shields.io/conda/dn/MOMA-AUH/guessadapt?cacheSeconds=300)](https://anaconda.org/MOMA-AUH/guessadapt)

Given a FASTQ file and a list of adapter sequences, `guessadapt` simply counts the number of occurrences of each adapter and returns a sorted list of counts. That's it!

## Installation

The recommended way to install **guessadapt** is via [conda](https://docs.conda.io/), using the `MOMA-AUH` channel:

```bash
conda install MOMA-AUH::guessadapt
```

## Usage

```text
guessadapt --help
usage: guessadapt [-h] [--version] [--limit LIMIT] [--adapters ADAPTERS] fastq

positional arguments:
  fastq                 path to input FASTQ file

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --limit LIMIT, -n LIMIT
                        maximal number of reads to consider
  --adapters ADAPTERS, -a ADAPTERS
                        comma-separated list of adapters (default:
                        AGATCGGAAGAGC,TGGAATTCTCGG,CTGTCTCTTATA)
```
