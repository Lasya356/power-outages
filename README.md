# Power Outages Data Analysis

<p>Authors: Ritvik Mohindru and Sai Sri Lasya Yadlapati</p>

## Introduction

### Dataset and Project Question Introduction

The dataset we chose to analyze contains information on major power outages across the United States, including factors such as the number of customers affected, outage duration, demand loss, cause category, and more. The guiding question for our project is: <u>what factors are associated with the severity of major power outages?</u>

By analyzing a range of variables this dataset has to offer, we aim to uncover patterns that can help predict future major outages. Furthermore, our analysis and our research question are important because understanding the factors influencing outage severity can help utility or energy companies better anticipate and reduce the scale of future major outages.

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

Below is a detailed description of the data cleaning procedure that we implemented to prepare the `outages` dataset for analysis.

### Data Cleaning Steps

1. Combining Date and Time Columns

   - We combined the `OUTAGE.START.DATE` and `OUTAGE.START.TIME` columns into one datetime column named `OUTAGE.START`.<br>Likewise, we repeated the same for `OUTAGE.RESTORATION.DATE` and `OUTAGE.RESTORATION.TIME` into the new column: `OUTAGE.RESTORATION`.
   - This step made sure that both the outage start and restoration time information were consolidated into a single datetime format, reducing redundant details.

2. Convert Index and Columns to Appropriate Data Types

   - We converted the `OBS` index, along with the `YEAR` and `MONTH` columns to integers. It seems more reasonable for the `MONTH` and `YEAR` columns to be stored as integers, rather than as floats (specifically converted `MONTH` to a nullible integer `Int64`, to account for any missing values).

3. Handle Missing Data

   - We filled missing values in the `CUSTOMERS.AFFECTED` column to 0.0, as NaN values in this column suggest that no customers were affected by the outage event.
   - Also converted the `DEMAND.LOSS.MW` column to float and filled any missing values with 0.0, as any missing demand loss could imply no measurable demand lost during the outage.

4. Creating and Renaming Columns

   - We renamed the `OUTAGE.DURATION` column to `OUTAGE.DURATION (MINUTES)` to clarify the units.
   - Created a new column, `OUTAGE.DURATION.HOURS` by dividing the `OUTAGE.DURATION (MINUTES)` by 60 to help with simpler graphing during our later analysis.
   - Renamed the `U.S._STATE` column to just `STATE` for easier access to the column.

5. Selecting Relevant Columns

   - To simplify the dataset, we only retained the columns that were relevant to our analysis (only kept the columns described in the previous section).

6. Canonicalization

   - We removed the periods and underscores in the column names and also lower-cased the column names to achieve unformity in the dataset's columns.

<br>
Below are the first five rows of the cleaned dataset that we will be utilizing for our analysis:

| obs | month | year | state     | postal code | nerc region | climate region     | climate category | outage start        | outage restoration  | outage duration (minutes) | outage duration (hours) | cause category     | cause category detail | customers affected | total customers |  population | demand loss mw |
| --: | ----: | ---: | :-------- | :---------- | :---------- | :----------------- | :--------------- | :------------------ | :------------------ | ------------------------: | ----------------------: | :----------------- | :-------------------- | -----------------: | --------------: | ----------: | -------------: |
|   1 |     7 | 2011 | Minnesota | MN          | MRO         | East North Central | normal           | 2011-07-01 17:00:00 | 2011-07-03 20:00:00 |                      3060 |                      51 | severe weather     | nan                   |              70000 |      2.5957e+06 | 5.34812e+06 |              0 |
|   2 |     5 | 2014 | Minnesota | MN          | MRO         | East North Central | normal           | 2014-05-11 18:38:00 | 2014-05-11 18:39:00 |                         1 |               0.0166667 | intentional attack | vandalism             |                  0 |     2.64074e+06 | 5.45712e+06 |              0 |
|   3 |    10 | 2010 | Minnesota | MN          | MRO         | East North Central | cold             | 2010-10-26 20:00:00 | 2010-10-28 22:00:00 |                      3000 |                      50 | severe weather     | heavy wind            |              70000 |      2.5869e+06 |  5.3109e+06 |              0 |
|   4 |     6 | 2012 | Minnesota | MN          | MRO         | East North Central | normal           | 2012-06-19 04:30:00 | 2012-06-20 23:00:00 |                      2550 |                    42.5 | severe weather     | thunderstorm          |              68200 |     2.60681e+06 | 5.38044e+06 |              0 |
|   5 |     7 | 2015 | Minnesota | MN          | MRO         | East North Central | warm             | 2015-07-18 02:00:00 | 2015-07-19 07:00:00 |                      1740 |                      29 | severe weather     | nan                   |             250000 |     2.67353e+06 | 5.48959e+06 |            250 |

### Univariate Analysis

Number of Outages Per Year

<iframe
  src="/projects/project04/assets/UNI-num-outages-per-year.html"
  width="800"
  height="600"
  frameborder="0"
></iframe>

### Bivariate Analysis

## Assessment of Missingness

## Hypothesis Testing

## Framing a Prediction Problem

## Baseline Model

## Final Model

## Fairness Analysis
