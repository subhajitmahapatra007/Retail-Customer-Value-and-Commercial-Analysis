# Assumptions & Limitations

## 1. Purpose

This document defines the assumptions, analytical boundaries, and limitations associated with the **Retail Customer Value & Commercial Analytics** project.

The purpose is to ensure that business conclusions are based only on information supported by the available dataset.

These assumptions should be considered when interpreting Python analysis, SQL results, ETL outputs, and Power BI dashboards.

---

# 2. Core Dataset Assumptions

## 2.1 Purchase Amount Represents Observed Purchase Value

The `purchase_amount` field is treated as the monetary value associated with the observed customer purchase record.

It is used to analyze:

- Purchase value
- Average purchase value
- Customer value
- Product contribution
- Category contribution
- Purchase-value segmentation

### Important

Purchase value is **not equivalent to profit or revenue recognized under a financial accounting definition** because the dataset does not provide sufficient financial information to establish those measures.

---

## 2.2 Customer ID Is the Record Identifier

`customer_id` is treated as the identifier for the customer associated with each observed record.

The supplied dataset appears to contain one record per Customer ID.

However, `customer_id` is **not treated as an Order ID or Transaction ID** because no dedicated order or transaction identifier is available.

---

## 2.3 One Row Represents One Observed Customer Purchase Record

The project assumes the analytical grain is:

> **One row = one observed customer purchase record.**

This assumption is used consistently across:

```text
Python
ETL
SQL
Power BI
```

Any future dataset containing multiple records per customer would require the grain and analytical model to be reassessed.

---

## 2.4 Previous Purchases Is a Historical Count

`previous_purchases` is interpreted as the reported number of previous purchases associated with the customer.

It is **not treated as historical transaction-level data**.

For example:

```text
previous_purchases = 30
```

means the customer has a reported previous-purchase count of 30.

It does not provide the dates, amounts, products, or details of those 30 previous purchases.

---

## 2.5 Season Is a Categorical Attribute

`season` is treated as a categorical business dimension.

It can be used to compare:

- Purchase value
- Customer behavior
- Product categories
- Discount usage
- Ratings

across seasons.

However, it is **not treated as a chronological time dimension**.

---

# 3. Data Quality Assumptions

## 3.1 Missing Review Ratings

The raw dataset contains missing values in `review_rating`.

Missing ratings are not interpreted as zero.

The ETL process will apply a documented imputation method and create an indicator:

```text
rating_was_imputed
```

This allows the analysis to distinguish between:

- Original ratings
- Imputed ratings

---

## 3.2 Duplicate Records

Duplicate records will be checked during the data-quality process.

Two types of duplicates will be considered:

### Full-Row Duplicates

Records where all available fields are identical.

### Identifier Duplicates

Records where the same `customer_id` appears more than once.

Duplicates will not be removed blindly.

Any duplicate identifier must first be investigated because duplicate IDs could indicate either:

- Legitimate multiple records
- Data-quality problems
- A change in dataset grain

---

## 3.3 Categorical Values

Categorical fields will be standardized during ETL.

Examples include:

```text
Gender
Category
Season
Subscription Status
Shipping Type
Discount Applied
Payment Method
Frequency of Purchases
```

The transformation process will:

- Remove unnecessary whitespace
- Standardize capitalization
- Normalize Yes/No values
- Detect unexpected categories

Unexpected values should be flagged rather than silently removed.

---

# 4. Promotional Analysis Assumptions

## 4.1 Discount Applied

`discount_applied` indicates whether a discount was associated with the observed purchase record.

It does not provide:

- Discount amount
- Discount percentage
- Original price
- Final discounted price
- Promotion cost

Therefore, analysis is limited to discount **usage patterns and associations**.

---

## 4.2 Promo Code Used

`promo_code_used` is retained in the raw data for traceability.

The supplied dataset shows effectively equivalent information between:

```text
discount_applied
promo_code_used
```

This relationship should be verified programmatically during ETL.

