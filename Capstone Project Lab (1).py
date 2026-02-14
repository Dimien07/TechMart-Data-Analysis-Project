#!/usr/bin/env python
# coding: utf-8

# # Ungraded Lab: Capstone Project Lab

# ## 📋 Overview 
# Welcome to the Capstone Project Lab! In this comprehensive hands-on session, you'll apply all the SQL concepts you've learned throughout the course to analyze a complex dataset from TechMart, a growing retail chain. You'll clean data, write advanced queries, and produce a well-documented analysis report. This lab simulates real-world data analysis challenges, preparing you for your future career as a data scientist.
# 
# ## 🎯 Learning Outcomes
# By the end of this lab, you will be able to:
# - Clean and prepare complex datasets using SQL
# - Write advanced SQL queries involving subqueries, CTEs, and window functions
# - Perform comprehensive data analysis across multiple related tables
# - Leverage generative AI tools to optimize SQL queries and enhance performance
# - Produce a well-documented data analysis report
# 
# 
# ## 📚 Dataset Information
# You'll be working with the <b>TechMart</b> dataset, which contains information about a retail chain's operations across North America and Europe. The dataset includes:
# - <b>Employee_Records:</b> Information about employees, their roles, and sales performance
# - <b>Product_Details:</b> Details about products, including categories and inventory
# - <b>Customer_Demographics:</b> Customer information and loyalty program status
# - <b>Sales_Transactions:</b> Transaction data linking customers, products, and employees
# 

# ## 🖥️ Activities
# 
# ### Activity 1: Data Exploration and Cleaning 
# 
# Before diving into analysis, it's crucial to understand and clean our dataset. We'll start by examining each table and addressing any data quality issues.

# <b>Step 1:</b> Connect to the database, then load and display tables:

# In[20]:


import sqlite3
import pandas as pd

# Setting up the database. DO NOT edit the code given below
from techsmart_db_setup import setup_database
setup_database() 
conn = sqlite3.connect('techsmart.db')

# Load and display tables
tables = ['Employee_Records', 'Product_Details', 'Customer_Demographics', 'Sales_Transactions']
for table in tables:
    query = f"SELECT * FROM {table} LIMIT 100"
    df = pd.read_sql_query(query, conn)
    print(f"\n{table}:")
    display(df)


# <b>Step 2:</b> Identify and handle missing values:

# In[30]:


# Example for Employee_Records
query = """
SELECT COUNT(*) as total_rows,
       SUM(CASE WHEN sales_performance IS NULL OR sales_performance = 'nan' THEN 1 ELSE 0 END) as missing_sales_performance
FROM Employee_Records
"""
df = pd.read_sql_query(query, conn)
display(df)


# <b>Step 3: Try it yourself: </b>Write queries to identify missing values in other tables

# In[31]:


# Your turn: Write queries to identify missing values in other tables
query = """
SELECT 
    COUNT(*) AS total_rows,

    SUM(CASE 
            WHEN age IS NULL OR age = 'nan' 
            THEN 1 
            ELSE 0 
        END) AS missing_age,

    SUM(CASE 
            WHEN loyalty_program IS NULL OR loyalty_program = 'nan' 
            THEN 1 
            ELSE 0 
        END) AS missing_loyalty_program

FROM Customer_Demographics;
       

"""
df = pd.read_sql_query(query, conn)
display(df)


# <b>Step 4:</b> Clean inconsistent data formats:

# In[44]:


# Example: Standardize sales_performance in Employee_Records
query = """
UPDATE Employee_Records
SET sales_performance = CASE
    WHEN sales_performance = 'nan' THEN NULL
    WHEN sales_performance = 'five thousand' THEN '5000'
    ELSE sales_performance
END
"""
cursor = conn.cursor()
cursor.execute(query)
conn.commit()
display(df)


# **Step 5: Try it yourself:** Clean inconsistent data in other tables
# 

# In[49]:


# Your turn: Clean inconsistent data in other tables
query = """
UPDATE Product_Details
SET stock = CASE
    WHEN stock = 'nan' THEN NULL
    WHEN stock = 'five thousand' THEN '5000'
    ELSE stock
END
"""
cursor = conn.cursor()
cursor.execute(query)
conn.commit()
display(df)


