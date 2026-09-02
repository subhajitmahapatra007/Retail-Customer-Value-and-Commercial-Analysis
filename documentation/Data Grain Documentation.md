# Data Grain Documentation

## 1. Purpose

Data grain defines the **level of detail represented by a single row** in the dataset.

Establishing the correct grain is critical because metrics such as customer count, purchase value, averages, rankings, and segmentation depend on understanding what each record represents.

---

## 2. Dataset Grain

The analytical grain of this dataset is:

> **One row represents one observed customer purchase record.**

The dataset contains 3,900 records and 3,900 customer IDs in the supplied data.

The `Customer ID` identifies the customer associated with the observed purchase record.

### Grain Definition

```text
1 Row
   =
1 Observed Customer Purchase Record
   =
1 Customer ID in the supplied dataset
```

---

## 3. Important Clarification: Customer ID ≠ Order ID

Although `Customer ID` is unique in the supplied dataset, it should **not** be interpreted as an Order ID.

The dataset does not contain a dedicated:

```text
Order ID
Transaction ID
Purchase Date
Transaction Date
```

Therefore, this project should not make assumptions that every `Customer ID` represents a real-world order number.

Instead, `Customer ID` is treated as the identifier of the customer associated with the observed purchase record.

---

## 4. What One Record Contains

Each record combines information about several aspects of the customer's observed purchase behavior.

### Customer Attributes

```text
Customer ID
Age
Gender
Location
```

### Purchase Attributes

```text
Item Purchased
Category
Purchase Amount (USD)
Size
Color
Season
```

### Customer Experience

```text
Review Rating
```

### Loyalty / Engagement

```text
Subscription Status
Previous Purchases
Frequency of Purchases
```

### Commercial / Promotional Information

```text
Discount Applied
Promo Code Used
```

### Fulfillment / Payment

```text
Shipping Type
Payment Method
```

---

## 5. Grain Diagram

The dataset can conceptually be represented as:

```text
                    CUSTOMER
                       │
                       │
                 Customer ID
                       │
                       ▼
             OBSERVED PURCHASE RECORD
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
     Product        Purchase       Customer
    Information       Value        Behavior
        │              │              │
        ▼              ▼              ▼
      Item          Amount       Subscription
     Category                     Previous Purchases
      Size                        Frequency
      Color
      Season
```

Each row combines these attributes for one observed purchase record.

---

## 6. Primary Identifier

### `customer_id`

`customer_id` is used as the primary identifier of the analytical record because the supplied dataset contains one observed record per customer ID.

Before loading the data into SQL, the ETL pipeline should validate:

```text
customer_id IS NOT NULL
customer_id IS UNIQUE
customer_id IS VALID
```

If duplicate customer IDs are discovered during future data updates, the grain must be reassessed before continuing with analysis.

---

## 7. Measures at This Grain

The following fields can be treated as measures or quantitative attributes at the record level.

| Field | Role | Interpretation |
|---|---|---|
| `purchase_amount` | Measure | Purchase value associated with the observed record |
| `review_rating` | Measure | Customer rating associated with the purchase |
| `previous_purchases` | Measure | Number of previous purchases reported for the customer |
| `age` | Attribute/Measure | Customer age |

### Important

`previous_purchases` represents a **count of previous purchases**, not the actual historical purchase transactions.

Therefore:

```text
previous_purchases = 25
```

does **not** mean that 25 historical transaction records are available in the dataset.

---

## 8. Fields That Should Not Be Treated as Measures

Several fields represent categories or descriptive attributes rather than numerical measures.

Examples include:

```text
gender
item_purchased
category
location
size
color
season
subscription_status
shipping_type
discount_applied
promo_code_used
payment_method
frequency_of_purchases
```

These fields should primarily be used for:

- Segmentation
- Grouping
- Filtering
- Comparison
- Dimension analysis

---

## 9. Aggregation Rules

Because the dataset is at the observed purchase-record level, aggregation should be performed carefully.

### Total Purchase Value

The total purchase value can be calculated as:

```text
SUM(purchase_amount)
```

This represents the total purchase value represented by the available records.

---

### Average Purchase Value

Average purchase value can be calculated as:

```text
AVG(purchase_amount)
```

This represents the average purchase value per observed record.

---

### Customer Count

If `customer_id` is unique:

```text
COUNT(DISTINCT customer_id)
```

can be used to represent the number of unique customers represented in the dataset.

---

### Previous Purchases

`previous_purchases` should generally be aggregated using measures such as:

```text
AVG(previous_purchases)
MIN(previous_purchases)
MAX(previous_purchases)
```

It should **not** normally be summed to represent the number of historical purchases across the business.

For example:

```text
SUM(previous_purchases)
```

would represent the sum of the reported historical-purchase counts across customers, not the number of historical transactions contained in the dataset.

---

## 10. Customer Segmentation Grain

Customer segmentation in this project is based on the available customer-level attributes.

Two important dimensions are:

### Current Purchase Value

Derived from:

```text
purchase_amount
```

### Purchase-History Engagement Proxy

Derived from:

```text
previous_purchases
```

This allows the project to create a business-oriented matrix such as:

