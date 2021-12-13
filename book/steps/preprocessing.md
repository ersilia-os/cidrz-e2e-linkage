# Preprocessing

## Background

### Data sources



| Details           | XXX | XXX |
| ----------------- | --- | --- |
| Total records     |     |     |
| Data range        |     |     |
| Age 15 - 20,      |     |     |
| Age 21-30         |     |     |
| Age 31-40         |     |     |
| Age 41-50         |     |     |
| Age >50           |     |     |
| Number of clinics |     |     |
|                   |     |     |

### Nature of the data - known issues

* Missing complete date of birth
* Age fields mixed with client age, or client year of birth. In very rare instances, a client's actual date of birth is included
* **Pre-processing Implementation**

The approach to have a polymorphic interfaces that allows for various data sources has necessitated the definition of reference types that would allow for a more intuitive, modular and reusable interface. The defined references types are defined below

#### **References types -**

* **Full name** - This is a string of names that does not have a predefined ordering in names. It is possible that first name may come last in the string, or surname coming first in the string. The output from this clean needs to be limited to the number of name tokens needed. For instance, if the output return 6 name tokens, it can be predefined that only 2 tokens, first name and surname, are returned or first name, middle name and last name are returned

```python
FullName.config(column=name, ouput=[firstname, middlename, lastname], output_cols=[first, middle, last,other])
```

* **Age** - this is an integer field but tends to include year values. It returns integer value

```python
Age.config(src_column=age, output_type=int)
```

* **Birth year** - this is obtained in two ways 1) calculated, 2) retrieved from the age columns as well.&#x20;

```python
BirthYear.config(src_column=age, output=birth_year)
BirthYear.calc(src_col=[birthyear, scr_date], output=birth_year)
```

* **Screening date** - cleaned as a datetime value
* **VIA** - cleaned by matching and replacing values
* **HIV result** - cleaned by matching and replacing values
