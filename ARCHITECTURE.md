# Architecture - Claude Skills for Codex CLI

## Design Philosophy

**Separation of Concerns**: AGENTS guide, Skills implement

```
┌─────────────────────────────────────────────────┐
│  User Request via Codex CLI                     │
│  "validate recruitment data for compliance"     │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  AGENTS.md (Root)                               │
│  ─────────────────                              │
│  • Identifies: "bureaucratic" skill needed      │
│  • Guides Claude: READ skills/bureaucratic/     │
│  • Instructs: Use bureaucratic_validator.py     │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Skill Documentation                            │
│  skills/bureaucratic/README.md                  │
│  ─────────────────────────────                  │
│  • Purpose & capabilities                       │
│  • Module descriptions                          │
│  • Usage examples                               │
│  • Input/output specs                           │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Skill Implementation                           │
│  skills/bureaucratic/src/                       │
│  ──────────────────────────                     │
│  • bureaucratic_validator.py                    │
│  • compliance_checker.py                        │
│  • data_normalizer.py                           │
│                                                 │
│  Claude executes Python code                    │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Test Data                                      │
│  Data/Test_Excel_Recrutement_v3.0.xlsx         │
│  ────────────────────────────────              │
│  Skill processes file, returns result           │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│  Standardized Output                            │
│  {                                              │
│    "status": "success",                         │
│    "data": {...},                               │
│    "metadata": {...}                            │
│  }                                              │
└─────────────────────────────────────────────────┘
```

## Directory Structure

```
Excel In ChatGPT/
│
├── AGENTS.md                      ⭐ Main orchestrator
│   └─> Guides Claude on WHEN to use which skill
│
├── skills/                        ⭐ Skills repository
│   │
│   ├── bureaucratic/              📁 Skill domain
│   │   ├── README.md             📄 Skill documentation
│   │   └── src/                  🐍 Python implementation
│   │       ├── __init__.py
│   │       ├── bureaucratic_validator.py
│   │       ├── compliance_checker.py
│   │       └── data_normalizer.py
│   │
│   ├── document_handling/         📁 Skill domain
│   │   ├── README.md             📄 Skill documentation
│   │   └── src/                  🐍 Python implementation
│   │       ├── __init__.py
│   │       ├── document_loader.py
│   │       ├── format_converter.py
│   │       ├── data_extractor.py
│   │       └── report_generator.py
│   │
│   └── template/                  📁 Template for new skills
│       ├── README.md             📋 How to create skills
│       └── src/                  🐍 Boilerplate code
│           └── __init__.py
│
├── Data/                         📊 Test data
│   └── *.xlsx                    Excel files for validation
│
└── Resources/                    📚 Documentation & assets
    ├── Documentation/
    └── Images/
```

## Component Responsibilities

### 1. AGENTS.md (Root)
**Role**: Orchestration & Guidance

**Responsibilities**:
- Map user requests to appropriate skills
- Guide Claude on which skill to read
- Provide high-level skill invocation patterns
- Define standard interfaces

**Does NOT**:
- Contain implementation code
- Duplicate skill documentation
- Describe internal skill logic

**Example Content**:
```markdown
### Bureaucratic Processing
**Location**: `skills/bureaucratic/`
**When to use**: Form validation, compliance checking

**Skill modules**:
- bureaucratic_validator.py - Form validation
- compliance_checker.py - Compliance verification
```

---

### 2. Skill README.md
**Role**: Documentation

**Responsibilities**:
- Describe skill purpose and capabilities
- Document each module's function
- Provide usage examples
- Define input/output specifications
- List dependencies

**Does NOT**:
- Contain implementation code
- Duplicate AGENTS.md guidance
- Include other skills' information

**Example Content**:
```markdown
# Bureaucratic Processing Skill

## Purpose
Handle administrative tasks and compliance checking

## Skill Modules

### bureaucratic_validator.py
Validates forms against regulations

**Usage**:
```python
from skills.bureaucratic.src.bureaucratic_validator import validate_form
result = validate_form(file_path="data.xlsx")
```
```

---

### 3. Skill src/ (Implementation)
**Role**: Execution

**Responsibilities**:
- Implement skill logic in Python
- Handle errors gracefully
- Return standardized outputs
- Process data efficiently

**Does NOT**:
- Contain documentation (use README.md)
- Include user-facing guides
- Mix concerns between modules

