# Data Dictionary

## 1. Purpose

This document defines the structure, meaning, data type, analytical role, and validation rules for each field in the **Customer Shopping Behavior Dataset**.

The raw dataset contains 18 columns. During the ETL process, column names will be standardized using lowercase `snake_case` naming conventions.

---

## 2. Dataset Summary

| Attribute | Value |
|---|---|
| Number of Records | 3,900 |
| Number of Raw Columns | 18 |
| Analytical Grain | One observed customer purchase record |
| Primary Identifier | `customer_id` |
| File Format | CSV |
| Currency | USD |

---

# 3. Complete Data Dictionary

## 3.1 Customer ID

| Property | Details |
|---|---|
| Raw Column | `Customer ID` |
| Clean Column | `customer_id` |
| Data Type | Integer |
| Analytical Role | Identifier |
| Description | Unique identifier associated with the customer represented by the record. |
| Expected Values | Positive integer |
| Null Allowed | No |
| Unique | Expected to be unique in the supplied dataset |
| Validation | Not null, integer, unique, positive |
| Business Use | Customer identification, customer counting, segmentation |

### Important Note

`customer_id` should not be interpreted as an Order ID or Transaction ID because the dataset does not contain a dedicated order or transaction identifier.

---

## 3.2 Age

| Property | Details |
|---|---|
| Raw Column | `Age` |
| Clean Column | `age` |
| Data Type | Integer |
| Analytical Role | Customer Attribute |
| Description | Age of the customer associated with the observed purchase record. |
| Expected Range | 18–70 |
| Null Allowed | No |
| Validation | Integer and within expected range |
| Business Use | Age-group segmentation and demographic analysis |

### Derived Feature

An `age_group` field may be created during ETL.

Example:

```text
18–24
25–34
35–44
45–54
55–64
65+
```

The final grouping should be validated against the actual age distribution.

---

## 3.3 Gender

| Property | Details |
|---|---|
| Raw Column | `Gender` |
| Clean Column | `gender` |
| Data Type | Categorical |
| Analytical Role | Dimension |
| Description | Gender category associated with the customer record. |
| Expected Values | Male, Female |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Demographic comparison and segmentation |

---

## 3.4 Item Purchased

| Property | Details |
|---|---|
| Raw Column | `Item Purchased` |
| Clean Column | `item_purchased` |
| Data Type | Categorical |
| Analytical Role | Product Dimension |
| Description | Specific product/item associated with the observed purchase record. |
| Expected Cardinality | Approximately 25 distinct items |
| Null Allowed | No |
| Validation | Non-null and standardized text |
| Business Use | Product-level performance analysis and ranking |

Examples may include individual apparel products such as shirts, jeans, jackets, shoes, etc.

---

## 3.5 Category

| Property | Details |
|---|---|
| Raw Column | `Category` |
| Clean Column | `category` |
| Data Type | Categorical |
| Analytical Role | Product Dimension |
| Description | Higher-level product category associated with the purchased item. |
| Expected Cardinality | 4 categories |
| Null Allowed | No |
| Validation | Non-null and standardized categorical values |
| Business Use | Category performance, contribution analysis and merchandising decisions |

---

## 3.6 Purchase Amount (USD)

| Property | Details |
|---|---|
| Raw Column | `Purchase Amount (USD)` |
| Clean Column | `purchase_amount` |
| Data Type | Numeric / Decimal |
| Analytical Role | Primary Measure |
| Description | Purchase value associated with the observed customer purchase record, expressed in US dollars. |
| Expected Range | Approximately $20–$100 |
| Null Allowed | No |
| Validation | Numeric, positive, within reasonable dataset range |
| Business Use | Sales-value analysis, customer value segmentation, category/product performance |

### Key Measures

This field is used to calculate:

```text
Total Purchase Value
Average Purchase Value
Purchase Value by Category
Purchase Value by Product
Purchase Value by Customer Segment
Purchase Value by Subscription Status
```

### Important Limitation

