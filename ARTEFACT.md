# Data Quality Summary Report

## Overview
This report summarizes data quality for a single numeric field across 4 sample records. The goal is to identify missing values and assess the distribution of observed values.

## Summary Statistics

| Metric            | Value   |
|-------------------|---------|
| Records analyzed  | 4       |
| Non-null values   | 3       |
| Missing values    | 1       |
| Invalid values    | 0       |
| Missing rate      | 25.0%   |
| Mean              | 20.0    |
| Min               | 10.0    |
| Max               | 30.0    |
| Range             | 20.0    |
| Median            | 20.0    |

## Interpretation
The dataset is small (4 records) and mostly complete, with a 25% missing rate (1 out of 4 values missing in the target field) and no invalid values. The observed values (10, 20, 30) are evenly spaced around a mean and median of 20.0, suggesting a symmetric distribution. No outliers are present in this sample.

## Recommendations
- Investigate the cause of the missing value and whether it can be recovered.
- Collect additional records to improve statistical reliability.
- Consider imputation strategies (e.g., mean or median imputation) for downstream analysis, if appropriate.