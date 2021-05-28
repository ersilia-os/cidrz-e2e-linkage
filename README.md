---
description: >-
  The e2elink executes a full record linkage pipeline without the need for human
  intervention.
---

# Welcome to End-to-End linkage!

This project is the result of a collaborative effort conducted at CIDRZ to perform end-to-end linkage in low-resourced settings.

## Features

We recommend using a `conda` environment:

```text
$ conda create -n e2elink python=3.7
$ conda activate e2elink
```

Then simply run:

```text
$ pip install e2elink
```

A command-line interface will be available to you:

```text
$ e2elink --help
```

{% hint style="warning" %}
This package uses pre-trained machine-learning models and pre-computed synthetic data that require about 1 GB of disk space. These data will be downloaded the first time the software is run.
{% endhint %}

