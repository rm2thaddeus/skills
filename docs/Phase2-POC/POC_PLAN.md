# Proof of Concept Plan

---
phase: 2
artifact: poc_plan
project: Excel In ChatGPT
owner: Aitor
updated: 2025-10-21
sources: []
links:
  profile: ../Phase0-Alignment/PROFILE.yaml
  context: ../Phase0-Alignment/CONTEXT.md
  idea: ../Phase1-Ideation/IDEA_NOTE.md
---

## Critical POC Question

**Can Codex CLI read and execute Claude skills from a repository?**

## Feasibility Assessment

### Technical Feasibility

**Primary Risk**: Codex CLI must be able to discover, read, and utilize Claude skills

**Approach**:
1. Research Codex CLI skill/tool format
2. Define skill structure that Codex can parse
3. Test if Codex can invoke skills
4. Validate with test data (Excel files)

**Confidence Level**: TBD after spikes

### Resource Feasibility

- **Time**: Moderate - need to learn Codex skill format
- **Skills**: Python development, understanding Codex CLI capabilities
- **Infrastructure**: Local development, Codex CLI access

## Architecture Overview

### System Components

1. **Skills Repository**: Directory structure containing Claude skills
2. **Skill Definitions**: Format/structure for defining skills (JSON/YAML/Python?)
3. **Bureaucratic Skills**: Skills for bureaucratic task processing
4. **Document Handling Skills**: Skills for document processing
5. **Skill Template**: Boilerplate for creating new skills
6. **Test Suite**: Excel test data to validate skill outputs

### Skill Structure (Initial Concept)

```
skills/
├── bureaucratic/
│   ├── skill_definition.yaml
│   └── implementation.py
├── document_handling/
│   ├── skill_definition.yaml
│   └── implementation.py
├── template/
│   ├── skill_template.yaml
│   └── template.py
└── README.md
```

### Data Flow

```
User Command (Codex CLI)
  → Codex reads skill from repository
  → Claude executes skill logic
  → Skill processes input (e.g., Excel file)
  → Outputs result
  → Validate against test data
```

## Technical Spikes

### Spike 1: Codex CLI Skill Format Research

- **Objective**: Understand how Codex CLI discovers and uses skills
- **Questions to Answer**: 
  - What format does Codex expect? (MCP tools? Custom format?)
  - How are skills discovered?
  - How are they invoked?
  - What metadata is required?
- **Time Box**: 1 hour
- **Findings**: ✅ **COMPLETE**
  - Codex CLI uses `AGENTS.md` files for skill definitions
  - Files can be in: home dir (`~/.codex/AGENTS.md`), repo root, or subdirectories
  - Codex merges files top-down to build context
  - Format: Markdown with sections for overview, capabilities, usage, examples
  - No special metadata required - plain markdown

### Spike 2: Skill Definition Structure

- **Objective**: Design skill definition format
- **Questions to Answer**:
  - What information does a skill need?
  - How to define inputs/outputs?
  - How to document usage?
  - Best format (YAML/JSON/Python)?
- **Time Box**: 30 minutes
- **Findings**: ✅ **COMPLETE**
  - Created standard AGENTS.md template with sections:
    - Overview & capabilities
    - Setup & prerequisites
    - Usage examples (basic & advanced)
    - Code style & patterns
    - Testing & validation
    - Input/output specs
    - Security & data handling
    - Troubleshooting
  - Format: Markdown (AGENTS.md) - no YAML/JSON needed
  - Template created at `skills/template/AGENTS.md`

### Spike 3: Bureaucratic Skill Prototype

- **Objective**: Create first working bureaucratic skill
- **Questions to Answer**:
  - What bureaucratic tasks to target?
  - Can Claude execute the skill logic?
  - Does it work via Codex CLI?
- **Time Box**: 1 hour
- **Findings**: ✅ **COMPLETE**
  - Created `skills/bureaucratic/AGENTS.md`
  - Targets: form validation, compliance checks, data completeness, normalization
  - Includes code patterns for:
    - Required field validation
    - Date format standardization
    - ID format validation
    - Completeness reporting
  - Ready for testing with recruitment data
  - Pending: Actual Codex CLI execution test