# <b>💡 Tip:</b> Use CASE statements to handle multiple conditions when cleaning data.

# ### Activity 2: Advanced Data Analysis  
# 
# Now that our data is clean, let's perform some advanced analysis to gain insights into TechMart's operations.

# <b>Step 1:</b> Analyze employee performance by location:

# In[34]:


query = """
WITH emp_sales AS (
    SELECT store_location, 
           AVG(CAST(sales_performance AS FLOAT)) as avg_sales,
           COUNT(*) as employee_count
    FROM Employee_Records
    WHERE sales_performance IS NOT NULL
    GROUP BY store_location
)
SELECT store_location, avg_sales, employee_count,
       RANK() OVER (ORDER BY avg_sales DESC) as location_rank
FROM emp_sales
ORDER BY avg_sales DESC
"""
df = pd.read_sql_query(query, conn)
display(df)


# <b>Step 2:</b> Identify top-selling products by category:

# In[35]:


query = """
SELECT *
FROM (
    SELECT p.category,
           p.product_name,
           SUM(s.quantity) AS total_sold,
           RANK() OVER (
               PARTITION BY p.category
               ORDER BY SUM(s.quantity) DESC
           ) AS rank_in_category
    FROM Sales_Transactions s
    JOIN Product_Details p ON s.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
WHERE rank_in_category <= 3
ORDER BY category, total_sold DESC
"""
df = pd.read_sql_query(query, conn)
display(df)


#  <b>Step 3: Try it yourself</b>  Analyze customer purchasing behavior:

# In[52]:


# Your turn: Write a query to analyze customer purchasing behavior
# Hint: Join Customer_Demographics with Sales_Transactions and use window functions

query = """
SELECT 
    c.customer_id,
    c.loyalty_program,
    
    COUNT(s.transaction_id) AS total_transactions,
    SUM(s.total_amount) AS total_spent,
    AVG(s.total_amount) AS avg_purchase_value,

    RANK() OVER (ORDER BY SUM(s.total_amount) DESC) AS spending_rank,

    SUM(s.total_amount) OVER () AS overall_revenue,

    ROUND(
        SUM(s.total_amount) * 100.0 
        / SUM(SUM(s.total_amount)) OVER (), 
        2
    ) AS revenue_percentage

FROM Customer_Demographics c
LEFT JOIN Sales_Transactions s
    ON c.customer_id = s.customer_id

GROUP BY 
    c.customer_id,
    c.loyalty_program;

"""
df = pd.read_sql_query(query, conn)
display(df)


# ### Activity 3: Performance Optimization 
# As our dataset grows, query performance becomes crucial. Let's optimize some of our complex queries. The below query analyzes sales performance for Electronics and Accessories by summarizing transactions per employee, store, and customer loyalty status, while also computing total revenue per store-category pair for ranking and comparison.
# 

# <b>Step 1:</b> Identify slow-running queries:

# In[53]:


# Example: Time a complex query
import time

start_time = time.time()
query = """
WITH StoreSales AS (
   SELECT
       e.store_location,
       e.employee_id,
       e.role,
       p.category,
       c.loyalty_program,
       COUNT(s.transaction_id) AS total_sales,
       SUM(s.quantity) AS total_units_sold,
       SUM(s.total_amount) AS total_revenue
   FROM Sales_Transactions s
   JOIN Employee_Records e ON s.employee_id = e.employee_id
   JOIN Product_Details p ON s.product_id = p.product_id
   JOIN Customer_Demographics c ON s.customer_id = c.customer_id
   WHERE p.category IN ('Electronics', 'Accessories')
   GROUP BY e.store_location, e.employee_id, e.role, p.category, c.loyalty_program
),

StoreRankings AS (
   SELECT
       store_location,
       category,
       SUM(total_revenue) AS store_revenue
   FROM StoreSales
   GROUP BY store_location, category
)

SELECT
   ss.store_location,
   ss.employee_id,
   ss.role,
   ss.category,
   ss.loyalty_program,
   ss.total_sales,
   ss.total_units_sold,
   ss.total_revenue
FROM StoreSales ss
JOIN StoreRankings sr ON ss.store_location = sr.store_location AND ss.category = sr.category
ORDER BY ss.store_location, ss.total_revenue DESC;

"""


