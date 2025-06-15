-- Consulta custosa que usei pro JMETER
SELECT
    s.id AS satellite_id,
    s.version,
    s.velocity_kms,
    s.height_km,
    s.latitude,
    s.longitude,
    op.inclination,
    op.period,
    op.semimajor_axis,
    op.eccentricity,
    l.date_utc,
    r.name AS rocket_name,
    lp.region AS launch_region
FROM
    starlink_satellites s
JOIN orbital_parameters op ON op.starlink_id = s.id
JOIN launches l ON s.launch_id = l.id
JOIN rockets r ON l.rocket_id = r.id
JOIN launchpads lp ON l.launchpad_id = lp.id
WHERE
    s.decayed = FALSE
    AND s.velocity_kms BETWEEN 7.3 AND 7.9
    AND s.latitude BETWEEN -10 AND 10
    AND op.inclination BETWEEN 53.05 AND 53.06
    AND op.eccentricity BETWEEN 0.00017 AND 0.00018
    AND lp.region = 'Florida'
ORDER BY
    op.period DESC,
    s.height_km DESC