# Data preprocessing

## Background

### Data sources

This project primarily works with data from a Zambian based Cervical Cancer programme and also from the Zambia based HIV/AIDS programme that utilises SmartCare as its EHR

**Summary of Cervical Cancer and SmartCare Data**

| Details | CaCx | SmartCare |
| :--- | :--- | :--- |
| Total records |  |  |
| Data range |  |  |
| Age 15 - 20, |  |  |
| Age 21-30 |  |  |
| Age 31-40 |  |  |
| Age 41-50 |  |  |
| Age &gt;50 |  |  |
| Number of clinics |  |  |
|  |  |  |

### Nature of the data - known issues

* Missing complete date of birth
* Age fields mixed with client age, or client year of birth. In very rare instances, a client's actual date of birth is included
* 
## Pre-processing Implementation

The approach to the design and implementation has been to make the system not hard-coded to Cervical Cancer and SmartCare. In addition, the idea of pre-processing stage would be preceed by an automated step that determines the nature of the fields to be passed to the pre-processing step

### References types

Full name

Birth Year



