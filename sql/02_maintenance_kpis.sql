-- ============================================
-- Industrial Maintenance Analytics
-- Maintenance KPI Analysis
-- ============================================

WITH maintenance_summary AS (
    SELECT
        equipment_id,
        COUNT(work_order_id) AS failure_count,
        SUM(downtime_hours) AS corrective_downtime,
        SUM(total_cost) AS total_maintenance_cost
    FROM maintenance_orders
    GROUP BY equipment_id
),

operating_summary AS (
    SELECT
        equipment_id,
        SUM(planned_hours) AS planned_hours,
        SUM(operating_hours) AS operating_hours
    FROM operating_history
    GROUP BY equipment_id
)

SELECT
    e.equipment_id,
    e.equipment_name,
    e.area,
    e.criticality,
    m.failure_count,

    ROUND(
        o.operating_hours / o.planned_hours * 100,
        2
    ) AS availability_pct,

    ROUND(
        o.operating_hours / m.failure_count,
        2
    ) AS mtbf_hours,

    ROUND(
        m.corrective_downtime / m.failure_count,
        2
    ) AS mttr_hours,

    ROUND(
        m.corrective_downtime,
        2
    ) AS corrective_downtime,

    ROUND(
        m.total_maintenance_cost,
        2
    ) AS total_maintenance_cost

FROM equipment AS e

LEFT JOIN maintenance_summary AS m
    ON e.equipment_id = m.equipment_id

LEFT JOIN operating_summary AS o
    ON e.equipment_id = o.equipment_id

ORDER BY availability_pct ASC;