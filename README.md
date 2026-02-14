# TechMart-Data-Analysis-Project
This project analyzes customer purchasing behavior, employee performance, and top-selling products for TechMart, a retail chain operating across North America and Europe. Using SQL and Python, I cleaned, explored, and analyzed data to generate actionable business insights.
Dataset Overview

The dataset contains four main tables:

Employee_Records – Information about employees, their roles, and sales performance.

Product_Details – Details about products, including categories and inventory.

Customer_Demographics – Customer information and loyalty program status.

Sales_Transactions – Transaction data linking customers, products, and employees.

Project Overview – What I Did

Cleaned and prepared complex datasets by handling missing values and converting inconsistent entries to proper numeric types.

Explored customer purchasing behavior, aggregating transactions and calculating total spending, average purchase value, and transaction counts.

Used advanced SQL techniques including CTEs, subqueries, window functions, and joins to rank customers and compute revenue contributions.

Compared loyalty program members vs non-members to identify patterns in spending and frequency.

Analyzed employee performance by location and top-selling products by category.

Identified slow-running queries and applied optimization techniques for faster execution.

Compiled insights into a concise report highlighting key trends and actionable recommendations.

Key Insights
1. Employee Performance by Location

Observation: Chicago ranks #1 in average sales per employee because each employee generates more revenue on average than in other locations.

Interpretation: Although Phoenix and New York have more employees, the average per-person contribution is lower. This highlights Chicago’s high per-capita productivity, likely driven by employee efficiency, store management, or high-demand customers.

2. Top-Selling Products by Category

Observation: A few items dominate sales in each category.

Example: Accessories → Keyboard (156 units), Charger (123 units), Speaker (85 units); Electronics → Tablet (134 units), Mouse (129 units), Headphones (110 units).

Actionable Insight: Insights can inform inventory management, marketing strategies, and promotional campaigns to maximize revenue.

3. Customer Purchasing Behavior

Observation: A small number of customers drive the majority of revenue, following the Pareto principle.

Patterns: Loyalty program members tend to spend more and purchase more frequently. Customers exhibit two main behaviors:

Frequent, low-value purchases

Infrequent, high-value purchases

Opportunity: Inactive customers (zero transactions) represent untapped potential for targeted marketing campaigns.

Slow-Running Queries and Optimization

Some queries were initially slow due to large joins and aggregations on Sales_Transactions and Product_Details.

Optimization Techniques Applied:

Used CTEs to simplify complex queries.

Leveraged window functions (RANK() OVER(), SUM(...) OVER()) for efficient ranking and percentage calculations.

Ensured joins were performed on indexed columns (customer_id, product_id, employee_id).

Pre-aggregated values to avoid redundant calculations.

Result: Significantly improved query performance while maintaining accurate results.

Conclusion / Next Steps

Segment customers using RFM (Recency, Frequency, Monetary value) analysis.

Analyze product-level sales trends and seasonal patterns.

Investigate drivers of high employee performance by location.

Predict customer churn and design retention strategies.
