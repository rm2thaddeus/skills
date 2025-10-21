# Templates & Guides

This directory contains reusable templates and guides for the Promptgramming methodology.

## Available Templates

All phase-specific templates are located in their respective phase directories:

- **Phase 0**: `PROFILE.yaml`, `CONTEXT.md`
- **Phase 1**: `IDEA_NOTE.md`
- **Phase 2**: `POC_PLAN.md`
- **Phase 3**: `PRD.md`, `agents.md`

## Frontmatter Standard

All markdown documents should include frontmatter:

```yaml
---
phase: <0|1|2|3>
artifact: <document_type>
project: Excel In ChatGPT
owner: Aitor
updated: YYYY-MM-DD
sources:
  - <reference_or_link>
links:
  profile: ../Phase0-Alignment/PROFILE.yaml
  context: ../Phase0-Alignment/CONTEXT.md
---
```

## Usage Guidelines

### When Creating New Documents

1. Copy the appropriate phase template
2. Fill in frontmatter with correct metadata
3. Update links to related artifacts
4. Complete required sections
5. Set `updated` field to current date

### When Editing Documents

1. Always update `updated` field
2. Maintain existing frontmatter structure
3. Keep cross-reference links current
4. Add to `sources` if using new references

### When Moving Between Phases

1. Complete checklist in current phase README
2. Review outputs from previous phases
3. Update main project README with phase status
4. Begin new phase with prompt starter

## Prompt Starters Library

### Phase 0: Alignment
```
You are my AI pair programmer. Start Phase 0 (Alignment).

- Ask about my editor, OS, experience, and preferences.
- Infer my prompting expertise and communication style.
- Help me articulate the main project idea in one sentence.

Output: update PROFILE.yaml and CONTEXT.md.
```

### Phase 1: Ideation
```
Move to Phase 1. Refine the idea into structured goals, scope, and assumptions.

Output: fill IDEA_NOTE.md with frontmatter and a clear objective.
```

### Phase 2: POC
```
Move to Phase 2. Research feasibility, architecture options, and dependencies.

Output: populate POC_PLAN.md with findings, candidate stacks, and risks.
```

### Phase 3: MVP
```
Move to Phase 3. Draft PRD acceptance criteria and define agents/personas.

Output: PRD.md and agents.md with checklists and next actions.
```

## Best Practices

1. **Keep It Simple**: Start with minimal content, expand as needed
2. **Stay Consistent**: Use templates for all phase documents
3. **Link Everything**: Cross-reference related artifacts
4. **Update Regularly**: Keep `updated` field current
5. **Version Control**: Commit after completing each phase

## Resources

- [Promptgramming GitHub](https://github.com/rm2thaddeus/promptgramming)
- [Translation Hill Methodology](https://github.com/rm2thaddeus/promptgramming/tree/main/reference/research)

---

**Note**: This template structure is designed for conversational AI-assisted development. Treat each interaction as a step in the compilation process from human intent to working code.