df = pd.read_sql_query(query, conn)
end_time = time.time()
print(f"Query execution time: {end_time - start_time} seconds")


# <b>Step 2:</b> Add an index to optimize your query:

# In[43]:


# Create an index
cursor.execute("CREATE INDEX idx_product_category ON Product_Details(category)")
conn.commit()


# <b>Step 3:</b> Use an AI to further optimize your query:

# Using an AI of your choice, further optimize your query then paste your updated query into the cell in Step 4.
# 

# **Step 4: Try it yourself:** Re-run your query and compare execution time

# In[54]:


# Your Turn: Run your optimized query and compare execution time

start_time = time.time()
query = """
WITH customer_sales AS (
    SELECT 
        c.customer_id,
        c.loyalty_program,
        COUNT(s.transaction_id) AS total_transactions,
        COALESCE(SUM(s.total_amount), 0) AS total_spent,
        COALESCE(AVG(s.total_amount), 0) AS avg_purchase_value
    FROM Customer_Demographics c
    LEFT JOIN Sales_Transactions s
        ON c.customer_id = s.customer_id
    GROUP BY 
        c.customer_id,
        c.loyalty_program
)

SELECT 
    customer_id,
    loyalty_program,
    total_transactions,
    total_spent,
    avg_purchase_value,
    RANK() OVER (ORDER BY total_spent DESC) AS spending_rank,
    SUM(total_spent) OVER () AS overall_revenue,
    ROUND(total_spent * 100.0 / SUM(total_spent) OVER (), 2) AS revenue_percentage
FROM customer_sales
ORDER BY spending_rank;

"""

df = pd.read_sql_query(query, conn)
end_time = time.time()
print(f"Query execution time: {end_time - start_time} seconds")


# <b>💡 Tip:</b> Indexes can significantly improve query performance, but they also have overhead. Use them judiciously.

# ### Activity 4: Generating the Analysis Report  
# 
# Now that we've performed our analysis, it's time to compile our findings into a comprehensive report.
# 
# <b>Step 1:</b> Summarize key findings:
# - List the top 3 insights from your analysis
# - Provide supporting data for each insight
# 
# <b>Step 2:</b> Include SQL queries:
# - For each key insight, provide the SQL query used
# 
# <b>Step 3:</b> Document your process:
# - Explain your data cleaning steps
# - Describe any challenges you encountered and how you overcame them
# - Discuss potential areas for further analysis

# #### Close the Connection
# It's good practice to close the database connection when you're done

# In[ ]:


# Close the database connection 
conn.close()


# ## ✅ Success Checklist
# - Cleaned and prepared all dataset tables
# - Performed at least 3 advanced SQL queries using subqueries, CTEs, or window functions
# - Optimized at least one complex query for better performance
# - Compiled a comprehensive analysis report with key insights and supporting data
# - Program runs without errors
# 
# ## 🔍 Common Issues & Solutions 
# 
# - Problem: Query returns no results 
#     - Solution: Double-check table and column names, and ensure your JOIN conditions are correct
# - Problem: Error "no such table" 
#      - Solution: Verify that you're connected to the correct database and that the table name is spelled correctly
# 
# ## ➡️ Summary
# In this comprehensive lab, you've applied advanced SQL concepts to analyze TechMart's retail operations data, working with multiple related tables covering employee records, product details, customer demographics, and sales transactions. You've gained hands-on experience in data cleaning, writing complex queries using subqueries, CTEs, and window functions, and optimizing query performance through indexing. Through this real-world simulation, you've developed the practical skills needed to conduct thorough data analysis and create well-documented reports, preparing you for actual data science roles.
# 
# 
# ### 🔑 Key Points
# - Data cleaning is crucial for accurate analysis
# - Advanced SQL techniques like CTEs and window functions enable complex analysis
# - Query optimization is essential for working with large datasets
# - Effective reporting is key to communicating insights
