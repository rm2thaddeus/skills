# Office Automation Agents

## Overview

This system provides Claude agents for office automation tasks using Anthropic's document-skills and skill-creator capabilities. The agents process documents, perform data analysis, and generate reports while maintaining human oversight through structured workflows with audit trails.

### Preflight & Execution Mode
- Agents MUST run preflight checks before any operation:
  - Prefer Anthropic submodule paths when present: `Code/anthropic-skills/document-skills/*`.
  - Otherwise verify local skeletons exist (`skills/document_handling`, `skills/template`).
  - Verify optional external scripts (e.g., `recalc.py`) are available; otherwise, skip dependent steps.
  - If required components are missing, return status: `pending_implementation` and do not attempt execution.
- Execution mode defaults to POC skeleton per `config.yaml` (`execution_mode: poc_skeleton`, `non_destructive_writes: true`).
- All write operations require approval; destructive writes are disabled in POC skeleton mode.

### Interviews/LinkedIn Pipeline Data Contracts (updated)
- Canonical normalized fields (first data sheet): `event_date`, `start_time`, `end_time`, `duration_minutes`, `company`, `role`, `medium`, `source`, `contacts`, `notes`, `period`, `year`.
- `normalized_interviews.xlsx` MUST NOT contain internal columns (`__source__`, `__key__`, `__login_time__`). These are reserved for internal processing and are dropped before export.
- `merged_interview_events.xlsx` MAY include `__source__` to indicate origin (`curated` or `linkedin`), but MUST NOT include `__key__` (internal dedupe key is dropped before export).
- PROVENANCE sheet MUST be appended as the LAST sheet so the first sheet is always the dataset, not metadata.
- When a “Basic” LinkedIn export is provided, the pipeline MUST scan `.../Jobs/` for job application CSVs and aggregate them to compute `Applications_By_Year` and `Application_Periods`.
- Date parsing MUST coerce unparseable values to NA (no string `NaT` in data); keys and other internal helpers must not leak to exported sheets.

### Quick Start (Testing)
- Initialize/update the Anthropic skills submodule:
  - `git submodule update --init --recursive`
- Confirm paths exist per `config.yaml` (Anthropic first, local fallback).
- Use the prompts under "Usage Examples" to run read-only tests; writes require approval and go under `artifacts/`.

## Available Agents

### 1. Excel Processing Agent
**Location**: `skills/document_handling/`  
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
4. If available, use `recalc.py` for formula recalculation; otherwise return `validation_skipped: recalc_unavailable`
5. Validate zero errors when recalculation is available; otherwise return `pending_implementation`
6. Generate audit trail with all changes
7. For interviews/LinkedIn runs, validate:
   - First sheet is data (not PROVENANCE)
   - `normalized_interviews.xlsx` excludes internal columns
   - `merged_interview_events.xlsx` excludes `__key__`
   - Applications tables populate when Jobs CSVs exist in Basic export

---

### 2. Document Processing Agent
**Location**: `skills/document_handling/`  
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
**Location**: `skills/template/`  
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

### POC Status Codes
- `pending_implementation`: Required component missing or skeleton-only step
- `validation_skipped: recalc_unavailable`: LibreOffice/recalc not available

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
**Last Updated**: 2025-10-30  
**Integration**: Anthropic Skills + Human-in-the-Loop Workflows