# Data Source Documentation

## 1. Dataset Overview

This project uses the **Customer Shopping Behavior Dataset** as the primary source for analyzing customer purchasing patterns, product performance, customer value, subscription behavior, and promotional activity.

The dataset contains customer-level shopping information across demographics, products, purchasing behavior, payment methods, shipping preferences, discounts, and customer ratings.

### Dataset Source

**Source:** Kaggle  
**Dataset:** Customer Shopping Behavior Dataset  
**Original Dataset Link:**  
https://www.kaggle.com/datasets/saadaliyaseen/shopping-behaviour-dataset/data

A GitHub-hosted copy of the dataset is also used during project development:

https://github.com/amlanmohanty1/customer-trends-data-analysis-SQL-Python-PowerBI/blob/main/customer_shopping_behavior.csv

---

## 2. Dataset Purpose

The dataset is used to answer business questions related to:

- Customer purchase value
- Customer engagement
- Product and category performance
- Subscription adoption
- Discount usage
- Customer ratings
- Purchase frequency
- Demographic behavior
- Geographic contribution
- Shipping and payment preferences
- Seasonal purchasing patterns

The analysis is designed to support **commercial and customer-focused decision-making**, rather than simply performing exploratory data analysis.

---

## 3. Dataset Structure

The raw dataset contains:

| Attribute | Value |
|---|---:|
| Records | 3,900 |
| Columns | 18 |
| File Format | CSV |
| Primary Identifier | `Customer ID` |
| Date/Time Field | Not available |
| Order ID | Not available |
| Quantity Field | Not available |
| Cost/Margin Field | Not available |

Each record represents an observed customer purchase record in the supplied dataset.

---

## 4. Raw Dataset Columns

The original dataset contains the following 18 columns:

1. Customer ID
2. Age
3. Gender
4. Item Purchased
5. Category
6. Purchase Amount (USD)
7. Location
8. Size
9. Color
10. Season
11. Review Rating
12. Subscription Status
13. Shipping Type
14. Discount Applied
15. Promo Code Used
16. Previous Purchases
17. Payment Method
18. Frequency of Purchases

These columns will be standardized during the ETL process into analytical-friendly names using lowercase `snake_case`.

For example:

```text
Customer ID              → customer_id
Purchase Amount (USD)    → purchase_amount
Review Rating            → review_rating
Previous Purchases       → previous_purchases
Subscription Status      → subscription_status
```

---

## 5. Data Collection and Preservation

The original/raw dataset should be preserved without modification under:

```text
data/
└── raw/
    └── customer_shopping_behavior.csv
```

The raw file acts as the **source-of-truth input** for the ETL pipeline.

No cleaning, transformation, imputation, or feature engineering should be performed directly on the raw file.

All transformations should be performed programmatically through the ETL pipeline.

---

## 6. Data Processing Flow

The dataset follows this processing flow:

```text
Raw CSV
   │
   ▼
Extract
   │
   ▼
Transform
   │
   ├── Standardize column names
   ├── Correct data types
   ├── Clean categorical values
   ├── Handle missing ratings
   ├── Remove analytical redundancy
   └── Create business features
   │
   ▼
Validate
   │
   ▼
Processed Dataset
   │
   ├── SQL Database
   │
   └── Power BI
```

The objective is to ensure that the analytical dataset can be reproduced from the untouched raw dataset.

---

## 7. Data Quality Notes

Initial profiling identifies several important data-quality considerations.

### Missing Values

`Review Rating` contains missing observations.

These missing ratings should not be interpreted as zero ratings.

The ETL process will handle these missing values using a documented imputation strategy while retaining an indicator showing which ratings were imputed.

Example:

```text
rating_was_imputed = True / False
```

This preserves transparency during analysis.

### Duplicate Records

Both full-row duplicates and identifier-level uniqueness should be checked during the data-quality audit.

`Customer ID` appears to be unique in the supplied dataset.

However, identifier uniqueness should be validated programmatically rather than assumed.

### Redundant Fields

`Discount Applied` and `Promo Code Used` contain effectively equivalent information in the supplied dataset.

Therefore:

- `discount_applied` will be retained as the primary analytical field.
- `promo_code_used` may be removed from the processed analytical table after redundancy has been verified.
- The original field will remain available in the raw dataset for traceability.

---

## 8. Dataset Limitations

The dataset does not contain:

- Transaction dates
- Order IDs
- Product costs
- Profit margins
- Quantities purchased
- Customer acquisition dates
- Customer churn status
- Historical transaction-level records
- Promotion cost
- Actual discount amount

Therefore, the project will not attempt to calculate metrics that require these fields.

For example, the dataset cannot reliably support:

- Monthly revenue trends
- Customer retention rate
- Churn rate
- Cohort retention
- True Customer Lifetime Value
- Profitability
- Gross margin
- Units sold
- Discount ROI
- Customer tenure

These limitations are documented in detail in:

```text
documentation/assumptions_limitations.md
```

---

## 9. Intended Analytical Use

The dataset will be used to develop a business analytics solution focused on:

### Customer Analytics

- Customer value segmentation
- Purchase-history engagement
- Subscription adoption
- Demographic purchasing behavior

### Product Analytics

- Category performance
- Product contribution
- Product ratings
- High-sales/low-rating opportunities

### Commercial Analytics

- Purchase value
- Discount usage
- Subscription opportunities
- Customer-product relationships

### Behavioral Analytics

- Purchase frequency
- Previous purchase behavior
- Payment preferences
- Shipping preferences
- Seasonal purchasing patterns

---

## 10. Data Lineage

The project maintains the following data lineage:

```text
Kaggle Dataset
      │
      ▼
Raw CSV
      │
      ▼
Python ETL Pipeline
      │
      ├── Extract
      ├── Transform
      └── Validate
      │
      ▼
Clean Analytical Dataset
      │
      ├── SQL Analysis
      └── Power BI
```

This structure ensures that the analytical outputs can be traced back to the original source data.

---

## 11. Reproducibility Principle

The processed dataset should never be treated as the primary source.

The **raw dataset is the source of truth**.

If the processed dataset is deleted, the complete analytical dataset should be reproducible by running the ETL pipeline against:

```text
data/raw/customer_shopping_behavior.csv
```

This makes the project reproducible and demonstrates a production-oriented data workflow.

---

## 12. Documentation Status

| Documentation Item | Status |
|---|---|
| Dataset Source Identified | Complete |
| Raw Data Preserved | Planned |
| Dataset Structure Documented | Complete |
| Data Quality Considerations Identified | Complete |
| Data Limitations Identified | Complete |
| ETL Lineage Defined | Complete |
| Reproducibility Approach Defined | Complete |

---

**Next documentation file:** `data_grain.md`