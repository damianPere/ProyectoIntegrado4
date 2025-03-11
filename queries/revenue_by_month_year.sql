-- TODO: Esta consulta devolverá una tabla con los ingresos por mes y año.
-- Tendrá varias columnas: month_no, con los números de mes del 01 al 12;
-- month, con las primeras 3 letras de cada mes (ej. Ene, Feb);
-- Year2016, con los ingresos por mes de 2016 (0.00 si no existe);
-- Year2017, con los ingresos por mes de 2017 (0.00 si no existe); y
-- Year2018, con los ingresos por mes de 2018 (0.00 si no existe).

WITH RECURSIVE month_numbers AS (
  SELECT '01' AS month_no
  UNION ALL
  SELECT PRINTF('%02d', CAST(month_no AS INTEGER) + 1)
  FROM month_numbers
  WHERE month_no < '12'
),
monthly_payments AS (
  SELECT
    customer_id,
    o.order_id,
    order_delivered_customer_date,
    order_status,
    strftime('%m', o.order_delivered_customer_date) AS delivery_month,
    strftime('%Y', o.order_delivered_customer_date) AS delivery_year,
    p.payment_value AS total_payment
  FROM olist_orders o
  JOIN olist_order_payments p ON o.order_id = p.order_id
  WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
  GROUP BY customer_id, o.order_id, order_delivered_customer_date,
           delivery_month, delivery_year
  ORDER BY order_delivered_customer_date ASC
),
yearly_monthly_totals AS (
  SELECT
    delivery_month,
    delivery_year,
    SUM(total_payment) AS total_payment
  FROM monthly_payments
  GROUP BY delivery_month, delivery_year
)
SELECT
    mn.month_no,
    CASE mn.month_no
        WHEN '01' THEN 'Ene'
        WHEN '02' THEN 'Feb'
        WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Abr'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul'
        WHEN '08' THEN 'Ago'
        WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct'
        WHEN '11' THEN 'Nov'
        WHEN '12' THEN 'Dic'
    END AS month,
    printf('%.2f', COALESCE(SUM(CASE WHEN ymt.delivery_year = '2016' THEN ymt.total_payment ELSE 0 END), 0.0)) AS Year2016,
    printf('%.2f', COALESCE(SUM(CASE WHEN ymt.delivery_year = '2017' THEN ymt.total_payment ELSE 0 END), 0.0)) AS Year2017,
    printf('%.2f', COALESCE(SUM(CASE WHEN ymt.delivery_year = '2018' THEN ymt.total_payment ELSE 0 END), 0.0)) AS Year2018
FROM
    month_numbers mn
LEFT JOIN yearly_monthly_totals ymt ON ymt.delivery_month = mn.month_no
GROUP BY
    mn.month_no
ORDER BY
    mn.month_no;
