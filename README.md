# Power Outages Data Analysis

<p>Authors: Sai Sri Lasya Yadlapati and Ritvik Mohindru</p>

## Introduction

### Dataset and Project Question Introduction

The dataset we chose to analyze contains information on major power outages across the United States from January 2000 to July 2016, including factors such as the number of customers affected, outage duration, demand loss, cause category, and more. The dataset we used can be retrieved from [https://engineering.purdue.edu/LASCI/research-data/outages](https://engineering.purdue.edu/LASCI/research-data/outages). The guiding question for our project is: <u>what characteristics are associated with each category of cause?</u>

By analyzing a range of variables this dataset has to offer, we aim to uncover patterns that are associated with different cause categories of major power outages. Furthermore, our analysis and our research question are important because understanding the various factors contributing to power outages can help utility or energy companies better anticipate and prepare for future major outages.

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

   - We combined the `OUTAGE.START.DATE` and `OUTAGE.START.TIME` columns into one datetime column named `OUTAGE.START`. Likewise, we repeated the same for `OUTAGE.RESTORATION.DATE` and `OUTAGE.RESTORATION.TIME` into the new column: `OUTAGE.RESTORATION`.
   - This step made sure that both the outage start and restoration time information were consolidated into a single datetime format, reducing redundant details.

2. Convert Index and Columns to Appropriate Data Types

   - We converted the `OBS` index, along with the `YEAR` and `MONTH` columns to integers.
   - It seems more reasonable for the `MONTH` and `YEAR` columns to be stored as integers, rather than as floats (specifically converted `MONTH` to a nullible integer `Int64`, to account for any missing values).

3. Creating, Removing, and Renaming Columns

   - We renamed the `OUTAGE.DURATION` column to `OUTAGE.DURATION (MINUTES)` to clarify the units.
   - Created a new column, `OUTAGE.DURATION.HOURS` by dividing the `OUTAGE.DURATION (MINUTES)` by 60 to help with simpler graphing during our later analysis.
   - Renamed the `U.S._STATE` column to just `STATE` for easier access to the column.

4. Selecting Relevant Columns

   - To simplify the dataset, we only retained the columns that were relevant to our analysis (only kept the columns described in the previous section).

5. Canonicalization

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

The histogram below displays the frequency distribution of the different cause categories for power outage events. The 'severe weather' cause category seems to have the highest frequency, which could possibly suggest that weather-related events are a leading cause for major power outages.

<iframe
  src="assets/UNI-cause-cat-freq.html"
  width="950"
  height="450"
  frameborder="0"
></iframe>

### Bivariate Analysis

The box plot below displays the relationship between cause categories of power outages and their durations. Based on this plot, we can infer that severe weather and fuel supply emergencies seem to cause power outages of the longest median durations; whereas, islanding and intentional attack appear to cause outage events of the shortest median durations.

<iframe
  src="assets/BI-outage-dur-vs-cause-cat.html"
  width="1050"
  height="550"
  frameborder="0"
></iframe>

### Interesting Aggregates

Here, we explored the relationship between climate region and key factors such as outage duration, customers affected, and demand loss in megawatts.

The following dataframe summarizes the aggregated mean values for these factors, grouped by `climate region`.

| climate region     | outage duration (hours) | customers affected | demand loss mw |
| :----------------- | ----------------------: | -----------------: | -------------: |
| Central            |                 45.0188 |             126810 |        477.482 |
| East North Central |                 89.2007 |             138389 |        560.406 |
| Northeast          |                 49.8609 |             121960 |        537.411 |
| Northwest          |                 21.4083 |              81420 |        177.897 |
| South              |                  47.435 |             183501 |        399.087 |
| Southeast          |                 36.9614 |             180540 |        761.533 |
| Southwest          |                 26.1023 |            39028.9 |        424.556 |
| West               |                 27.1389 |             194580 |        651.457 |
| West North Central |                 11.6094 |              47316 |            326 |

<iframe
  src="assets/AGG-climate-region-outage-dur.html"
  width="1000"
  height="550"
  frameborder="0"
></iframe>

From the above bar chart and the aggregated table, it is evident that the East North Central climate region seems to have the longest lasting power outage events, on average, while the West North Central climate region seems to have the shortest.

Additionally, the West North Central region also appears to have the least amount of customers affected and demand loss, on average.

This aggregation is interesting, as it provides insights into the influence of climate region on factors such as outage duration, customers affected, and demand loss (megawatts). This information can help utility or energy companies to dedicate and prioritize resources to those climate regions with greater impacts (i.e. longer outage durations, more customers affected, higher demand loss, etc.). It could also allow them to invest in crucial infrastructure upgrades in order to mitigate and minimize the impact of future outage events.

## Assessment of Missingness

### NMAR Analysis

In the dataset, many columns have missing values. Specifically, the missing values in the `demand loss mw` column in this dataset are likely to be not missing at random (NMAR). In simple terms, demand loss (megawatts) represents the amount of power lost during an outage event. However, in most cases, the value seems to be reflecting the total power loss over the duration of the outage, rather than at a single point. This column is possibly NMAR, as the missingness is likely dependent on the values itself -- for example, if the demand loss is too large to be computed. The complexities involved in computing these values may have resulted in the column's missingness. Essentially, larger outage events, which usually involve more complex calculations, such as aggregating power loss data from multiple companies and multiple causal factors, are more prone to missing values. This suggests that the missigness of the values in the `demand loss mw` column are dependent on the values themselves -- as larger values are likely to be missing. Therefore, the `demand loss mw` column is likely NMAR, as the missingness of the values likely depend on the scale of the outage event, as the values would be more difficult to compute for larger outages.

However, additional data can be gathered to make the missingness of this column MAR (missing at random). Obtaining data regarding the electricity generated during the power outage would make the `demand loss mw` column MAR. The `demand loss mw` column is calculated based on the amount of power lost during an outage event, which reqiures information about the power generated. If the data on the amount of power generated were missing, the `demand loss mw` column should, in theory, also be missing. In this specific case, the missigness of `demand loss mw` would depend on the new "power generated" column. Thus, collecting data on the electricity generated during the outage event can help explain the missingness of `demand loss mw`, making it MAR.

### Missingness Dependency

In this section, we investigates whether there was a missingness dependency between the `month` column and two other columns: `outage restoration` and `cause category detail`.

#### Month Against Outage Restoration

We tested whether the missingness in the `outage restoration` column is dependent on the `month` column.

**Null Hypothesis**: The distribution of `month` is the same when `outage restoration` is missing and not missing.

**Alternative Hypothesis**: The distribution of `month` is different when `outage restoration` is missing and not missing.

**Test Statistic**: We used the Total Variation Distance (TVD) as our test statistic.

**Observed TVD**: We found an observed TVD of 0.223.

**Significance Level**: We chose to set the significance level at 0.05.

**Resulting P-Value**: After performing 10,000 permutations, we got a p-value of 0.1238.

**Visualizations**:

Below is a horizontal bar chart depicting the distribution of the `month` column when `outage restoration` is missing and when it is not missing.

<iframe
  src="assets/MD-month-outage-rest.html"
  width="1000"
  height="550"
  frameborder="0"
></iframe>

Below is the empirical distribution of the Total Variation Distance (TVD).

<iframe
  src="assets/MD-month-outage-rest-tvd.html"
  width="1000"
  height="500"
  frameborder="0"
></iframe>
**Conclusion**: After conducting the permutation test, the p-value obtained was 0.136, which is greater than the specified significance level of 0.05. Thus, we fail to reject the null hypothesis -- that the distribution of `month` is the same when `outage restoration` is missing and not missing -- meaning that the missingness of the `outage restoration` column is not dependent on the `month` column.

#### Month Against Cause Category Detail

We tested whether the missingness in the `cause category detail` column is dependent on the `month` column.

**Null Hypothesis**: The distribution of `month` is the same when `cause category detail` is missing and not missing.

**Alternative Hypothesis**: The distribution of `month` is different when `cause category detail` is missing and not missing.

**Test Statistic**: We used the Total Variation Distance (TVD) as our test statistic.

**Observed TVD**: We found an observed TVD of 0.15.

**Significance Level**: We chose to set the significance level at 0.05.

**Resulting P-Value**: After performing 10,000 permutations, we got a p-value of 0.0.

**Visualizations**:

Below is a horizontal bar chart depicting the distribution of the `month` column when `cause category detail` is missing and when it is not missing.

<iframe
  src="assets/MD-month-ccd.html"
  width="1000"
  height="550"
  frameborder="0"
></iframe>

Below is the empirical distribution of the Total Variation Distance (TVD).

<iframe
  src="assets/MD-month-ccd-tvd.html"
  width="1000"
  height="550"
  frameborder="0"
></iframe>

**Conclusion**: After conducting the permutation test, the p-value obtained was 0.0, which is less than the specified significance level of 0.05. Thus, we reject the null hypothesis -- that the distribution of `month` is the same when `cause category detail` is missing and not missing -- meaning that the missingness of the `cause category detail` column is dependent on the `month` column.

## Hypothesis Testing

In this hypothesis test, we examine whether the distribution of climate regions, specifically the West and Central climate regions, differs significantly across various cause categories. This analysis is important, as it can help explain the relationship between specific climate regions and cause categories and understand how regional factors could influence the types of events causing power outages.

**Null Hypothesis**: There is no difference in the distribution of the West and Central climate regions across all cause categories.

**Alternative Hypothesis**: There is a significant difference in the distribution of the West and Central climate regions across all cause categories.

**Test Statistic**: We used the Total Variation Distance (TVD) as our test statistic because it quantifies the difference between the categorical distributions of the West and Central climate regions across cause categories.

**Significance Level**: We chose to set the significance level at 0.05.

**Test**: We chose to use a permutation test because it allows us to compare the distributions of West and Central climate regions across the cause categories without making assumptions about the underlying data distribution.

**Resulting P-Value**: After performing 10,000 permutations, we got a p-value of 0.0.

**Visualizations**:

Below is a horizontal bar chart depicting the distribution of the cause categories over the two climate regions: West and Central.

<iframe
  src="assets/TEST-ccd-climate-reg.html"
  width="950"
  height="550"
  frameborder="0"
></iframe>

Below is a histogram illustrating the distribution of our test statistics from the permutation test. The test statistic represents the total variation distance between the West and Central climate region distributions across 10,000 permutations. The observed test statistic (red line) is also shown.

<iframe
  src="assets/TEST-tvd-cause-cat.html"
  width="850"
  height="550"
  frameborder="0"
></iframe>

**Conclusion**: After conducting the permutation test, the p-value obtained was 0.0, which is much less than the specified significance level of 0.05. Thus, we reject the null hypothesis and conclude that there is a significant difference in the distribution of the West and Central climate regions across all cause categories.

## Framing a Prediction Problem

From the hypothesis test conducted above, we found that there is a significant difference in some of the climate regions across all cause categories. This detail suggests that climatic factors could possibly influence the cause of outages. Assuming this, it's important to determine whether we can predict the cause category based on other variables, such as climate region, outage duration, customers affected, etc.

Simply put, our prediction problem is a multiclass classification task, where we aim to predict the cause of a major power outage (i.e. the `cause category` column).

We will be building a random forest classifier to predict the `cause category` column (response variable) because it can provide important information about the cause of the outage, which can allow utility companies to implement preventive measures and improve infrastructure where needed. The two mentioned features will generally be available at the time of prediction.

We will be using accuracy as one of our metrics. Accuracy as an evaluation metric can oftentimes be misleading if the classes in `cause category` are imbalanced. For instance, if severe weather were to occur more frequently as a cause than, islanding, for example, then accuracy will likely exaggerate our model's performance. Because this may very well be the case, we will opt for the F-1 score as well, as it does a great job of factoring in the model's precision and recall when a class imbalance is present.

## Baseline Model

For our baseline model, we used a Random Forest classifier to predict the `cause category` of major power outages, given only two feature columns: `climate region` (a categorical nominal column) and `outage duration (hours)` (a quantitative continuous column). `climate region` and `outage duration (hours)`.

We dropped any missing values in the `climate region` and `outage duration (hours)` to keep the model simple and avoid any issues while fitting the model.

We one-hot-encoded `climate region` and dropped the first column from the result of nine binary columns to avoid multicollinearity. Next, we standardized the `outage durations (hours)` column, as it will allow the random forest classifier model to perform more efficiently.

After fitting the model, it achieved an accuracy of 61.41% and an F-1 score of 35.99%. This model performed quite poorly, considering the large discrepancy between the F-1 and accuracy scores. This also suggests a heavy class imbalance, likely due the high frequency of the 'severe weather' cause category, causing our baseline model to predict this category often.

Our baseline model did not perform well, due to the presence of class imbalance within the target variable. The model's reliance on predicting the 'severe weather' cause category often greatly overstates the model's performance and ability to generalize to unseen data.

## Final Model

<!-- 1. Feature Engineering

- `year` : one-hot encode
- `climate region` : one-hot encode
- `outage duration (hours)` : standardize
- `customers affected` : quantile transform
- `demand loss (mw)`: standardize

acc=0.8197674418604651
f1=0.6004905812710123 -->

## Fairness Analysis
