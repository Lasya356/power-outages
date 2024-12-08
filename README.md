# Power Outages Data Analysis

<p>Authors: Ritvik Mohindru and Sai Sri Lasya Yadlapati</p>

## Introduction

### Dataset and Research Question Introduction

The dataset we chose to analyze contains information on major power outages across the United States, including factors such as the number of customers affected, outage duration, demand loss, cause category, and more. The guiding research question for our project is: <u>what factors are associated with the severity of major power outages?</u>

By analyzing a range of variables this dataset has to offer, we aim to uncover patterns that can help predict future major outages. Furthermore, our analyis and our research question are important, as understanding the factors influencing outage severity can help utility or energy companies better anticipate and reduce the scale of future major outages.

### Overview of Relevant Columns

The original dataset contains 1,534 rows of major outage events and 57 columns of related climatic, geographic, land-use, and economic characteristics.
Some key columns that we will be using in our analysis are described below:

| Column Name               | Description                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------- |
| `MONTH`                   | Month that outage event occurred                                                                   |
| `YEAR`                    | Year that outage event occurred                                                                    |
| `U.S._STATE`              | U.S. state in which outage event occurred                                                          |
| `POSTAL.CODE`             | Postal code of U.S. state in which outage event occurred                                           |
| `NERC.REGION`             | North American Electric Reliability Corporation (NERC) region that in which outage event occurred  |
| `CLIMATE.REGION`          | The U.S. climate region, as specified by the National Centers for Environmental Information (NCEI) |
| `CLIMATE.CATEGORY`        | Climate episode corresponding to the year                                                          |
| `OUTAGE.START.DATE`       | Day of the year when outage started                                                                |
| `OUTAGE.START.TIME`       | Time of the day when outage started                                                                |
| `OUTAGE.RESTORATION.DATE` | Day of the year when power was restored to all customers                                           |
| `OUTAGE.RESTORATION.TIME` | Time of the day when power was restored to all customers                                           |
| `CAUSE.CATEGORY`          | Main category outage cause                                                                         |
| `CAUSE.CATEGORY.DETAIL`   | Detailed description of outage cause                                                               |
| `CUSTOMERS.AFFECTED`      | Number of customers affected by the outage event                                                   |
| `TOTAL.CUSTOMERS`         | Total number of customers served annually in the U.S. state                                        |
| `OUTAGE.DURATION`         | Duration of the outage event in minutes                                                            |
| `DEMAND.LOSS.MW`          | Peak electricity demand lost during the outage event                                               |

## Data Cleaning and Exploratory Data Analysis

## Assessment of Missingness

## Hypothesis Testing

## Framing a Prediction Problem

## Baseline Model

## Final Model

## Fairness Analysis
