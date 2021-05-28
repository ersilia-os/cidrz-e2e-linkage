---
description: >-
  We deal with a limited number of fields that we typically encounter in CIDRZ
  datasets
---

# Linkage variables

The majority of datasets that we encounter at CIDRZ contain only a limited number of linkage variables. We identify the following types of columns:

## Reference fields

| Field | Description | Standard format |
| :--- | :--- | :--- |
| full\_name | First name and last name | john smith |
| birth\_date | Date of birth | 1985-01-31 |
| visit\_date | Date of data event, typically a visit to the clinic | 2020-12-31 |
| sex | Gender | m |
| identifier | Unique identifier for the patient | 23956b40-2cc9-4e50 |

## Other standard fields

| Field | Reference field | Description | Standard format |
| :--- | :--- | :--- | :--- |
| first\_name | full\_name | First name | john |
| last\_name | full\_name | Last name | smith |
| age | birth\_date | Age | 35 |
| birth\_year | birth\_date | Year of birth | 1985 |

{% hint style="info" %}
We recognize that the current number of standard fields is limited. We are willing to add more upon request. Please [reach out to us](https://github.com/ersilia-os/cidrz-e2e-linkage/issues) if you have ideas or suggestions.
{% endhint %}