If confirmed, `discount_applied` will be used as the primary analytical field to avoid redundant information.

---

## 4.3 Discount Analysis Is Observational

A comparison such as:

```text
Average Purchase Value
        │
        ├── Discount Applied
        │
        └── No Discount
```

can identify an association.

It cannot prove that the discount itself caused the difference.

For example, higher purchase values among discounted purchases could be related to:

- Product mix
- Customer segment
- Subscription status
- Season
- Purchase frequency
- Other unobserved factors

Therefore, the project will avoid causal statements such as:

> "Discounts increased purchase value."

unless experimental or causal evidence is available.

Preferred interpretation:

> "Discounted purchases were associated with higher/lower purchase values in the observed dataset."

---

# 5. Customer Segmentation Assumptions

## 5.1 Purchase Value

`purchase_amount` is used as the primary measure of current observed purchase value.

Customers may be categorized into value bands such as:

```text
Low Value
Medium Value
High Value
```

The thresholds should be determined from the actual dataset distribution.

---

## 5.2 Engagement

`previous_purchases` is used as a **purchase-history engagement proxy**.

It does not directly measure:

- Customer loyalty
- Customer satisfaction
- Customer lifetime value
- Retention
- Churn probability

Therefore, terminology such as:

> "Purchase-history engagement"

is preferred over claiming that the field directly measures customer loyalty.

---

## 5.3 Business Segments

Customer segments should be designed around business usefulness rather than applying machine learning simply because it is available.

A possible framework is:

```text
                  CURRENT PURCHASE VALUE

                Low                    High
          ┌──────────────────┬──────────────────┐
High      │ Repeat /         │ High-Value &     │
Engagement│ Developing       │ Engaged          │
          ├──────────────────┼──────────────────┤
Low       │ Low Value        │ High Potential   │
Engagement│                  │                  │
          └──────────────────┴──────────────────┘
```

The final segment thresholds must be validated using the actual data distribution.

---

# 6. Financial Limitations

The dataset does not contain enough information to calculate true profitability.

The following fields are unavailable:

```text
Product Cost
Cost of Goods Sold
Gross Margin
Operating Cost
Profit
Shipping Cost
Marketing Cost
Promotion Cost
```

Therefore:

> **Purchase value must not be presented as profit.**

---

# 7. Customer Lifetime Value Limitation

A true Customer Lifetime Value calculation requires information about customer behavior over time.

This dataset does not contain sufficient historical transaction information.

Missing information includes:

- Customer acquisition date
- Transaction dates
- Historical transaction values
- Customer tenure
- Historical purchase frequency over time
- Profit margin

Therefore, the project will not calculate **true Customer Lifetime Value (CLV)**.

Instead, the project may use:

> **Observed Purchase Value**

and:

> **Purchase-History Engagement Proxy**

as separate analytical concepts.

---

# 8. Retention & Churn Limitations

The dataset cannot reliably calculate:

```text
Customer Retention Rate
Customer Churn Rate
Repeat Purchase Rate
Cohort Retention
Customer Tenure
Reactivation Rate
```

The primary reason is the absence of transaction dates and complete customer transaction history.

`previous_purchases` alone is not sufficient to calculate these metrics.

---

# 9. Time-Series Limitations

The dataset contains no:

```text
Order Date
Purchase Date
Transaction Date
Month
Quarter
Year
```

Therefore, the project cannot reliably calculate:

```text
Monthly Sales
Weekly Sales
Year-over-Year Growth
Month-over-Month Growth
Revenue Trend
Sales Forecasting
Seasonal Time-Series Forecast
```

The `season` field can only be used for categorical comparison.

---

# 10. Product & Inventory Limitations

The dataset provides information about products and categories but does not provide inventory information.

Unavailable fields include:

```text
Opening Inventory
Closing Inventory
Stock Level
Units Sold
Units Available
Reorder Point
Lead Time
Stockout Events
```

Therefore, the project cannot reliably answer:

