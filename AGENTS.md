# Office Automation Agents

## Overview

This system provides Claude agents for office automation tasks using Anthropic's document-skills and skill-creator capabilities. The agents process documents, perform data analysis, and generate reports while maintaining human oversight through structured workflows with audit trails.

## Available Agents

### 1. Excel Processing Agent
**Location**: `Code/anthropic-skills/document-skills/xlsx/`  
**When to use**: Excel file creation, editing, analysis, and formula management

```bash
# Process Excel file with data analysis
claude "analyze Data/Test_Excel_Recrutement_v3.0.xlsx and generate insights"

# Create financial model with formulas
claude "create financial model from Data/sales_data.xlsx with growth projections"
```

**Key capabilities**:
- Zero formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Preserve existing templates and formatting
- Industry-standard color coding (Blue inputs, Black formulas, Green internal links, Red external links)
- Proper number formatting (currency, percentages, multiples)
- Formula recalculation using LibreOffice integration
- Comprehensive error checking and validation

**Workflow**:
1. Load Excel file using pandas or openpyxl
2. Analyze data structure and requirements
3. Apply transformations while preserving formulas
4. Use `recalc.py` script for formula recalculation
5. Validate zero errors before completion
6. Generate audit trail with all changes

---

### 2. Document Processing Agent
**Location**: `Code/anthropic-skills/document-skills/`  
**When to use**: Multi-format document processing (docx, pdf, pptx)

```bash
# Convert document formats
claude "convert Data/report.docx to PDF with proper formatting"

# Extract data from PDF forms
claude "extract form data from Data/application.pdf"
```

**Key capabilities**:
- DOCX: Document creation, editing, template processing
- PDF: Form processing, data extraction, document manipulation
- PPTX: Presentation creation, template application, slide management
- Format conversion between document types
- Template preservation and customization

---

### 3. Skill Creator Agent
**Location**: `Code/anthropic-skills/skill-creator/`  
**When to use**: Extending capabilities for specific office workflows

```bash
# Create custom skill for specific workflow
claude "create skill for invoice processing workflow"

# Extend existing skill for new document type
claude "extend xlsx skill for budget template processing"
```

**Key capabilities**:
- Skill creation following Anthropic's official format
- YAML frontmatter with proper metadata
- Bundled resources (scripts, references, assets)
- Progressive disclosure design for context efficiency
- Validation and packaging for distribution

---

## Human-in-the-Loop Workflow

### Approval Process
All document transformations require human approval at key stages:

1. **Analysis Phase**: Present findings and proposed changes
2. **Transformation Phase**: Show before/after comparisons
3. **Validation Phase**: Display error reports and validation results
4. **Final Review**: Complete audit trail and artifact summary

### Audit Trail System
Every operation generates comprehensive audit artifacts:

```json
{
  "operation_id": "uuid-here",
  "timestamp": "2025-01-21T10:30:00Z",
  "agent": "excel-processing",
  "input_file": "Data/Test_Excel_Recrutement_v3.0.xlsx",
  "output_file": "Data/Test_Excel_Recrutement_v3.0_processed.xlsx",
  "changes": [
    {
      "sheet": "Sheet1",
      "cell": "B10",
      "old_value": "=SUM(B2:B9)",
      "new_value": "=SUM(B2:B10)",
      "reason": "Extended range to include new data"
    }
  ],
  "validation": {
    "formula_errors": 0,
    "total_formulas": 42,
    "status": "success"
  },
  "approval_status": "pending",
  "approved_by": null,
  "approved_at": null
}
```

### Artifact Management
All operations create artifacts for tracking and review:

- **Input Artifacts**: Original files with metadata
- **Processing Artifacts**: Intermediate files and logs
- **Output Artifacts**: Final processed files
- **Audit Artifacts**: Complete operation history
- **Validation Artifacts**: Error reports and validation results

## Integration Architecture

### Skill Integration Pattern
```python
def execute_office_automation_task(task_data: dict) -> dict:
    """
    Standard office automation task execution
    
    Args:
        task_data: {
            "agent_type": "excel-processing" | "document-processing" | "skill-creator",
            "input_file": str,
            "parameters": dict,
            "workflow_options": dict
        }
    
    Returns:
        {
            "status": "success" | "error" | "pending_approval",
            "artifacts": [],
            "audit_trail": {},
            "approval_required": bool,
            "message": str
        }
    """
```

### File Organization
```
artifacts/
├── operations/           # Operation-specific artifacts
│   ├── {operation_id}/
│   │   ├── input/        # Original files
│   │   ├── processing/   # Intermediate files
│   │   ├── output/       # Final results
│   │   └── audit.json    # Complete audit trail
├── approvals/           # Pending approvals
└── completed/           # Approved operations
```

## Usage Examples

### Excel Data Analysis
```bash
# Analyze recruitment data
claude "analyze Data/Test_Excel_Recrutement_v3.0.xlsx for compliance issues and generate summary report"

# Create financial projections
claude "create 5-year financial model from Data/sales_data.xlsx with scenario analysis"
```

### Document Processing
```bash
# Process multiple document types
claude "extract key metrics from Data/report.pdf and create Excel summary"

# Convert and format documents
claude "convert Data/presentation.pptx to PDF with company branding"
```

### Custom Workflow Creation
```bash
# Create invoice processing skill
claude "create skill for processing invoice PDFs and extracting data to Excel templates"

# Extend existing capabilities
claude "extend xlsx skill to handle budget variance analysis workflows"
```

## Quality Assurance

### Validation Requirements
- **Zero Formula Errors**: All Excel files must pass formula validation
- **Template Preservation**: Existing formatting and conventions maintained
- **Data Integrity**: No data loss during processing
- **Audit Completeness**: Full operation history recorded
- **Human Approval**: All transformations require explicit approval

### Error Handling
- Comprehensive error detection and reporting
- Graceful fallback to manual processing
- Clear error messages with remediation steps
- Automatic backup creation before processing
- Rollback capabilities for failed operations

## Development Guidelines

### Adding New Agents
1. Follow skill-creator patterns from `Code/anthropic-skills/skill-creator/`
2. Implement proper audit trail generation
3. Include human approval checkpoints
4. Test with existing data files
5. Update this agents.md file with new capabilities

### Extending Existing Agents
1. Use skill-creator extension patterns
2. Maintain backward compatibility
3. Update validation requirements
4. Test with comprehensive data sets
5. Document new capabilities

---

**Project**: Excel In ChatGPT - Office Automation  
**Phase**: MVP Development  
**Last Updated**: 2025-01-21  
**Integration**: Anthropic Skills + Human-in-the-Loop Workflows