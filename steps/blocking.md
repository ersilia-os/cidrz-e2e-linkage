---
description: >-
  It is not necessary to compare all pairs of records, blocking can save us a
  lot of time
---

# Blocking

## Introduction

Blocking is a technique to reduce the number of fine-grained comparisons that are necessary to identify true linkage hits.

1. Vectorize the source and target datasets
2. For each row in the source file, find the top-k nearest neighbors in the target file

Blocking needs to be efficient computationally in order to work in low-resource settings. We use [FAISS](https://github.com/facebookresearch/faiss) \(for dense vectors\) or [PySparnn](https://github.com/facebookresearch/pysparnn) \(for sparse vectors\). The default now is to use sparse vectors as returned by Scikit-Learn [TF-IDF vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).

## Usage

You can run blocking on pre-processed data. The only real parameter is the number of neighbors \(k\). We determine k automatically \(between 5 and 100\) based on the size of your datasets.

```text
$ e2elink step block
```

This run will produce an index file based on the target data.

{% hint style="info" %}
Often, the target data is a large file that you want to use more than once \(for instance, to link it with multiple source files\). We cache this file so that your pipeline becomes more efficient.
{% endhint %}

