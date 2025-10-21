# Excel In ChatGPT - Skills Repository

## Overview

This repository provides Claude skills for Codex CLI to solve data analysis and document processing problems.

## Available Skills

### 1. Bureaucratic Processing
**Location**: `skills/bureaucratic/SKILL.md`  
**When to use**: Form validation, compliance checking, administrative workflows

```bash
codex "validate recruitment form for compliance"
```

**Key capabilities**:
- Form validation against regulations
- Compliance verification
- Data completeness checking
- Administrative report generation

---

### 2. Document Handling
**Location**: `skills/document_handling/SKILL.md`  
**When to use**: Excel/CSV processing, format conversion, data extraction

```bash
codex "convert Excel file to CSV"
```

**Key capabilities**:
- Load and parse Excel/CSV/JSON documents
- Convert between formats
- Extract and filter data
- Merge/split documents
- Generate reports with charts

---

### 3. Creating New Skills
**Location**: `skills/template/SKILL.md`  
**When to use**: Extending capabilities to new domains

**Template includes**:
- Official Anthropic Skills spec format
- YAML frontmatter structure
- Code pattern examples
- Documentation guidelines

---

## How to Use Skills

### Discovery
When a user requests a task:
1. Identify the appropriate skill domain
2. Read the skill's `SKILL.md` file from `skills/[domain]/`
3. Follow instructions and use provided scripts
4. Return standardized output

### Example Flow
```
User: "validate Data/recruitment.xlsx for compliance"

Claude:
1. Recognizes "validate" + "compliance" → bureaucratic skill
2. Reads skills/bureaucratic/SKILL.md
3. Uses scripts/bureaucratic_validator.py per instructions
4. Returns compliance report
```

## Skill Organization

```
skills/
├── bureaucratic/          # Administrative & compliance
│   ├── SKILL.md          # Skill definition (Anthropic format)
│   └── scripts/          # Implementation code
│       ├── __init__.py
│       ├── bureaucratic_validator.py
│       ├── compliance_checker.py
│       └── data_normalizer.py
│
├── document_handling/     # Document processing
│   ├── SKILL.md
│   └── scripts/
│       ├── __init__.py
│       ├── document_loader.py
│       ├── format_converter.py
│       ├── data_extractor.py
│       └── report_generator.py
│
└── template/             # Boilerplate for new skills
    ├── SKILL.md          # Template following Anthropic spec
    └── scripts/
        └── __init__.py
```

## Skill Invocation Pattern

### Standard Skill Interface
All skills follow this pattern:

```python
def execute_skill(input_data: dict) -> dict:
    """
    Standard skill execution interface
    
    Args:
        input_data: {
            "file_path": str,
            "parameters": dict,
            "options": dict
        }
    
    Returns:
        {
            "status": "success" | "error",
            "data": {},
            "metadata": {},
            "message": str
        }
    """
```

### Error Handling
All skills include comprehensive error handling and return standardized error messages.

## Test Data

Use files in `Data/` directory to validate skill outputs:
- `Test_Excel_Recrutement_v3.0*.xlsx` - Recruitment data
- `Aitor-Patino.xlsx` - Sample personal data

## Development Guidelines

### Adding New Skills
1. Copy `skills/template/` to `skills/your-skill-name/`
2. Update `SKILL.md` with YAML frontmatter (name, description, license)
3. Implement Python scripts in `scripts/` directory
4. Test with sample data
5. Update this AGENTS.md file to reference new skill

### Code Standards
- Python 3.8+
- Type hints required
- Comprehensive docstrings
- Error handling for all operations
- Standardized output format

## Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

Core dependencies:
- pandas>=2.0.0
- openpyxl>=3.1.0
- pydantic>=2.0.0

---

**Project**: Excel In ChatGPT  
**Phase**: POC Complete, MVP Ready  
**Last Updated**: 2025-10-21

