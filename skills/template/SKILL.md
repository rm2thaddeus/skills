---
name: template-skill
description: Boilerplate and guidelines for creating new Claude skills. Use this as a starting point when creating new skills for specific domains or workflows.
license: Apache 2.0
---

# Skill Template

Boilerplate and guidelines for creating new Claude skills.

## Structure

```
skills/your_new_skill/
├── README.md                  # Skill documentation (this file)
├── src/                       # Implementation code
│   ├── __init__.py
│   ├── module1.py            # Skill logic
│   └── module2.py
└── tests/                    # Test files
    └── test_module1.py
```

## Creating a New Skill

### Step 1: Copy Template

```bash
cp -r skills/template skills/your_skill_name
cd skills/your_skill_name
```

### Step 2: Update README.md

Document:
- Purpose and use cases
- Skill modules and their functions
- When to use this skill
- Dependencies
- Usage examples
- Output format

### Step 3: Implement Modules

Create Python modules in `src/`:

```python
# src/your_module.py
from typing import Dict
import pandas as pd

def execute_skill(input_data: Dict) -> Dict:
    """
    Main skill execution function
    
    Args:
        input_data: {
            "file_path": str,
            "parameters": dict
        }
    
    Returns:
        {
            "status": "success" | "error",
            "data": {},
            "metadata": {},
            "message": str
        }
    """
    try:
        # Your implementation here
        result = perform_task(input_data)
        
        return {
            "status": "success",
            "data": result,
            "metadata": {"timestamp": "..."},
            "message": "Task completed successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
```

### Step 4: Add Tests

```python
# tests/test_your_module.py
import pytest
from skills.your_skill.src.your_module import execute_skill

def test_basic_execution():
    result = execute_skill({
        "file_path": "test_data.xlsx",
        "parameters": {}
    })
    assert result["status"] == "success"
    assert "data" in result
```

### Step 5: Update Main AGENTS.md

Add your skill to the main `AGENTS.md` file in project root:

```markdown
### N. Your Skill Name
**Location**: `skills/your_skill_name/`  
**When to use**: Brief description of when to use

**Skill modules**:
- `module1.py` - Description
- `module2.py` - Description
```

## Code Standards

### Required
- Python 3.8+
- Type hints for all functions
- Docstrings (Google style)
- Error handling with try/except
- Standardized output format

### Recommended
- Use pandas for data operations
- Use pathlib for file paths
- Include logging
- Add comprehensive tests
- Follow PEP 8

## Output Format Standard

All skills must return this structure:

```python
{
    "status": "success" | "error",
    "data": {},  # Main result
    "metadata": {
        "timestamp": "ISO 8601",
        "processing_time_ms": int,
        # other metadata
    },
    "message": str  # Human-readable message
}
```

## Testing Your Skill

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest skills/your_skill_name/tests/

# Test with Codex
codex "use your skill to process test data"
```

## Dependencies Template

Add to project `requirements.txt`:

```txt
# Your Skill Name
your-package>=1.0.0
another-package>=2.0.0
```

## Documentation Checklist

- [ ] README.md with clear purpose
- [ ] Usage examples for each module
- [ ] When to use this skill
- [ ] Input/output specifications
- [ ] Dependencies listed
- [ ] Test data identified
- [ ] Implementation status noted
- [ ] Added to main AGENTS.md

## Example Skills

Reference existing skills for patterns:
- `skills/bureaucratic/` - Form validation patterns
- `skills/document_handling/` - Document processing patterns

---

**Use this template to maintain consistency across all skills in the repository.**

