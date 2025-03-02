-- TODO: Esta consulta devolverá una tabla con las diferencias entre los tiempos
-- reales y estimados de entrega por mes y año. Tendrá varias columnas:
-- month_no, con los números de mes del 01 al 12; month, con las primeras 3 letras
-- de cada mes (ej. Ene, Feb); Year2016_real_time, con el tiempo promedio de
-- entrega real por mes de 2016 (NaN si no existe); Year2017_real_time, con el
-- tiempo promedio de entrega real por mes de 2017 (NaN si no existe);
-- Year2018_real_time, con el tiempo promedio de entrega real por mes de 2018
-- (NaN si no existe); Year2016_estimated_time, con el tiempo promedio estimado
-- de entrega por mes de 2016 (NaN si no existe); Year2017_estimated_time, con
-- el tiempo promedio estimado de entrega por mes de 2017 (NaN si no existe); y
-- Year2018_estimated_time, con el tiempo promedio estimado de entrega por mes
-- de 2018 (NaN si no existe).
-- PISTAS:
-- 1. Puedes usar la función julianday para convertir una fecha a un número.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Considera tomar order_id distintos.


SELECT
    strftime('%m', o.order_purchase_timestamp) AS month_no,
    CASE strftime('%m', o.order_purchase_timestamp)
        WHEN '01' THEN 'Jan'
        WHEN '02' THEN 'Feb'
        WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Apr'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul'
        WHEN '08' THEN 'Aug'
        WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct'
        WHEN '11' THEN 'Nov'
        WHEN '12' THEN 'Dec'
    END AS month,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2016' THEN julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2016_real_time,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' THEN julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2017_real_time,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2018' THEN julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2018_real_time,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2016' THEN julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2016_estimated_time,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' THEN julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2017_estimated_time,
    AVG(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2018' THEN julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp) ELSE NULL END) AS Year2018_estimated_time
FROM olist_orders o
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY month_no
ORDER BY month_no;
