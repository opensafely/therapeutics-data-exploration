-- This query is for a data development project that must include T1OO data.
-- Consequently, this query doesn't reference the PatientsWithTypeOneDissent table.
SELECT DISTINCT CASIM05_risk_cohort as risk_group FROM therapeutics ORDER BY CASIM05_risk_cohort;
