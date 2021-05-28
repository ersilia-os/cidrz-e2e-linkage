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



