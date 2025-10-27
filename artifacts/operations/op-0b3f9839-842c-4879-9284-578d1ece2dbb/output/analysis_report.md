# Recruitment Workbook Analysis (op-0b3f9839-842c-4879-9284-578d1ece2dbb)

## Workbook Overview
- Sheets detected: Instructions, Donnees medecins, Donnees visites, Dashboard
- Instructions sheet spans 22 rows (textual guidance only)
- Doctors records: 197 rows, Visits records: 624 rows

## Doctors Dataset (Donnees medecins)
- Attitude mix: {'Neutre': 74, 'Prescripteur': 62, 'Detracteur': 60, 'Non_renseigne': 1}
- Region split: {'Nord': 99, 'Sud': 96, 'DOM_TOM': 1, 'Non_renseigne': 1}
- Missing counts: {'Identifiant': 0, 'Civilite': 0, 'Nom': 0, 'Prenom': 0, 'Specialite_1': 53, 'Specialite_2': 116, 'Etablissement': 0, 'ARS': 0, 'Secteur': 0, 'Region': 0, 'Nbr_patients_potentiels_pour_Produimax': 1, 'Attitude_envers_Produimax': 0}
- Potential patients total 1870.0 (mean 9.54)
- Top specialties: {'Non_renseigne': 54, 'Radiologie': 34, 'Hematologie': 32, 'Urologie': 30, 'Oncologie': 27, 'Proctologie': 20}

## Visit Activity (Visites 2020 focus)
- Filtered 2020 visits: 611 of 624 total (outside scope: 13)
- Date coverage: 2019-03-07 to 2021-12-23
- Mode split 2020: {'Face_a_face': 306, 'Interaction_a_distance': 305}
- Sector coverage 2020: {'S4': 114, 'S6': 106, 'S5': 103, 'S3': 99, 'S2': 97, 'S1': 90, 'S9': 2} (macro breakdown {'Nord': 323, 'Sud': 286, 'Hors_cible': 2})
- Delegate top 5: {'Agatha_CHRISTIE': 114, 'Coco_CHANEL': 106, 'Charlotte_CORDAY': 103, 'Catelyn_STARK': 99, 'Michel_STROGOFF': 97}
- Visits per doctor (count=154, mean=3.97, max=26)
- Average visit duration 37.39 min (median 30 min)
- Attitude share in 2020 visits: {'Neutre': 232, 'Prescripteur': 194, 'Detracteur': 185}

## Coverage vs Potential
- Doctors with 2020 visits: 154 (out of 197)
- Potential patients touched: 1419.0 (vs total 1870.0)
- Attitude mix within covered doctors: {'Neutre': 63, 'Detracteur': 50, 'Prescripteur': 41}
- Top specialties reached: {'Non_renseigne': 40, 'Radiologie': 29, 'Hematologie': 26, 'Urologie': 21, 'Oncologie': 21}

## Data Quality Notes
- 53 doctors missing Specialite_1 and 116 missing Specialite_2 values; consider enrichment before modeling.
- One doctor lacks attitude and region classification (flagged as Non_renseigne).
- Two 2020 visits belong to Secteur S9 (outside Nord/Sud focus); 13 visits fall outside the 2020 time window.
- Visit duration values are text-based and were interpreted as minute counts; confirm consistency if timing precision is required.

## Validation Snapshot
- Excel formulas detected: 9 (no errors found).
- No workbook transformations were applied in this analysis step.

## Suggested Next Checks
1. Confirm whether Secteur S9 visits should be excluded or reassigned before dashboard calculations.
2. Decide on imputation or data collection for missing specialties to support segmentation logic.
3. Align visit duration format (e.g., convert to numeric minutes in workbook) if downstream KPIs rely on time metrics.