- Which products are close to stockout?
- Which products need replenishment?
- What is inventory turnover?
- What is the optimal reorder quantity?
- Which products have the highest unit sales?

The project can instead focus on **purchase-value contribution and product demand patterns represented by the available records**.

---

# 11. Promotion ROI Limitation

The dataset identifies whether a discount was applied but does not provide the financial cost of the promotion.

Unavailable information includes:

```text
Discount Amount
Promotion Cost
Campaign Cost
Incremental Sales
Baseline Sales
Profit Margin
```

Therefore, the project cannot calculate:

```text
Promotion ROI
Incremental Revenue
Incremental Profit
Customer Acquisition Cost
Return on Promotional Spend
```

---

# 12. Causal Inference Limitation

The project is primarily based on observational data.

Therefore, relationships discovered during analysis should not automatically be interpreted as causal relationships.

For example:

```text
Discount → Purchase Value
Subscription → Higher Spending
Rating → Purchase Behavior
Previous Purchases → Current Purchase Value
```

may show statistical association without establishing causality.

The analysis should use language such as:

- "associated with"
- "correlated with"
- "observed among"
- "higher/lower in the dataset"

rather than:

- "caused"
- "resulted in"
- "increased because of"

unless causal evidence exists.

---

# 13. Statistical Analysis Limitations

Statistical tests may be used where appropriate to investigate relationships between variables.

However, statistical significance should not automatically be interpreted as business significance.

Where statistical analysis is performed, the project should consider:

- Effect size
- Sample size
- Practical business impact
- Distribution assumptions
- Potential confounding variables

Statistical results should support business reasoning rather than replace it.

---

# 14. Predictive Analytics Limitations

The dataset can support limited predictive experimentation, but it is not a naturally structured time-series or longitudinal dataset.

Potential predictive tasks may include:

```text
Purchase Value Classification
High-Value Customer Classification
Subscription Status Classification
```

However, model performance should be evaluated carefully.

The project should not claim that the dataset supports reliable:

```text
Sales Forecasting
Customer Churn Prediction
Long-Term Customer Lifetime Prediction
Demand Forecasting Over Time
```

because the required temporal information is unavailable.

---

# 15. Machine Learning Limitation

Machine learning should only be introduced if it answers a meaningful business question.

The project is primarily a:

> **Business Analytics and Decision Support project**

rather than an ML modeling project.

Therefore, ML should not be added simply to increase technical complexity.

If a predictive model is developed, it should clearly explain:

1. Business problem
2. Target variable
3. Available features
4. Data limitations
5. Model evaluation
6. Business interpretation
7. Deployment/use-case implications

---

# 16. Geographic Analysis Limitations

`location` can be used to compare customer and purchase-value patterns across locations.

However, the dataset does not provide:

```text
Population
Store Count
Market Size
Regional Marketing Spend
Household Income
Competitor Presence
```

Therefore, a location with higher purchase value should not automatically be interpreted as having higher market potential.

Geographic findings should be described as:

> "Higher observed purchase contribution in the dataset."

---

# 17. Rating Analysis Limitations

`review_rating` can be used to compare customer experience across products and categories.

However, ratings may be missing for some records.

Additionally, a rating does not necessarily explain the reason behind customer satisfaction or dissatisfaction.

Therefore, a low rating should be treated as an **indicator requiring investigation**, not proof of a specific product problem.

---

# 18. Recommended Analytical Language

To maintain analytical integrity, the following terminology should be preferred.

| Avoid | Prefer |
|---|---|
| Profit | Purchase Value |
| Order ID | Customer ID / Record Identifier |
| Customer Loyalty | Purchase-History Engagement Proxy |
| Customer Lifetime Value | Observed Purchase Value |
| Retention | Not measurable from available data |
| Churn | Not measurable from available data |
| Discount Impact | Discount Association |
| Seasonal Trend | Seasonal Comparison |
| Revenue Growth | Not measurable without dates |
| Historical Transactions | Reported Previous Purchase Count |

---

# 19. Explicitly Out of Scope

