---
description: Medical record linkage is finally made easy. Get started!
---

# Quick start

## Prepare your data

We provide some exemplary datasets. These datasets are synthetic but greatly inspired by previous works we've done at CIDRZ. You can download them as follows:

```bash
$ e2elink example
```

{% hint style="success" %}
Three files will appear in your working directory. These correspond to a source file, a target file, and a truth file.
{% endhint %}

## Run full pipeline

You can run a full linkage pipeline as follows:

```bash
$ e2elink step all --src-file src.tsv --trg-file trg.tsv
```

An output folder will be created. The most important file in this folder is the results file. Have a look:

```bash
$ head output/results.tsv
```

If you prefer it, you can view results on your browser. A simple app will appear:

```bash
$ e2elink view results --folder output
```

## Run step by step

If you prefer to have full control over the linkage pipeline, you can run the code step by step.

#### 1. Set up output directory

First, you want to create an output directory where results will be stored.

```bash
$ e2elink step setup --src-file src.tsv --trg-file trg.tsv
```

#### 2. Schema matching

Check your input files and identify column types.

```bash
$ e2elink step schema
```

This will create a mapping file with the suggested correspondence between original column names and standard column names. For more details, please see:

{% page-ref page="concepts/linkage-variables.md" %}

#### 3. Data pre-processing

Once the schema of the input files has been identified, you need to preprocess the data.

```bash
$ e2elink step preprocess
```

This will create a preprocessed files with standard column names and cleaned data. Cleaning data is a critical step of record linkage. Learn more about how we do it here:

{% page-ref page="steps/preprocessing.md" %}

#### 4. Blocking

Blocking is a key step to ensure computational performance. By default, we block based on full names. For each row in the source file, we look for the nearest neighbors \(best candidates\) in the target file.

```bash
$ e2elink step block
```

A blocking index, specific to the target file, will be generated and stored as output. Please read more about blocking here:

{% page-ref page="steps/blocking.md" %}

#### 5. Comparison

Comparisons are the fun part of record linkage. Each reference field is compared using one multiple similarity metrics to achieve the best possible fuzzy matches.

```bash
$ e2elink step compare
```

We have done a big effort to have a comprehensive and efficient set of comparisons for each linkage variable. Learn more here:

{% page-ref page="steps/comparisons.md" %}

{% hint style="info" %}
We are always happy to include new types of comparisons. Please [reach out to us](https://github.com/ersilia-os/cidrz-e2e-linkage/issues) if you have suggestions!
{% endhint %}

#### 6. Scoring

We provide a single linkage score based on the multiple comparisons. This score is based on pre-trained and calibrated models based on synthetic data. So it can be interpreted as a probability.

```bash
$ e2elink step score
```

Our scoring methodology is a unique component of this record linkage package. Please learn more here:

{% page-ref page="steps/scoring.md" %}

