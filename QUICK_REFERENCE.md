# Quick Reference - Claude Skills for Codex CLI

## 🚀 Skills Available

### 1. Bureaucratic Processing
**Location**: `skills/bureaucratic/` | [Documentation](skills/bureaucratic/README.md)

```bash
# Validate form compliance
codex "validate Data/Test_Excel_Recrutement_v3.0.xlsx"

# Check data completeness
codex "check if all required fields are filled in recruitment data"

# Generate compliance report
codex "create compliance report for Data/Aitor-Patino.xlsx"
```

### 2. Document Handling
**Location**: `skills/document_handling/` | [Documentation](skills/document_handling/README.md)

```bash
# Load and inspect
codex "show me the structure of Data/Test_Excel_Recrutement_v3.0.xlsx"

# Convert format
codex "convert Data/Aitor-Patino.xlsx to CSV"

# Merge documents
codex "merge all Test_Excel files into one summary"

# Extract data
codex "extract rows where poste='Developer' from recruitment data"
```

### 3. Create New Skill
**Location**: `skills/template/` | [Template Guide](skills/template/README.md)

```bash
# Copy template structure
cp -r skills/template skills/my_new_skill

# Implement in src/
# Document in README.md
# Test with Codex
codex "use my new skill to process data"
```

## 📂 Project Structure

```
Excel In ChatGPT/
├── skills/                        # 🎯 Main deliverable
│   ├── bureaucratic/             # Form validation & compliance
│   ├── document_handling/        # Excel/CSV processing
│   ├── template/                 # Boilerplate for new skills
│   └── README.md                 # Skills documentation
│
├── Data/                         # Test data (6 Excel files)
├── Resources/                    # Documentation & images
│   ├── Documentation/           # PDFs
│   └── Images/                  # Charts
│
├── docs/                        # Development documentation
│   ├── Phase0-Alignment/       # User profile & context
│   ├── Phase1-Ideation/        # Goals & scope
│   ├── Phase2-POC/             # Architecture & spikes
│   ├── Phase3-MVP/             # Implementation plan
│   └── .cursor/rules/          # Development guidelines
│
├── Code/                       # Future implementation
│   ├── Backend/
│   └── Frontend/
│
├── README.md                   # Project overview
├── GETTING_STARTED.md         # Setup guide
├── QUICK_REFERENCE.md         # This file
└── requirements.txt           # Python dependencies
```

## 🛠️ Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Test a skill
codex "validate Data/Test_Excel_Recrutement_v3.0.xlsx for compliance"
```

## 📖 Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Main file - guides Claude on when to use skills |
| `skills/README.md` | Complete skills documentation |
| `skills/*/README.md` | Individual skill documentation |
| `skills/*/src/` | Skill implementation code |
| `requirements.txt` | Python dependencies |
| `README.md` | Project overview |
| `GETTING_STARTED.md` | Detailed setup guide |

## 🎯 Development Phases

- ✅ **Phase 0**: Alignment - User profile & project context defined
- ✅ **Phase 1**: Ideation - Goals, scope, and requirements established
- ✅ **Phase 2**: POC - Skills architecture designed & implemented
- ⏳ **Phase 3**: MVP - Testing with Codex CLI, refinement, production-ready

## 🧪 Testing with Codex CLI

### Prerequisites
1. Codex CLI must be installed and configured
2. This repository should be in a Codex-accessible location
3. Python dependencies installed

### Test Commands

```bash
# Test bureaucratic skill
codex "validate all recruitment files for compliance"

# Test document handling
codex "convert all Excel files to CSV format"

# Test skill combination
codex "extract data from recruitment files, validate compliance, generate report"
```

### Expected Behavior
- Codex discovers AGENTS.md files automatically
- Claude uses skill instructions to generate code
- Code executes with proper error handling
- Outputs follow standardized format

## 🔧 Customization

### Add New Skill

1. **Copy template**:
   ```bash
   cp -r skills/template skills/my_skill
   ```

2. **Edit AGENTS.md**:
   - Update overview & capabilities
   - Define code patterns
   - Add usage examples
   - Include test cases

3. **Test**:
   ```bash
   codex "use my skill to [task description]"
   ```

### Modify Existing Skill

1. Open skill's AGENTS.md
2. Update relevant sections
3. Test changes with Codex
4. Update version & changelog

## 💡 Best Practices

1. **Skill Documentation**: Always update AGENTS.md with new patterns
2. **Error Handling**: Include comprehensive error handling in examples
3. **Testing**: Use test data in `Data/` for validation
4. **Standardization**: Follow template structure for consistency
5. **Version Control**: Update changelog when modifying skills

## 🐛 Troubleshooting

### Codex doesn't see my skill
- Ensure AGENTS.md exists in skill directory
- Check file is properly formatted markdown
- Verify Codex CLI can access repository path

### Skill execution fails
- Check Python dependencies are installed (`pip install -r requirements.txt`)
- Verify test data exists in `Data/` directory
- Review error messages in skill output
- Check file paths in commands

### Import errors
- Activate virtual environment if using one
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- Check Python version (3.8+ required)

## 📚 Documentation Links

- [Main README](README.md)
- [Getting Started Guide](GETTING_STARTED.md)
- [Main Agent Instructions](AGENTS.md)
- [Skills Documentation](skills/README.md)
- [Bureaucratic Skill](skills/bureaucratic/README.md)
- [Document Handling Skill](skills/document_handling/README.md)
- [Skill Template](skills/template/README.md)
- [Phase Documentation](docs/)

## 📞 Support

- Review skill AGENTS.md for specific guidance
- Check `docs/` for development methodology
- Refer to `GETTING_STARTED.md` for setup help
- Test with provided data in `Data/` directory

---

**Last Updated**: 2025-10-21  
**Phase**: POC Complete, Ready for MVP  
**Skills**: 3 (Bureaucratic, Document Handling, Template)