The following analyses are outside the reliable scope of this project:

```text
❌ True Customer Lifetime Value
❌ Customer Churn Prediction
❌ Retention Rate
❌ Cohort Analysis
❌ Monthly / Weekly Revenue Trends
❌ Year-over-Year Growth
❌ Profit Analysis
❌ Gross Margin Analysis
❌ Inventory Turnover
❌ Units Sold
❌ Average Units per Order
❌ Customer Tenure
❌ Discount ROI
❌ Promotion ROI
❌ Causal Promotion Effectiveness
❌ Long-Term Sales Forecasting
❌ Historical Transaction-Level Analysis
```

Explicitly excluding unsupported analyses strengthens the credibility of the project.

---

# 20. Analytical Scope

The project will focus on business questions that are directly supported by the available data.

### Customer Value

- Which customer groups have higher observed purchase values?
- Which customers show stronger purchase-history engagement?
- Where are high-engagement customers who are not subscribed?

### Product Performance

- Which categories contribute the most purchase value?
- Which products contribute the most purchase value?
- Which products have high purchase value but relatively weak ratings?

### Subscription

- What is the subscription penetration?
- How does purchase behavior differ between subscribers and non-subscribers?
- Which engaged customer groups represent potential subscription opportunities?

### Promotion

- How widely are discounts used?
- Which customer groups and categories have higher discount usage?
- How does observed purchase value differ between discounted and non-discounted records?

### Customer Behavior

- Which purchase-frequency groups show higher purchase values?
- How does behavior differ across demographic groups?
- Which payment and shipping preferences are most common?

---

# 21. Business Interpretation Framework

All major findings should follow this framework:

```text
Finding
   ↓
Evidence
   ↓
Interpretation
   ↓
Business Hypothesis
   ↓
Recommendation
   ↓
Expected Business Impact
```

### Example Structure

```text
Finding:
A particular customer segment has higher observed purchase value.

Evidence:
The segment has a higher average purchase amount than other segments.

Interpretation:
This segment represents a relatively higher-value customer group.

Business Hypothesis:
The segment may warrant greater loyalty and personalized marketing attention.

Recommendation:
Prioritize targeted engagement and subscription campaigns for this segment.

Expected Impact:
Potential improvement in customer engagement and commercial value.
```

The actual finding must always come from the analyzed dataset.

No business result should be invented before analysis.

---

# 22. Data Governance Principle

The project follows a simple principle:

> **Do not claim what the data cannot support.**

Every KPI, visualization, SQL query, statistical test, and business recommendation should be traceable to:

1. A dataset field
2. A documented transformation
3. A defined business question
4. A valid analytical method

---

# 23. Final Limitations Statement

This project analyzes customer shopping behavior using a cross-sectional dataset containing customer attributes, observed purchase value, product information, purchase-history counts, subscription status, discount indicators, ratings, and behavioral preferences.

The dataset is suitable for **descriptive and diagnostic commercial analytics**, including customer segmentation, product/category performance, subscription analysis, purchase-value analysis, and promotional behavior analysis.

However, the absence of transaction dates, order IDs, detailed historical transactions, cost data, margin data, quantity data, and promotion-cost information limits the ability to perform reliable retention, churn, true CLV, profitability, time-series, inventory, and causal promotion analyses.

Consequently, all business recommendations in this project will be presented as **data-informed recommendations based on observed patterns**, rather than causal or predictive claims beyond what the data supports.

---

## Documentation Status

| Area | Status |
|---|---|
| Dataset Assumptions | Documented |
| Data Quality Assumptions | Documented |
| Grain Assumptions | Documented |
| Customer Segmentation Limitations | Documented |
| Financial Limitations | Documented |
| Time-Series Limitations | Documented |
| Promotion Limitations | Documented |
| ML Limitations | Documented |
| Out-of-Scope Analysis | Documented |
| Business Interpretation Framework | Documented |

---

**Project Principle:**

> **Use the data to support decisions—not to manufacture conclusions.**