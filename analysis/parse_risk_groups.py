import csv
import re
from pathlib import Path

# Allowed risk group list and extract method taken from cohort-extractor
# https://github.com/opensafely-core/cohort-extractor/blob/c28c7fee575d476c1abfab80e9af84dbfeea0d85/cohortextractor/therapeutics_utils.py
COHORTEXTRACTOR_ALLOWED_RISK_GROUPS = [
    "downs syndrome",
    "haematologic malignancy",
    "haematological diseases",
    "hiv or aids",
    "imid",
    "immune-mediated inflammatory disorders (imid)",
    "liver disease",
    "primary immune deficiencies",
    "rare neurological conditions",
    "renal disease",
    "sickle cell disease",
    "solid cancer",
    "solid organ recipients",
    "solid organ transplant recipients",
    "stem cell transplant recipients",
]


def extract_risk_groups_from_file(input_file):
    """
    Helper function to extract distinct risk groups from a file with one line
    per distinct risk group value extracted from the database

    (Note that this input file is expected to be generated manually, checked to ensure
    no disclosive free text data may be included, and used to ensure the following
    `ALLOWED_RISK_GROUPS` list is complete)
    """
    lines = Path(input_file).read_text().strip().split("\n")
    risk_groups = set()
    for line in lines:
        for group in line.split("and"):
            group = re.sub("Patients with a?", "", group)
            risk_groups.add(group.strip().lower())
    return sorted(risk_groups)


def parse_groups():
    risk_group_files = [
        "mol1_risk_group.csv", "casim05_risk_group.csv", "sot02_risk_group.csv"
    ]

    all_groups = set()
    for risk_group_file in risk_group_files:
        fp = Path("output") / risk_group_file
        risk_groups = extract_risk_groups_from_file(fp)
        all_groups = all_groups | set(risk_groups)

    print(sorted(all_groups))

    present_in_both = set(COHORTEXTRACTOR_ALLOWED_RISK_GROUPS) & all_groups
    cohortextractor_only = set(COHORTEXTRACTOR_ALLOWED_RISK_GROUPS) - all_groups
    current_only = all_groups - set(COHORTEXTRACTOR_ALLOWED_RISK_GROUPS)

    with (Path("output") / "risk_groups.csv").open("w") as output_file:
        writer = csv.DictWriter(output_file, ["current", "cohort_extractor"])
        writer.writeheader()
        writer.writerows(
            [
                {"current": risk_group, "cohort_extractor": risk_group}
                for risk_group in present_in_both
            ]
        )
        writer.writerows(
            [
                {"current": risk_group, "cohort_extractor": ""}
                for risk_group in current_only
            ]
        )
        writer.writerows(
            [
                {"current": "", "cohort_extractor": risk_group}
                for risk_group in cohortextractor_only
            ]
        )



if __name__ == "__main__":
    parse_groups()