**Example Structure**:
```python
# skills/bureaucratic/src/bureaucratic_validator.py
from typing import Dict
import pandas as pd

def validate_form(file_path: str, form_type: str = "recruitment") -> Dict:
    """
    Validate form data against regulations
    
    Args:
        file_path: Path to Excel file
        form_type: Type of form to validate
    
    Returns:
        Standardized result dictionary
    """
    try:
        df = pd.read_excel(file_path)
        # Validation logic here
        return {
            "status": "success",
            "data": {"valid_records": 95, ...},
            "metadata": {...}
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

---

### 4. Test Data (Data/)
**Role**: Validation

**Responsibilities**:
- Provide sample data for testing
- Enable output validation
- Support skill development

---

## Information Flow

### Phase 1: Request Analysis
```
User: "validate recruitment.xlsx for compliance"
    ↓
AGENTS.md identifies: bureaucratic skill
    ↓
Claude reads: skills/bureaucratic/README.md
```

### Phase 2: Implementation Discovery
```
README.md describes: bureaucratic_validator.py
    ↓
Claude reads: skills/bureaucratic/src/bureaucratic_validator.py
    ↓
Claude understands: validate_form() function
```

### Phase 3: Execution
```
Claude executes:
  result = validate_form("Data/recruitment.xlsx")
    ↓
Returns standardized output
    ↓
User receives result
```

## Design Principles

### 1. Single Responsibility
- **AGENTS.md**: WHEN to use skills
- **README.md**: WHAT skills do
- **src/**: HOW skills work

### 2. Standardization
All skills follow same structure:
- README.md for documentation
- src/ for implementation
- Standardized output format

### 3. Discoverability
- Clear naming conventions
- Consistent directory structure
- Cross-referenced documentation

### 4. Extensibility
- Template for new skills
- Modular architecture
- Clear interfaces

### 5. Testability
- Test data provided
- Standardized outputs
- Clear validation criteria

## Adding New Skills

### Step 1: Copy Template
```bash
cp -r skills/template skills/new_skill
```

### Step 2: Update Documentation
Edit `skills/new_skill/README.md`:
- Purpose and capabilities
- Module descriptions
- Usage examples

### Step 3: Implement Code
Create modules in `skills/new_skill/src/`:
- Follow standard patterns
- Implement standard interface
- Handle errors properly

### Step 4: Register in AGENTS.md
Add skill to root AGENTS.md:
```markdown
### N. New Skill Name
**Location**: `skills/new_skill/`
**When to use**: Description

**Skill modules**:
- module1.py - Description
```

### Step 5: Test
```bash
codex "use new skill to process data"
```

## Best Practices

### For AGENTS.md
✅ Keep brief and focused on WHEN  
✅ Link to skill READMEs  
✅ Provide command examples  
❌ Don't duplicate skill documentation  
❌ Don't include implementation details  

### For Skill README.md
✅ Document all modules  
✅ Provide usage examples  
✅ Define I/O specifications  
❌ Don't include AGENTS.md content  
❌ Don't mix documentation with code  

### For Skill src/
✅ Follow Python best practices  
✅ Use type hints  
✅ Handle errors gracefully  
✅ Return standardized outputs  
❌ Don't embed documentation  
❌ Don't mix concerns  

## Output Standardization

All skills MUST return this format:

```python
{
    "status": "success" | "error",
    "data": {
        # Skill-specific result data
    },
    "metadata": {
        "timestamp": "ISO 8601",
        "processing_time_ms": int,
        # Other metadata
    },
    "message": str  # Human-readable message
}
```

## Error Handling

All skills MUST handle errors:

```python
try:
    result = perform_task()
    return {"status": "success", "data": result, ...}
except FileNotFoundError as e:
    return {"status": "error", "message": f"File not found: {e}"}
except Exception as e:
    return {"status": "error", "message": f"Error: {e}"}
```

---

## Summary

**Clear Separation**: 
- AGENTS.md = Orchestrator (when/which)
- README.md = Documentation (what)
- src/ = Implementation (how)

**Benefits**:
- Easy to understand
- Simple to extend
- Maintainable
- Testable

**Result**: Clean architecture where Claude can efficiently discover, understand, and execute skills based on user requests.

---

**Last Updated**: 2025-10-21  
**Status**: POC Architecture Complete

