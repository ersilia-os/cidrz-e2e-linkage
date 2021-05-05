---
description: >-
  This simple App displays a control menu to generate synthetic data for record
  linkage studies.
---

# Synthetic data generation

## Run as part of the e2elink package

```text
e2elink run syndata
```

## Motivation

* Anonymize Personally Identifieable Information \(PII\)
* Lack of gold standards
* Small and large files
* Test linkage pipelines under different conditions
* Educational purposes

## Key concepts

### File types

* **Source file**: The main file of interest.
* **Target file**: Typically, a large file containing. Source file entries are searched within this file.
* **Linkage file**: Contains pairs of indices corresponding to source and target rows. This file can be considered to be the ground truth \(gold standard\).

### Reference columns

* **Identifier**: Expected to be unique.
* **Name**: Full name, first & last...
* **Age**: Age, year of birth, birth date.
* **Date**: Date of registry or visit. Typically sorted.

### Algorithm steps

1. Get parameters \(from user or observed in real tables, e.g. SmartCare\).
2. Generate reference tables. These tables are full and clean.
3. Transform files to change column names, add missing values, misspellings, etc.

## Use of machine learning

* **Vectorization**: Represent text data in a vectorial format, for example, with a character-sensitive word embedding method \(e.g. [FastText](https://fasttext.cc/)\).
  * Calculate similarities between words.
  * Train classifiers.
* **Generative models**: These models are useful to capture correlations between fields. An example would be a [Generative Adversarial Network](https://sdv.dev/SDV/user_guides/single_table/ctgan.html) \(GAN\).

