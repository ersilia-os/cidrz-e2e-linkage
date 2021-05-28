---
description: >-
  It is not necessary to compare all pairs of records, blocking can save us a
  lot of time
---

# Blocking

## Introduction

Blocking is a technique to reduce the number of fine-grained comparisons that are necessary to identify true linkage hits.

1. Vectorize the source and target datasets
2. For each row in the source file, find the top-k nearest neighbours in the target file

Blocking needs to be efficient computationally in order to work in low-resource settings. We use [FAISS](https://github.com/facebookresearch/faiss) \(for dense vectors\) or [PySparnn](https://github.com/facebookresearch/pysparnn) \(for sparse vectors\). The default now is to use sparse vectors as returned by Scikit-Learn [TF-IDF vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).

## Usage

```text
$ e2elink step block
```