`purchase_amount` represents purchase value, not profit.

The dataset does not contain product cost or margin information.

---

## 3.7 Location

| Property | Details |
|---|---|
| Raw Column | `Location` |
| Clean Column | `location` |
| Data Type | Categorical |
| Analytical Role | Geographic Dimension |
| Description | Customer location/state associated with the observed purchase record. |
| Expected Cardinality | Approximately 50 locations/states |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Geographic sales contribution and customer behavior analysis |

---

## 3.8 Size

| Property | Details |
|---|---|
| Raw Column | `Size` |
| Clean Column | `size` |
| Data Type | Categorical |
| Analytical Role | Product Attribute |
| Description | Size selected for the purchased item. |
| Expected Values | Common apparel size categories such as S, M, L, XL |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Product preference and assortment analysis |

---

## 3.9 Color

| Property | Details |
|---|---|
| Raw Column | `Color` |
| Clean Column | `color` |
| Data Type | Categorical |
| Analytical Role | Product Attribute |
| Description | Color associated with the purchased item. |
| Expected Cardinality | Multiple color categories |
| Null Allowed | No |
| Validation | Standardized text values |
| Business Use | Product preference and merchandising analysis |

---

## 3.10 Season

| Property | Details |
|---|---|
| Raw Column | `Season` |
| Clean Column | `season` |
| Data Type | Categorical |
| Analytical Role | Behavioral Dimension |
| Description | Season category associated with the observed purchase record. |
| Expected Values | Spring, Summer, Fall, Winter |
| Null Allowed | No |
| Validation | Standardized seasonal categories |
| Business Use | Seasonal purchasing comparison |

### Important Limitation

`season` is a categorical field and should not be treated as a chronological time dimension.

The dataset does not contain actual transaction dates.

Therefore, the project can compare purchasing behavior across seasons but cannot calculate monthly or yearly trends.

---

## 3.11 Review Rating

| Property | Details |
|---|---|
| Raw Column | `Review Rating` |
| Clean Column | `review_rating` |
| Data Type | Decimal |
| Analytical Role | Customer Experience Measure |
| Description | Rating associated with the observed purchase/product experience. |
| Expected Range | 1–5 |
| Null Allowed | Yes in raw data |
| Missing Records | 37 |
| Validation | Numeric and within 1–5 |
| Business Use | Product/customer experience analysis |

### Missing Value Handling

The raw dataset contains missing review ratings.

These should not be replaced with zero because zero represents a fundamentally different meaning.

The ETL pipeline will use a documented imputation strategy and create:

```text
rating_was_imputed
```

This field indicates whether the original rating was missing and subsequently imputed.

---

## 3.12 Subscription Status

| Property | Details |
|---|---|
| Raw Column | `Subscription Status` |
| Clean Column | `subscription_status` |
| Data Type | Categorical |
| Analytical Role | Customer/Loyalty Dimension |
| Description | Indicates whether the customer has an active subscription status in the dataset. |
| Expected Values | Yes, No |
| Null Allowed | No |
| Validation | Standardized Yes/No values |
| Business Use | Subscription penetration and customer segmentation |

### Key Business Metrics

```text
Subscription Rate
Subscriber Purchase Value
Non-Subscriber Purchase Value
High-Engagement Non-Subscriber Share
```

---

## 3.13 Shipping Type

| Property | Details |
|---|---|
| Raw Column | `Shipping Type` |
| Clean Column | `shipping_type` |
| Data Type | Categorical |
| Analytical Role | Fulfillment Dimension |
| Description | Shipping method selected for the observed purchase. |
| Expected Cardinality | 6 shipping types |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Shipping preference and purchase-value analysis |

---

## 3.14 Discount Applied

| Property | Details |
|---|---|
| Raw Column | `Discount Applied` |
| Clean Column | `discount_applied` |
| Data Type | Categorical / Boolean-like |
| Analytical Role | Promotional Dimension |
| Description | Indicates whether a discount was applied to the observed purchase. |
| Expected Values | Yes, No |
| Null Allowed | No |
| Validation | Standardized Yes/No values |
| Business Use | Discount usage and purchase-value comparison |

