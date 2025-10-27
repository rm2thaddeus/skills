# Excel In ChatGPT - Office Automation System

## Overview

This system provides Claude agents for office automation tasks using Anthropic's document-skills and skill-creator capabilities. The system processes documents, performs data analysis, and generates reports while maintaining human oversight through structured workflows with comprehensive audit trails.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- LibreOffice (for Excel formula recalculation)
- Anthropic's document-skills repository
- Claude API access

### Installation

1. **Clone and setup the repository:**
```bash
git clone <your-repo>
cd "Excel In ChatGPT"
pip install -r requirements.txt
```

2. **Ensure Anthropic skills are available:**
```bash
# The anthropic-skills should be in Code/anthropic-skills/
ls Code/anthropic-skills/document-skills/
ls Code/anthropic-skills/skill-creator/
```

3. **Initialize the system:**
```bash
python office_automation.py
```

## 📋 Available Agents

### 1. Excel Processing Agent
Processes Excel files with zero formula errors and comprehensive validation.

**Usage:**
```python
from office_automation import process_excel_file

result = process_excel_file(
    "Data/Test_Excel_Recrutement_v3.0.xlsx",
    {
        "analysis_type": "compliance_check",
        "output_format": "summary_report"
    }
)
```

**Key Features:**
- ✅ Zero formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- ✅ Preserves existing templates and formatting
- ✅ Industry-standard color coding
- ✅ Formula recalculation with LibreOffice
- ✅ Comprehensive error validation

### 2. Document Processing Agent
Handles multi-format document processing (docx, pdf, pptx).

**Usage:**
```python
from office_automation import process_document

result = process_document(
    "Data/report.docx",
    {
        "operation": "convert_to_pdf",
        "preserve_formatting": True
    }
)
```

### 3. Skill Creator Agent
Creates and extends skills using Anthropic's skill-creator patterns.

**Usage:**
```python
from office_automation import create_skill

result = create_skill(
    "invoice_processor",
    {
        "description": "Process invoice PDFs and extract data to Excel",
        "capabilities": ["pdf_extraction", "excel_export"]
    }
)
```

## 🔄 Human-in-the-Loop Workflow

### Approval Process

All document transformations require human approval at key stages:

1. **Analysis Phase**: Present findings and proposed changes
2. **Transformation Phase**: Show before/after comparisons  
3. **Validation Phase**: Display error reports and validation results
4. **Final Review**: Complete audit trail and artifact summary

### Managing Approvals

```python
from workflow_manager import get_pending_approvals, approve_operation

# Get all pending approvals
pending = get_pending_approvals()
for approval in pending:
    print(f"Operation {approval.operation_id}: {approval.description}")

# Approve an operation
success = approve_operation("operation-123", "user", "Looks good!")
```

## 📊 Artifact Tracking

### Comprehensive Audit Trail

Every operation generates detailed artifacts:

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
  "approval_status": "approved",
  "approved_by": "user",
  "approved_at": "2025-01-21T10:35:00Z"
}
```

### Artifact Management

```python
from artifact_tracker import register_artifact, validate_artifact_integrity

# Register an artifact
artifact_id = register_artifact(
    "operation-123",
    "output.xlsx",
    "output",
    "Processed Excel file",
    ["excel", "processed"]
)

# Validate integrity
validation = validate_artifact_integrity(artifact_id)
print(f"File integrity: {validation['valid']}")
```

## 🗂️ File Organization

```
artifacts/
├── operations/           # Active operations
│   ├── {operation_id}/
│   │   ├── input/        # Original files
│   │   ├── processing/   # Intermediate files
│   │   ├── output/       # Final results
│   │   └── audit.json    # Complete audit trail
├── approvals/           # Pending approvals
├── completed/           # Approved operations
├── archived/            # Archived operations
└── backups/             # Backup files
```

## 🔧 Configuration

Edit `config.yaml` to customize the system:

```yaml
# Human-in-the-Loop Settings
require_approval_for:
  - excel_formula_changes
  - document_format_conversion
  - new_skill_creation
  - data_extraction_operations

auto_approve_for:
  - read_only_operations
  - validation_only_checks
  - metadata_extraction

# Validation Requirements
excel_validation:
  max_formula_errors: 0
  require_recalc: true
  validate_references: true
```

## 📈 Usage Examples

### Excel Data Analysis
```python
# Analyze recruitment data for compliance
result = process_excel_file(
    "Data/Test_Excel_Recrutement_v3.0.xlsx",
    {
        "analysis_type": "compliance_check",
        "generate_summary": True,
        "check_formulas": True
    }
)

