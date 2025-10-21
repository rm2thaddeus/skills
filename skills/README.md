# Claude Skills for Codex CLI

This repository contains Claude skills following [Anthropic's official Skills spec](https://github.com/anthropics/skills).

## Architecture

**Based on Anthropic's Skills Format**:
- **SKILL.md**: Each skill has a `SKILL.md` file with YAML frontmatter and instructions
- **YAML Frontmatter**: Required fields: `name`, `description`; optional: `license`
- **Scripts**: Implementation code in `scripts/` directory
- **Self-contained**: Each skill folder includes all resources needed

**For Codex CLI**:
- **AGENTS.md** (root): Guides Claude on WHEN to use which skill
- **SKILL.md**: The actual skill instructions Claude follows

## 📚 Available Skills

### 1. [Bureaucratic Processing](./bureaucratic/SKILL.md)

Handle administrative tasks, form validation, and compliance checking.

**When to use**:
- Form validation against regulations
- Data completeness checks
- Compliance verification
- Administrative report generation

**Quick Start**:
```bash
codex "validate Data/Test_Excel_Recrutement_v3.0.xlsx for compliance"
```

---

### 2. [Document Handling](./document_handling/SKILL.md)

Process, extract, and transform documents in various formats.

**When to use**:
- Loading Excel/CSV/JSON documents
- Converting between formats
- Extracting and filtering data
- Merging/splitting documents
- Generating reports with charts

**Quick Start**:
```bash
codex "convert Data/Aitor-Patino.xlsx to CSV"
```

---

### 3. [Skill Template](./template/SKILL.md)

Template for creating new Claude skills following Anthropic's official spec.

**Use when**:
- Creating new skills
- Learning skill structure
- Following best practices

**Quick Start**:
```bash
cp -r skills/template skills/your-skill-name
```

---

## 🚀 How Skills Work

### Anthropic Skills Format

Each skill is a folder containing:

```
skill-name/
  ├── SKILL.md              # Required: Skill definition
  ├── scripts/              # Optional: Implementation code
  │   ├── __init__.py
  │   └── module.py
  └── resources/            # Optional: Templates, configs, etc.
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: Clear description of what this skill does and when to use it
license: Apache 2.0
---

# Skill Name

[Instructions that Claude will follow...]

## Usage Examples
...

## Guidelines
...
```

### Discovery Flow

1. User makes request via Codex CLI
2. Root `AGENTS.md` guides Claude to appropriate skill
3. Claude reads skill's `SKILL.md`
4. Claude follows instructions and uses scripts as needed
5. Returns standardized output

---

## 📋 Creating New Skills

### Step 1: Copy Template

```bash
cp -r skills/template skills/your-skill-name
```

### Step 2: Update SKILL.md

Edit `skills/your-skill-name/SKILL.md`:

```yaml
---
name: your-skill-name
description: Complete description of what your skill does and when Claude should use it
license: Apache 2.0
---
```

### Step 3: Add Instructions

Write clear instructions in markdown:
- What the skill does
- When to use it
- How to use it
- Code examples
- Best practices

### Step 4: Implement Scripts

Add Python scripts in `scripts/` directory:
- Follow standard patterns
- Use type hints
- Include docstrings
- Return standardized outputs

### Step 5: Test

```bash
codex "use your-skill-name to process test data"
```

### Step 6: Register

Add your skill to root `AGENTS.md`

---

## 🎯 Skill Standards

### Required Format

✅ **SKILL.md** with YAML frontmatter  
✅ `name` field (lowercase, hyphens)  
✅ `description` field (complete, clear)  
✅ Markdown instructions  

### Best Practices

✅ Self-contained (all resources in skill folder)  
✅ Clear, actionable instructions  
✅ Code examples for complex operations  
✅ Standardized output format  
✅ Error handling  
✅ Test data or examples  

### Output Standard

All skills should return:

```python
{
    "status": "success" | "error",
    "data": {...},
    "metadata": {...},
    "message": str
}
```

---

## 📚 Reference

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- [Main AGENTS.md](../AGENTS.md)
- [Architecture Documentation](../ARCHITECTURE.md)

---

## 🧪 Testing

### Test Data

Use files in `../Data/` directory:
- `Test_Excel_Recrutement_v3.0*.xlsx` - Recruitment data
- `Aitor-Patino.xlsx` - Sample personal data

### Test Command

```bash
codex "use [skill-name] to process Data/test-file.xlsx"
```

---

**Project**: Excel In ChatGPT  
**Format**: Anthropic Skills Spec v1.0  
**Last Updated**: 2025-10-21
