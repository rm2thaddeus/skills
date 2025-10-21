# Architecture Decision Record - Skills vs AGENTS.md

## Date
2025-10-21

## Status
✅ Accepted

## Context

Initial POC design mixed AGENTS.md files with skill implementations, placing AGENTS.md files inside each skill directory. This created confusion about the role and responsibility of AGENTS.md files.

### Problem
- **Unclear separation**: Was AGENTS.md the skill itself or documentation?
- **Redundancy**: Skills documentation duplicated in AGENTS.md
- **Scalability**: As skills grow, mixing guidance with implementation becomes unwieldy

## Decision

**Separate AGENTS.md (guidance) from Skills (implementation)**

### New Architecture

```
Root AGENTS.md (Single file)
    ↓ Guides Claude on WHEN to use skills
    ↓ Points to skill directories
    
skills/[skill_name]/README.md
    ↓ Documents WHAT the skill does
    ↓ Describes modules and usage
    
skills/[skill_name]/src/*.py
    ↓ Implements HOW the skill works
    ↓ Python code that executes tasks
```

### Structure
```
Excel In ChatGPT/
├── AGENTS.md                    ⭐ Orchestrator (WHEN)
└── skills/
    ├── bureaucratic/
    │   ├── README.md            📄 Documentation (WHAT)
    │   └── src/
    │       └── *.py             🐍 Implementation (HOW)
    ├── document_handling/
    │   ├── README.md
    │   └── src/
    │       └── *.py
    └── template/
        ├── README.md
        └── src/
            └── *.py
```

## Rationale

### 1. Single Responsibility Principle
- **AGENTS.md**: Orchestration - tells Claude which skill to use
- **README.md**: Documentation - describes the skill
- **src/*.py**: Implementation - executes the skill

### 2. Discoverability
- Codex reads root AGENTS.md first
- AGENTS.md directs Claude to appropriate skill
- Claude reads skill README.md for details
- Claude executes skill src/ code

### 3. Maintainability
- Update skill implementation without touching AGENTS.md
- Add new skills by updating one file (root AGENTS.md)
- Clear ownership and responsibility for each component

### 4. Scalability
- Root AGENTS.md stays manageable even with many skills
- Each skill is self-contained with docs and code
- Easy to add/remove/modify skills independently

## Consequences

### Positive
✅ Clear separation of concerns  
✅ Easy to understand information flow  
✅ Scalable to many skills  
✅ Reduced duplication  
✅ Better maintainability  
✅ Follows Unix philosophy (do one thing well)  

### Negative
⚠️ Requires discipline to maintain separation  
⚠️ Three layers to understand (AGENTS → README → src)  

### Neutral
- Root AGENTS.md becomes the "table of contents"
- Skills are self-documenting via README.md
- Implementation details hidden in src/

## Implementation

### Changes Made
1. ✅ Created root `AGENTS.md` as single orchestrator
2. ✅ Removed `AGENTS.md` from skill directories
3. ✅ Created `README.md` in each skill directory for documentation
4. ✅ Moved implementation to `src/` subdirectories
5. ✅ Updated all references throughout project
6. ✅ Created `ARCHITECTURE.md` documenting this design

### File Changes
- **Deleted**: `skills/*/AGENTS.md` (3 files)
- **Created**: Root `AGENTS.md` (1 file)
- **Created**: `skills/*/README.md` (3 files)
- **Created**: `skills/*/src/__init__.py` (3 files)
- **Updated**: All documentation references

## Example Flow

### User Request
```bash
codex "validate recruitment data for compliance"
```

### Execution Flow
1. **Codex reads**: Root `AGENTS.md`
   - Identifies: "bureaucratic" skill needed
   - Location: `skills/bureaucratic/`

2. **Claude reads**: `skills/bureaucratic/README.md`
   - Understands: Form validation capabilities
   - Modules: `bureaucratic_validator.py`

3. **Claude reads**: `skills/bureaucratic/src/bureaucratic_validator.py`
   - Finds: `validate_form()` function
   - Understands: Parameters and return format

4. **Claude executes**: Python code
   ```python
   result = validate_form("Data/recruitment.xlsx")
   ```

5. **Returns**: Standardized output
   ```json
   {"status": "success", "data": {...}}
   ```

## Alternatives Considered

### Alternative 1: AGENTS.md per skill
**Pros**: Self-contained skills  
**Cons**: Confusion about AGENTS.md role, harder for Codex to discover  
**Rejected**: Mixes guidance with implementation

### Alternative 2: No AGENTS.md, only README
**Pros**: Simpler structure  
**Cons**: No orchestration layer, Claude must guess which skill  
**Rejected**: Lacks clear entry point for Codex

### Alternative 3: Configuration file (YAML/JSON)
**Pros**: Machine-readable  
**Cons**: Less readable for humans, requires parsing  
**Rejected**: Codex works better with markdown

## Validation

### Success Criteria
- ✅ Root AGENTS.md exists and guides Claude
- ✅ Each skill has README.md with documentation
- ✅ Each skill has src/ with implementation
- ✅ No duplicate content between layers
- ✅ Clear information flow from request to execution

### Testing
- Pending Phase 3: Actual Codex CLI execution
- Structure validated: ✅
- Documentation updated: ✅
- Examples provided: ✅

## References

- Main AGENTS.md: `/AGENTS.md`
- Architecture doc: `/ARCHITECTURE.md`
- POC Plan: `/docs/Phase2-POC/POC_PLAN.md`
- Skills README: `/skills/README.md`

## Notes

This architecture decision was made during Phase 2 POC based on user feedback that "mixing AGENTS.md and skills isn't wise." The user correctly identified that AGENTS should be used to help Claude know WHEN to read skills, not BE the skills themselves.

This represents a significant improvement in the architecture and sets up a clean foundation for Phase 3 MVP implementation.

---

**Decision Made By**: Aitor (user feedback)  
**Implemented By**: Claude (AI assistant)  
**Date**: 2025-10-21  
**Phase**: 2 (POC)  
**Status**: Implemented and Documented