### Key Metrics

```text
Discount Usage Rate
Purchase Value with Discount
Purchase Value without Discount
Discount Usage by Category
Discount Usage by Customer Segment
```

### Important Analytical Limitation

This field indicates whether a discount was applied but does not provide the actual discount amount.

Therefore, the project cannot calculate:

```text
Discount Amount
Discount Percentage
Discount ROI
Profit Impact of Discount
```

Also, differences between discounted and non-discounted purchases should be interpreted as associations rather than causal effects.

---

## 3.15 Promo Code Used

| Property | Details |
|---|---|
| Raw Column | `Promo Code Used` |
| Clean Column | `promo_code_used` |
| Data Type | Categorical / Boolean-like |
| Analytical Role | Promotional Attribute |
| Description | Indicates whether a promotional code was used for the observed purchase. |
| Expected Values | Yes, No |
| Null Allowed | No |
| Validation | Standardized Yes/No values |
| Business Use | Promotional behavior analysis |

### Redundancy Note

In the supplied dataset, `Promo Code Used` and `Discount Applied` are effectively equivalent.

This relationship should be verified during the ETL data-quality audit.

After verification:

```text
discount_applied
```

will be retained as the primary analytical field.

`promo_code_used` may be excluded from the processed analytical table to avoid redundant information.

The original raw field must remain untouched for traceability.

---

## 3.16 Previous Purchases

| Property | Details |
|---|---|
| Raw Column | `Previous Purchases` |
| Clean Column | `previous_purchases` |
| Data Type | Integer |
| Analytical Role | Customer Engagement Measure |
| Description | Number of previous purchases reported for the customer. |
| Expected Range | Approximately 1–50 |
| Null Allowed | No |
| Validation | Integer and positive |
| Business Use | Purchase-history engagement segmentation |

### Critical Interpretation

This field is a **count of previous purchases**.

It is not historical transaction-level data.

For example:

```text
previous_purchases = 20
```

means that the customer has a reported previous-purchase count of 20.

It does not mean that 20 historical transaction records are available for analysis.

### Appropriate Uses

```text
Average Previous Purchases
Purchase-History Engagement Segments
Previous Purchases vs Current Purchase Value
Subscription Status by Engagement
```

### Inappropriate Uses

```text
Customer Retention Rate
Cohort Analysis
Historical Revenue
Customer Tenure
Transaction-Level Purchase History
```

---

## 3.17 Payment Method

| Property | Details |
|---|---|
| Raw Column | `Payment Method` |
| Clean Column | `payment_method` |
| Data Type | Categorical |
| Analytical Role | Payment Dimension |
| Description | Payment method associated with the observed purchase. |
| Expected Cardinality | 6 payment methods |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Payment preference and customer behavior analysis |

---

## 3.18 Frequency of Purchases

| Property | Details |
|---|---|
| Raw Column | `Frequency of Purchases` |
| Clean Column | `purchase_frequency` |
| Data Type | Categorical |
| Analytical Role | Customer Behavior Dimension |
| Description | Purchase-frequency category reported for the customer. |
| Expected Cardinality | 7 categories |
| Null Allowed | No |
| Validation | Standardized categorical values |
| Business Use | Customer engagement and purchase-behavior segmentation |

### Important Limitation

This field provides a categorical frequency classification.

It should not be converted into exact transaction dates or exact purchase intervals unless the source documentation explicitly supports such an interpretation.

---

# 4. Field Classification

The dataset fields can be grouped into the following analytical categories.

## Customer Dimensions

```text
customer_id
age
gender
location
```

## Product Dimensions

```text
item_purchased
category
size
color
season
```

## Purchase Measure

```text
purchase_amount
```

## Customer Experience

```text
review_rating
```

## Loyalty / Engagement

```text
subscription_status
previous_purchases
purchase_frequency
```

## Promotion

