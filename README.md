An end-to-end data analytics project using Python, SQL, ETL, and Power BI to identify high-value customer segments, product opportunities, subscription gaps, and promotion patterns to support data-driven retail decisions.

# Retail Customer Value & Commercial Analytics

## Project Overview

This project analyzes **3,900 retail customer purchase records** to help a retail business understand which customer segments, products, and purchasing behaviors are associated with higher sales value and stronger customer engagement.

The project follows an end-to-end analytics workflow:

**Raw Data → Python ETL → Data Validation → SQL → Business Analysis → Power BI → Insights → Recommendations**

Rather than focusing only on data cleaning or dashboard creation, the project is designed around real business questions and decisions related to:

* Customer value and purchase behavior
* Customer engagement and subscription opportunities
* Product and category performance
* Discount and promotion patterns
* Customer ratings and product experience
* Demographic and geographic differences

## Business Problem

The retailer has customer, product, purchase, demographic, subscription, discount, and rating information but lacks a structured view of **where its most valuable customer and product opportunities exist**.

The objective is to identify the customer segments and product behaviors associated with higher purchase value and use these insights to support more targeted **marketing, merchandising, loyalty, and promotional decisions**.

## Key Objectives

1. Identify high-value customer segments based on observed purchase behavior.
2. Determine which products and categories contribute most to purchase value.
3. Analyze the relationship between previous purchase behavior and current purchase value.
4. Identify subscription opportunities among highly engaged customers.
5. Evaluate discount usage patterns across customers, products, and categories.
6. Identify products that combine strong demand with comparatively weaker ratings.

## Tools & Technologies

* **Python** — Data profiling, ETL, validation, feature engineering and business analysis
* **SQL** — Data modeling and business analysis using aggregations, CTEs and window functions
* **Power BI** — KPI development, interactive dashboarding and business reporting
* **Pandas / NumPy / Matplotlib** — Data processing and visualization

## Key Deliverables

* Reproducible Python ETL pipeline
* Data-quality and validation framework
* Clean analytical dataset
* SQL analytical database
* Business-driven SQL analysis
* Python business-analysis notebook
* KPI framework
* Interactive Power BI dashboard
* Evidence-based business recommendations

## Important Analytical Limitations

The dataset does not contain transaction dates, order IDs, quantities, costs, margins, or complete historical transaction records. Therefore, this project does **not** claim to measure true customer retention, churn, customer lifetime value, profitability, monthly revenue growth, or causal promotion effectiveness.

`Previous Purchases` is treated as a **purchase-history engagement proxy**, and discount analysis is treated as **observational/associational analysis rather than causal analysis**.

## Business Value

The final analysis is designed to help stakeholders answer:

> **Who are our most valuable customer groups, which products and categories deserve attention, and where should customer engagement and promotional efforts be prioritized?**
