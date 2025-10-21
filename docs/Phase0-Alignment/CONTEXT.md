# Project Context

---
phase: 0
artifact: context
project: Excel In ChatGPT
owner: Aitor
updated: 2025-10-21
sources:
  - Resources/Documentation/Excel automation prd.pdf
  - Resources/Documentation/Excel automation with Python.pdf
  - Data/Test_Excel_Recrutement_v3.0*.xlsx
links:
  profile: ./PROFILE.yaml
---

## Main Idea

**Build a repository of Claude skills for Codex CLI that solves data analysis and document processing problems.**

**Clarification**: Excel files in `Data/` are test data to gauge Codex outputs, not the primary focus.

## Background

This project focuses on building a CLI tool (for Codex) that automates Excel workflows with ChatGPT integration, specifically targeting recruitment data processing and analysis.

### Key Context
- **Platform**: Codex CLI (command-line interface)
- **Approach**: Python for data processing + specialized instructions for Excel updates
- **Domain**: Recruitment data automation

## Current State

### Existing Assets
- **Test Data**: 6 Excel files with recruitment data (Test_Excel_Recrutement_v3.0*.xlsx)
- **Personal Data**: Aitor-Patino.xlsx
- **Documentation**: 
  - Excel automation PRD (PDF)
  - Excel automation with Python guide (PDF)
- **Outputs**: 3 chart visualizations (coverage, modes by region, monthly visits)
- **Archive**: excel_automation.zip with previous work

### Technical Foundation
- Python for data processing (user has some experience)
- Excel manipulation (user has automated parts before)
- Understanding that Python is best for data, special handling for Excel formatting

### Known Constraints
- Must work as CLI tool (Codex environment)
- Windows 10 development environment
- Python-based implementation
- Needs to handle both data processing and Excel formatting

## Goals

_To be refined in Phase 1_

Primary:
- Build functional Codex CLI tool
- Automate recruitment data workflows
- Integrate ChatGPT capabilities

## Non-Goals

- Web-based interface (this is CLI-focused)
- Real-time collaboration features
- Manual Excel manipulation

## Open Questions

1. **Scope**: What specific recruitment workflows need automation?
   - Data validation?
   - Report generation?
   - Data analysis and insights?
   - Chart creation?

2. **ChatGPT Integration**: How will AI be used?
   - Natural language queries?
   - Automated insights generation?
   - Data cleaning suggestions?
   - Report writing?

3. **Input/Output**: What are the expected formats?
   - Input: Excel files with what structure?
   - Output: Modified Excel files? New reports? Charts?

4. **Codex CLI**: What commands/interface is expected?
   - Single command execution?
   - Interactive mode?
   - Batch processing?

## User Preferences

- **Working Style**: Action-oriented, make decisions and explain after
- **Communication**: Key decisions only, not step-by-step
- **Updates**: At major phase milestones
- **Experience**: Intermediate Python, some Excel automation

## Next Steps

1. ✅ Complete Phase 0 alignment
2. ✅ Define main idea in one sentence
3. ⏳ Move to Phase 1: Define specific objectives and scope
4. ⏳ Review existing documentation (PDFs) to inform architecture
5. ⏳ Examine test data structure to understand use cases

