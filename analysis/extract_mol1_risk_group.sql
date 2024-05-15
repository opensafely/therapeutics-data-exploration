-- This query is for a data development project that must include T1OO data.
-- Consequently, this query doesn't reference the PatientsWithTypeOneDissent table.
SELECT DISTINCT MOL1_high_risk_cohort as risk_group FROM therapeutics ORDER BY MOL1_high_risk_cohort;
