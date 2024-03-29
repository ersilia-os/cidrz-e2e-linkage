---
description: The e2elink is a Python package. Installation should be straightforward.
---

# Installation

## Linux and MacOSX

We recommend using a [conda](https://docs.conda.io/en/latest/miniconda.html) environment:

```text
$ conda create -n e2elink python=3.7
$ conda activate e2elink
```

Then simply run: 

```bash
$ git clone https://github.com/ersilia-os/cidrz-e2e-linkage.git
$ cd cidrz-e2e-linkage
$ pip install -e .
```

{% hint style="success" %}
You are done!
{% endhint %}

A CLI command will be available to you.

```bash
$ ersilia --help
```

{% hint style="warning" %}
This package uses pre-trained machine-learning models and pre-computed synthetic data that require about 1 GB of disk space. These data will be downloaded the first time the software is run.
{% endhint %}

## For developers

The e2elink package contains many machine-learning functionalities that were necessary to prepare a pre-trained list of models. To obtain a fully-featured version of the tool, run:

```bash
$ pip install .[dev]
```