```text
discount_applied
promo_code_used
```

## Fulfillment & Payment

```text
shipping_type
payment_method
```

---

# 5. Raw-to-Clean Column Mapping

| Raw Column | Clean Column |
|---|---|
| Customer ID | `customer_id` |
| Age | `age` |
| Gender | `gender` |
| Item Purchased | `item_purchased` |
| Category | `category` |
| Purchase Amount (USD) | `purchase_amount` |
| Location | `location` |
| Size | `size` |
| Color | `color` |
| Season | `season` |
| Review Rating | `review_rating` |
| Subscription Status | `subscription_status` |
| Shipping Type | `shipping_type` |
| Discount Applied | `discount_applied` |
| Promo Code Used | `promo_code_used` |
| Previous Purchases | `previous_purchases` |
| Payment Method | `payment_method` |
| Frequency of Purchases | `purchase_frequency` |

---

# 6. Derived Analytical Fields

The ETL process may create additional business-oriented fields.

## `age_group`

Groups customers into meaningful demographic bands.

Example:

```text
18–24
25–34
35–44
45–54
55–64
65+
```

---

## `purchase_value_band`

Categorizes customers based on observed purchase value.

Possible structure:

```text
Low
Medium
High
```

The actual thresholds should be determined using the observed distribution rather than arbitrary business assumptions.

---

## `engagement_segment`

Represents purchase-history engagement using `previous_purchases`.

Example conceptual segments:

```text
Low Engagement
Developing
Established
Highly Engaged
```

Thresholds should be data-driven and documented.

---

## `rating_was_imputed`

Boolean indicator showing whether `review_rating` was originally missing before ETL processing.

Possible values:

```text
True
False
```

This provides transparency around imputed customer ratings.

---

# 7. Recommended Analytical Measures

The following measures can be derived from the dataset.

### Sales / Purchase Value

```text
Total Purchase Value
Average Purchase Value
Median Purchase Value
Purchase Value by Category
Purchase Value by Product
Purchase Value by Location
```

### Customer

```text
Unique Customers
High-Value Customer Count
High-Value Customer Share
Average Previous Purchases
Average Purchase Value by Engagement
```

### Subscription

```text
Subscription Rate
Subscriber Purchase Value
Non-Subscriber Purchase Value
High-Engagement Non-Subscriber Share
```

### Product

```text
Category Purchase Value
Product Purchase Value
Product Contribution %
Average Product Rating
High-Sales / Low-Rating Products
```

### Promotion

```text
Discount Usage Rate
Discounted Purchase Value
Non-Discounted Purchase Value
Discount Usage by Category
Discount Usage by Customer Segment
```

---

# 8. Data Dictionary Governance

Any future changes to the dataset should trigger a review of this data dictionary.

The following should be revalidated:

```text
☐ Column names
☐ Data types
☐ Primary identifier
☐ Dataset grain
☐ Expected categorical values
☐ Numeric ranges
☐ Missing-value patterns
☐ Duplicate records
☐ Redundant fields
☐ Business meaning
☐ Derived features
```

Changes to the data model should also be reflected in:

```text
documentation/data_grain.md
documentation/assumptions_limitations.md
ETL scripts
SQL schema
Power BI data model
```

---

# 9. Final Analytical Model

After ETL, the primary analytical table is expected to contain the standardized fields:

```text
customer_id
age
gender
item_purchased
category
purchase_amount
location
size
color
season
review_rating
rating_was_imputed
subscription_status
shipping_type
discount_applied
previous_purchases
payment_method
purchase_frequency
age_group
purchase_value_band
engagement_segment
```

The exact final column set may be adjusted during implementation if a feature is found to be redundant or not useful for business analysis.

---

**Documentation Status:** Complete  
**Raw Fields:** 18  
**Primary Identifier:** `customer_id`  
**Primary Measure:** `purchase_amount`  
**Key Engagement Field:** `previous_purchases`  
**Key Loyalty Field:** `subscription_status`  
**Key Promotional Field:** `discount_applied`