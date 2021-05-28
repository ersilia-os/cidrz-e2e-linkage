---
description: >-
  Measuring the similarity between two entries can be difficult. We look at
  similarities from multiple viewpoints.
---

# Comparisons

## Introduction

Fuzzy matching is all about identifying the most relevant similarity metrics to compare two fields. Our approach is to compute multiple similarity metrics. The comparisons task can be summarized as follows:

1. For each pair \(as defined by the blocking step\), compare columns
2. Calculate multiple similarity metrics for each pair of columns
3. Store results as a comparisons matrix, having \(n, m\) dimensions, n being the number of pairs and m being the number of different metric calculation types

## Metrics

### Full name

| Metric | Abbreviation | Description |
| :--- | :--- | :--- |
| Exact | ex | Exact match between two strings |
| Levenshtein | lev | Number of edits needed to transform one word to the other |
| Jaro-Winkler | jw | Edit distance that gives more weight to initial characters |
| Match rating | mra | Simple set of phonetic rules |
| Cosine | cos | Angle between text-based vectors |
| Monge-Elkan Levenshtein | mel | Compare tokens \(first name, last name\) without taking into account the order. The Levenshtein similarity is used. |
| Monge-Elkan Jaro-Winkler | mejw | Idem. using Jaro-Winkler similarity. |

### Birth date

| Metric | Abbreviation | Description |
| :--- | :--- | :--- |
|  |  |  |

### Sex

| Metric | Abbreviation | Description |
| :--- | :--- | :--- |
| Exact | ex | Exact gender match |

{% hint style="info" %}
We are always exploring new types of metrics. If you have ideas or suggestions, please [reach out to us](https://github.com/ersilia-os/cidrz-e2e-linkage/issues)! We will be happy to incorporate your suggestions.
{% endhint %}

## Usage

By default, all metrics are calculated for each pair of samples.

```text
$ e2elink compare
```

{% hint style="warning" %}
This step can be slow. If you want to speed up the process, please consider reducing the k parameter in the blocking step or working with a less precise comparison.
{% endhint %}

A lighter but less precise version of the comparisons can be achieved as follows:

```text
$ e2elink compare --light
```

