---
---
## From scratch Heap file and Hash index

> Originally written for some undergraduate DB systems class I took.

This is still a bit interesting to me as it's a from-scratch implementation of part of a DB and I think
it would be a good exercise to revisit this code and fix the bugs that are definitely in there somewhere.

Will be funny to see how bad the Java code is too.

### Usage

The dataset used in this project is available at https://data.gov.au/data/dataset/asic-business-names but
I've also copied a subset of that dataset into [./data/](./data) 

#### `dbload`

Implementing a heap file in Java. Load a database relation (.tsv) and write a heap file.

```bash
bazel run //databases/fromscratch_heapfile_and_hashindex:dbload -- \
    -p 4096 \
    "$(git rev-parse --show-toplevel)/databases/fromscratch_heapfile_and_hashindex/data/TRUNCATED_DATASET_WO_HEADER.csv"
```

#### `hashload`

A hash indexer that uses the heap file to build an index, `hash.<pagesize>`.

#### `dbquery`

Perform a text search using the heap file, with or without an index.

### Build

`bazel build //databases/fromscratch_heapfile_and_hashindex/...`

### Tests

... I guess tests weren't part of the assignment.
