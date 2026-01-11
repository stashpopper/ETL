/* =========================================================
   BASIC DATA UNDERSTANDING
   ========================================================= */

-- 1. Total number of orders
SELECT COUNT(*) AS total_orders
FROM df_orders;


-- 2. Date range of the dataset
SELECT
    MIN(order_date) AS first_order,
    MAX(order_date) AS last_order
FROM df_orders;


-- 3. Total revenue and total profit
SELECT
    ROUND(SUM(sale_price), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM df_orders;


/* =========================================================
   PRODUCT & CATEGORY ANALYSIS
   ========================================================= */

-- 4. Top 10 revenue generating products
SELECT
    product_id,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;


-- 5. Revenue by category
SELECT
    category,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY category
ORDER BY revenue DESC;


-- 6. Revenue by sub-category
SELECT
    sub_category,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY sub_category
ORDER BY revenue DESC;


/* =========================================================
   REGION & CUSTOMER INSIGHTS
   ========================================================= */

-- 7. Revenue by region
SELECT
    region,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY region
ORDER BY revenue DESC;


-- 8. Average order value per region
SELECT
    region,
    ROUND(SUM(sale_price) / COUNT(*), 2) AS avg_order_value
FROM df_orders
GROUP BY region
ORDER BY avg_order_value DESC;


/* =========================================================
   TIME-BASED ANALYSIS
   ========================================================= */

-- 9. Monthly revenue trend (all years)
SELECT
    strftime('%Y-%m', order_date) AS year_month,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY year_month
ORDER BY year_month;


-- 10. Yearly revenue comparison
SELECT
    strftime('%Y', order_date) AS year,
    ROUND(SUM(sale_price), 2) AS revenue
FROM df_orders
GROUP BY year
ORDER BY year;


-- 11. Monthly sales comparison: 2022 vs 2023
SELECT
    strftime('%m', order_date) AS month,
    ROUND(SUM(CASE WHEN strftime('%Y', order_date) = '2022'
                   THEN sale_price ELSE 0 END), 2) AS sales_2022,
    ROUND(SUM(CASE WHEN strftime('%Y', order_date) = '2023'
                   THEN sale_price ELSE 0 END), 2) AS sales_2023
FROM df_orders
GROUP BY month
ORDER BY month;


/* =========================================================
   PROFITABILITY ANALYSIS
   ========================================================= */

-- 12. Most profitable categories
SELECT
    category,
    ROUND(SUM(profit), 2) AS total_profit
FROM df_orders
GROUP BY category
ORDER BY total_profit DESC;


-- 13. Profit margin by category
SELECT
    category,
    ROUND(SUM(profit) / SUM(sale_price) * 100, 2) AS profit_margin_percent
FROM df_orders
GROUP BY category
ORDER BY profit_margin_percent DESC;


-- 14. Sub-category with highest profit growth (2023 vs 2022)
SELECT
    sub_category,
    ROUND(SUM(CASE WHEN strftime('%Y', order_date) = '2022'
                   THEN profit ELSE 0 END), 2) AS profit_2022,
    ROUND(SUM(CASE WHEN strftime('%Y', order_date) = '2023'
                   THEN profit ELSE 0 END), 2) AS profit_2023,
    ROUND(
        SUM(CASE WHEN strftime('%Y', order_date) = '2023'
                 THEN profit ELSE 0 END)
      - SUM(CASE WHEN strftime('%Y', order_date) = '2022'
                 THEN profit ELSE 0 END),
        2
    ) AS profit_growth
FROM df_orders
GROUP BY sub_category
ORDER BY profit_growth DESC
LIMIT 1;


/* =========================================================
   OPERATIONAL INSIGHTS
   ========================================================= */

-- 15. Orders by shipping mode
SELECT
    ship_mode,
    COUNT(*) AS total_orders
FROM df_orders
GROUP BY ship_mode
ORDER BY total_orders DESC;


-- 16. Average discount impact (indirect via sale price)
SELECT
    category,
    ROUND(AVG(sale_price), 2) AS avg_selling_price
FROM df_orders
GROUP BY category
ORDER BY avg_selling_price DESC;
