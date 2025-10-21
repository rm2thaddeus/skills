---
name: bureaucratic
description: Handle administrative tasks, form validation, and compliance checking for Excel-based documents. Use when validating forms against regulations, checking data completeness, verifying compliance, or generating administrative reports.
license: Apache 2.0
---

# Bureaucratic Processing Skill

Handle administrative tasks, form validation, and compliance checking for Excel-based documents.

## Skill Modules

### `bureaucratic_validator.py`
Validates forms against regulations and standards.

**Usage**:
```python
from skills.bureaucratic.scripts.bureaucratic_validator import validate_form

result = validate_form(
    file_path="Data/recruitment.xlsx",
    form_type="recruitment"
)
```

### `compliance_checker.py`
Verifies data against compliance requirements.

**Usage**:
```python
from skills.bureaucratic.scripts.compliance_checker import check_compliance

result = check_compliance(
    df=dataframe,
    rules_path="config/rules.yaml"
)
```

### `data_normalizer.py`
Standardizes data formats (dates, IDs, names).

**Usage**:
```python
from skills.bureaucratic.scripts.data_normalizer import normalize_data

result = normalize_data(
    df=dataframe,
    fields=["date", "id", "name"]
)
```

## When to Use

- "validate form for compliance"
- "check if data is complete"
- "standardize date formats"
- "verify administrative requirements"
- "generate compliance report"

## Dependencies

```python
pandas>=2.0.0
openpyxl>=3.1.0
pydantic>=2.0.0
python-dateutil>=2.8.0
```

## Test Data

Use `Data/Test_Excel_Recrutement_v3.0*.xlsx` files for testing.

## Output Format

```json
{
  "status": "success",
  "data": {
    "total_records": 100,
    "valid_records": 95,
    "errors": [...],
    "warnings": [...],
    "compliance_score": 0.95
  },
  "metadata": {
    "validation_timestamp": "2025-10-21T12:00:00Z"
  }
}
```

## Implementation Status

**Phase**: POC - Implementation skeleton ready  
**Next**: Implement actual validation logic in Phase 3 MVP

