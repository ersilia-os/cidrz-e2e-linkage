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

#### 5. Comparison

#### 6. Scoring