if result["status"] == "pending_approval":
    print(f"Operation {result['operation_id']} requires approval")
    # Review artifacts and approve
    approve_operation(result["operation_id"], "user", "Approved after review")
```

### Document Processing Pipeline
```python
# Process multiple documents
documents = [
    "Data/report.docx",
    "Data/presentation.pptx", 
    "Data/analysis.pdf"
]

for doc in documents:
    result = process_document(doc, {"preserve_formatting": True})
    if result["status"] == "pending_approval":
        print(f"Document {doc} processed, awaiting approval")
```

### Custom Skill Creation
```python
# Create custom skill for specific workflow
result = create_skill(
    "budget_analyzer",
    {
        "description": "Analyze budget Excel files and generate variance reports",
        "capabilities": ["excel_analysis", "variance_calculation", "report_generation"],
        "templates": ["budget_template.xlsx"]
    }
)
```

## 🔍 Monitoring and Compliance

### Generate Compliance Reports
```python
from artifact_tracker import generate_compliance_report

# Generate report for specific operation
report = generate_compliance_report("operation-123")
print(f"Operation processed {report['summary']['total_artifacts']} artifacts")

# Generate system-wide report
system_report = generate_compliance_report()
print(f"System has {system_report['summary']['total_artifacts']} total artifacts")
```

### Monitor System Health
```python
from workflow_manager import get_pending_approvals
from artifact_tracker import ArtifactTracker

# Check pending approvals
pending = get_pending_approvals()
print(f"Pending approvals: {len(pending)}")

# Check artifact integrity
tracker = ArtifactTracker()
all_artifacts = tracker._get_all_artifacts()
corrupted = [a for a in all_artifacts if a.status.value == "corrupted"]
print(f"Corrupted artifacts: {len(corrupted)}")
```

## 🛠️ Development

### Adding New Agents

1. **Extend the base class:**
```python
class CustomAgent(OfficeAutomationAgent):
    def __init__(self):
        super().__init__("custom-agent")
    
    def process_custom_task(self, input_data, parameters):
        # Implementation
        pass
```

2. **Update configuration:**
```yaml
custom_agent:
  name: "Custom Agent"
  capabilities:
    - custom_processing
    - specialized_validation
```

3. **Test with sample data:**
```python
# Test with existing data files
result = custom_agent.process_custom_task(
    "Data/test_file.xlsx",
    {"custom_param": "value"}
)
```

### Extending Existing Agents

1. **Follow skill-creator patterns**
2. **Maintain backward compatibility**
3. **Update validation requirements**
4. **Test with comprehensive data sets**
5. **Document new capabilities**

## 🔒 Security and Compliance

### Data Protection
- ✅ Encrypt sensitive data
- ✅ Secure deletion capabilities
- ✅ Access logging
- ✅ Immutable audit trails

### Compliance Features
- ✅ GDPR compliant data handling
- ✅ 90-day data retention policy
- ✅ User consent tracking
- ✅ Data anonymization options

## 📚 Integration with Anthropic Skills

### Document Skills Integration
The system integrates with Anthropic's document-skills:

- **xlsx**: Excel processing with formula management
- **docx**: Word document processing
- **pdf**: PDF form processing and data extraction
- **pptx**: PowerPoint presentation management

### Skill Creator Integration
Uses skill-creator patterns for:
- Creating new specialized skills
- Extending existing capabilities
- Template generation
- Validation and packaging

## 🚨 Troubleshooting

### Common Issues

1. **Formula Errors in Excel**
   - Check LibreOffice installation
   - Verify recalc.py script execution
   - Review formula references

2. **Approval Workflow Issues**
   - Check config.yaml settings
   - Verify artifact directory permissions
   - Review audit trail files

3. **Integration Problems**
   - Verify anthropic-skills paths
   - Check Python dependencies
   - Review error logs

### Debug Mode
Enable debug mode in `config.yaml`:
```yaml
debug_mode: true
verbose_logging: true
save_intermediate_files: true
```

## 📞 Support

For issues and questions:
1. Check the audit trails in `artifacts/`
2. Review configuration in `config.yaml`
3. Examine error logs
4. Validate artifact integrity

---

**Project**: Excel In ChatGPT - Office Automation  
**Version**: MVP 1.0  
**Last Updated**: 2025-01-21  
**Integration**: Anthropic Skills + Human-in-the-Loop Workflows