---
description: Simple generation of realistic synthetic datasets
---

# Synthetic data

## Introduction

Synthetic data generation is key to record linkage because, most often, we have to deal with sensitive data, involving personally identifiable information, which hampers data sharing and collaboration.

This tool produces synthetic that is very similar to the datasets that we have encountered in our experience with medical 

* **Source file**: The main file of interest.
* **Target file**: Typically, a large file containing. Source file entries are searched within this file.
* **Linkage file**: Contains pairs of indices corresponding to source and target rows. This file can be considered to be the ground truth \(gold standard\).



* Anonymize Personally Identifiable Information \(PII\)
* Lack of gold standards
* Small and large files
* Test linkage pipelines under different conditions
* Educational purposes

## Usage

### Run in the command line

The following command will generate a random synthetic dataset in the current working directory.

```text
$ e2elink synthetic
```

This will generate a realistic dataset that we believe is reasonable. You can pass a configuration file if you prefer:

```text
$ e2elink synthetic --params synthetic_params.yml
```

The parameters file can look like this:

{% code title="synthetic\_params.yml" %}
```yaml
# source file
src:
  - size: 100
# target file
trg:
  - size: 1000
# truth file
truth:
  - expected_rate: 0.7
```
{% endcode %}

Alternatively, you can see our template parameters file and edit it manually. The following command will produce this file named `synthetic_params.yml`:

```text
$ e2elink synthetic --template-params
```

### Run in the browser

An easier way to produce customized synthetic data is to use the synthetic data generator app. You launch it locally with the following command:

```text
$ e2elink synthetic --app
```

{% hint style="info" %}
An online demo of the synthetic data generator is [available here](http://example.com).
{% endhint %}