### Spike 4: Document Handling Skill Prototype

- **Objective**: Create document handling skill
- **Questions to Answer**:
  - What document operations to include?
  - How to handle different formats (Excel, PDF, etc.)?
  - Integration with test data?
- **Time Box**: 1 hour
- **Findings**: ✅ **COMPLETE**
  - Created `skills/document_handling/AGENTS.md`
  - Operations: load, extract, convert, merge, split, visualize
  - Formats: Excel, CSV, JSON (extensible)
  - Includes patterns for:
    - Multi-sheet Excel handling
    - Format conversion
    - Data filtering/extraction
    - Document merging
    - Chart generation
  - Ready for testing with Excel test data
  - Pending: Actual Codex CLI execution test

### Spike 5: Test Data Validation

- **Objective**: Use Excel test data to validate skill outputs
- **Questions to Answer**:
  - How to measure skill effectiveness?
  - What metrics to track?
  - How to automate validation?
- **Time Box**: 30 minutes
- **Findings**: _TBD_

## Dependencies

### External Tools/Services

- Codex CLI environment
- Claude API (via Codex)
- Python 3.8+

### Libraries/Frameworks

- pandas (for test data validation)
- openpyxl (for Excel test files)
- PyYAML or similar (for skill definitions)

### Development Tools

- Text editor (Cursor)
- Git (for version control)
- Python virtual environment

## Research Notes

### Key Questions

1. **Codex Skill Format**: Does Codex have a native skill/tool format? Or do we define our own?
2. **Skill Discovery**: How does Codex find skills in a repository?
3. **Bureaucratic Tasks**: What specific bureaucratic operations to implement?
4. **Document Handling**: What document types and operations?
5. **Template Design**: What makes a good skill template?

### References

- Codex CLI documentation (if available)
- MCP (Model Context Protocol) tools format
- Claude function calling patterns
- Existing skill/tool repositories

## Risk Analysis

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Codex can't read custom skill format | High | Research Codex native formats, use MCP if needed | Open |
| Skills too complex for Claude | Medium | Keep skills focused and well-documented | Open |
| Test data insufficient | Low | Add more test cases as needed | Open |
| Template not flexible enough | Medium | Iterate based on user feedback | Open |

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| 2025-10-21 | Focus on skills repository vs data analysis tool | User clarification - Excel is test data, not primary focus | Data analysis toolkit |
| 2025-10-21 | Need bureaucratic + document handling skills | User requirement | Other skill domains |

## Initial Implementation Plan

### Phase 2.1: Research & Design
- [ ] Research Codex CLI skill format
- [ ] Design skill definition structure
- [ ] Define bureaucratic skill scope
- [ ] Define document handling skill scope

### Phase 2.2: Prototype Skills
- [ ] Create skill template
- [ ] Implement bureaucratic skill
- [ ] Implement document handling skill
- [ ] Test with Excel data

### Phase 2.3: Validation
- [ ] Validate Codex can read skills
- [ ] Test skill execution
- [ ] Measure outputs against test data
- [ ] Document findings

## POC Status: Phase 2 Complete ✅

### Completed
1. ✅ Researched Codex CLI skill format (AGENTS.md at root)
2. ✅ Designed skill architecture (AGENTS.md guides, Python implements)
3. ✅ Created skill template (`skills/template/`)
4. ✅ Designed bureaucratic skill structure (`skills/bureaucratic/`)
5. ✅ Designed document handling skill structure (`skills/document_handling/`)
6. ✅ Created requirements.txt with dependencies
7. ✅ Separated concerns: AGENTS.md (when to use) vs src/ (implementation)

### Pending Validation
1. ⏳ Test skills with actual Codex CLI
2. ⏳ Validate with Excel test data
3. ⏳ Measure skill execution accuracy
4. ⏳ Refine based on test results

### Next Phase
Ready to move to **Phase 3 (MVP)** to:
- Test skills with Codex CLI
- Refine based on real usage
- Create integration examples
- Document best practices
- Finalize for production use
