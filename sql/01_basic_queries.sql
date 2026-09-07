-- ============================================
-- Industrial Maintenance Analytics
-- Basic SQL Queries
-- ============================================


-- 1. View all equipment
SELECT *
FROM equipment;


-- 2. View maintenance orders
SELECT *
FROM maintenance_orders;


-- 3. Count equipment
SELECT COUNT(*) AS total_equipment
FROM equipment;


-- 4. Count maintenance orders
SELECT COUNT(*) AS total_work_orders
FROM maintenance_orders;


-- 5. Count failures by equipment
SELECT
    equipment_id,
    COUNT(*) AS failure_count
FROM maintenance_orders
GROUP BY equipment_id
ORDER BY failure_count DESC;


-- 6. Total downtime by equipment
SELECT
    equipment_id,
    ROUND(SUM(downtime_hours), 2) AS total_downtime_hours
FROM maintenance_orders
GROUP BY equipment_id
ORDER BY total_downtime_hours DESC;


-- 7. Total maintenance cost by equipment
SELECT
    equipment_id,
    ROUND(SUM(total_cost), 2) AS total_maintenance_cost
FROM maintenance_orders
GROUP BY equipment_id
ORDER BY total_maintenance_cost DESC;