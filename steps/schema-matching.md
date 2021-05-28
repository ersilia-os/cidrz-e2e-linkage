---
description: The first step of record linkage is recognizing the inputs.
---

# Schema matching

## Introduction

Schema matching refers to the mapping of columns in an input dataset to a set of standard columns that we will eventually use as linkage variables. For example, the full name of a person is sometimes referred to as _Client Name_, whereas sometimes it is specified in two fields, _Name_ and _Surname_.

The task of the schema matching can be summarized as follows:

1. Get column names of the input file
2. Read the content of the columns
3. Map column names to standard fields based on column contents

Mapping is done based on pre-trained text-based classifiers built with a massive dataset of synthetic data. Pretrained models are downloaded automatically \(you can find them [here](http://example.com) too\). We used the fantastic [FastText](https://fasttext.cc/) tool to build the language-based models.

## Standard fields

The majority of datasets that we encounter at CIDRZ contain only a limited number of linkage variables. We identify the following types of columns:

### Reference fields

| Field | Description | Standard format |
| :--- | :--- | :--- |
| full\_name | First name and last name | john smith |
| birth\_date | Date of birth | 1985-01-31 |
| visit\_date | Date of data event, typically a visit to the clinic | 2020-12-31 |
| sex | Gender | m |
| identifier | Unique identifier for the patient | 23956b40-2cc9-4e50 |

### Other standard fields

| Field | Reference field | Description | Standard format |
| :--- | :--- | :--- | :--- |
| first\_name | full\_name | First name | john |
| last\_name | full\_name | Last name | smith |
| age | birth\_date | Age | 35 |
| birth\_year | birth\_date | Year of birth | 1985 |

{% hint style="info" %}
We recognize that the current number of standard fields is limited. We are willing to add more upon request. Please [reach out to us](https://github.com/ersilia-os/cidrz-e2e-linkage/issues) if you have ideas or suggestions.
{% endhint %}

## Usage

```text
$ e2elink step match
```

#### Edit matching

The schema matching tool will do its best to match columns to standard columns. The mapping will be stored in a file that looks like this:

{% code title="match.yml" %}
```yaml
# standard fields
standard:
 - first_name: "Name"
 - last_name: "Surname"
 - age: "Age"
 - visit_date: "Date"
```
{% endcode %}

You can manually edit this file if you are not satisfied with it. The preprocessing step is going to read it.

#### Predefined matching

If you know the matching beforehand, you can specify it to make speed up the process. For example, you pre-specify the visit data column and let the tool guess the rest:

{% code title="my\_match.yml" %}
```yaml
# standard fields
standard:
 - visit_date: "Date of visit"
```
{% endcode %}

Then, pass this file when running the matching step:

```yaml
$ e2elink step math --file my_match.yml
```