```text
                    CURRENT PURCHASE VALUE
                  Low                High
              ┌───────────────┬───────────────┐
High          │               │               │
ENGAGEMENT    │ Developing /  │ High-Value &  │
              │ Repeat        │ Engaged       │
              ├───────────────┼───────────────┤
Low           │               │               │
ENGAGEMENT    │ Low Value     │ High Potential│
              │               │               │
              └───────────────┴───────────────┘
```

The actual thresholds for these segments should be determined from the observed data distribution rather than arbitrarily assumed.

---

## 11. Business Questions Supported by This Grain

The current grain supports questions such as:

### Customer Value

- Which customer segments have the highest purchase value?
- What is the average purchase value by customer segment?
- How does previous purchase behavior relate to current purchase value?

### Product Performance

- Which categories generate the highest purchase value?
- Which products contribute most to purchase value?
- Which products have high purchase value but weaker ratings?

### Subscription

- What percentage of customers are subscribers?
- Are highly engaged customers more likely to subscribe?
- Which customer segments contain many high-engagement non-subscribers?

### Promotion

- What percentage of observed records involve discounts?
- How does purchase value differ between discount and non-discount records?
- Which categories have higher discount usage?

### Customer Behavior

- How does purchase behavior differ across age groups?
- Which purchase-frequency groups have higher purchase values?
- Which payment and shipping methods are most commonly used?

---

## 12. Business Questions NOT Supported by This Grain

The dataset cannot reliably answer questions requiring transaction history or time-series information.

### Customer Retention

Cannot reliably calculate:

```text
Retention Rate
Customer Churn
Cohort Retention
Customer Tenure
```

because historical transaction dates and customer activity timelines are unavailable.

---

### Revenue Trends

Cannot reliably calculate:

```text
Monthly Revenue
Weekly Revenue
Monthly Growth
Year-over-Year Growth
Revenue Trend
```

because there is no transaction date.

---

### True Customer Lifetime Value

A true CLV calculation would require information such as:

```text
Customer Revenue Over Time
Purchase Frequency Over Time
Customer Tenure
Margin / Profitability
```

These are not available at the required level of detail.

---

### Profitability

The dataset contains purchase value but does not contain:

```text
Product Cost
COGS
Gross Margin
Operating Cost
Profit
```

Therefore, purchase value must not be presented as profit.

---

## 13. Season Is Not a Time Dimension

The `Season` field contains categorical values such as:

```text
Spring
Summer
Fall
Winter
```

It can be used to compare customer behavior across seasons.

However, it should **not** be treated as a chronological time dimension.

For example:

```text
Spring → Summer → Fall → Winter
```

does not provide actual transaction chronology.

Therefore, seasonal analysis should be presented as:

> **Comparison across seasonal categories**

rather than:

> **Time-series trend analysis**

---

## 14. Discount Analysis at This Grain

The dataset allows comparison between records with and without discounts.

For example:

```text
Average Purchase Value
        │
        ├── Discount Applied
        │
        └── No Discount
```

However, this analysis is **observational**.

A difference in purchase value between discounted and non-discounted records does not prove that the discount caused the difference.

Other factors may influence the result, including:

- Product category
- Customer characteristics
- Purchase frequency
- Subscription status
- Season
- Product selection

Therefore, conclusions should use language such as:

> "Discounted purchases were associated with..."

rather than:

> "Discounts increased..."

unless a proper causal experiment is available.

---

## 15. Power BI Modeling Implication

For the initial version of this project, a simple analytical table is sufficient because:

- The dataset contains only 3,900 records.
- The dataset has a single primary analytical grain.
- There is no transaction history.
- There is no need to artificially create multiple fact tables.

The cleaned analytical table can therefore serve as the primary Power BI fact-like table.

A more complex star schema should only be introduced if it provides a clear analytical or modeling benefit.

---

## 16. SQL Modeling Implication

The initial SQL table can be designed around the same grain:

```text
customer_purchase_behavior
```

Conceptually:

```text
customer_purchase_behavior
────────────────────────────────────────
customer_id              PRIMARY KEY
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
subscription_status
shipping_type
discount_applied
previous_purchases
payment_method
frequency_of_purchases
...
```

Business-derived fields may also be added during the ETL process.

---

## 17. Grain Validation Checklist

The ETL pipeline should validate the following before analytical use:

```text
☐ One row represents one observed customer purchase record
☐ customer_id is not null
☐ customer_id is unique
☐ purchase_amount is numeric
☐ purchase_amount is positive
☐ previous_purchases is numeric
☐ review_rating is within the expected range
☐ Categorical values are standardized
☐ No unexpected duplicate records remain
☐ No date-based analysis is performed
☐ Customer ID is not treated as Order ID
☐ Previous purchases are not treated as historical transaction records
```

---

## 18. Final Grain Statement

For this project, the official grain statement is:

> **The dataset is analyzed at the level of one observed customer purchase record per Customer ID. Each record contains customer attributes, product information, purchase value, customer engagement indicators, promotional information, fulfillment preferences, and payment behavior.**

This grain definition should remain consistent across:

```text
Python
    ↓
ETL
    ↓
SQL
    ↓
Power BI
```

Any future change to the dataset structure should trigger a new grain assessment before modifying the analytical model.

---

**Documentation Status:** Complete  
**Primary Grain:** One observed customer purchase record  
**Primary Identifier:** `customer_id`  
**Historical Transaction Data:** Not available  
**Time-Series Analysis:** Not supported