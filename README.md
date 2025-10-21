# Excel In ChatGPT

> A repository of Claude skills for Codex CLI - solving data analysis and document processing problems

## Project Status

**Current Phase**: Phase 2 - POC (Proof of Concept) Complete ✅

**Next**: Ready for Phase 3 (MVP) - Testing and refinement

## Quick Start

### For First-Time Setup

Start your AI-assisted development journey by running through Phase 0:

```
You are my AI pair programmer. Start Phase 0 (Alignment).

- Ask about my editor, OS, experience, and preferences.
- Infer my prompting expertise and communication style.
- Help me articulate the main project idea in one sentence.

Output: update docs/Phase0-Alignment/PROFILE.yaml and CONTEXT.md.
```

### Project Structure

```
Excel In ChatGPT/
├── docs/                          # Project documentation & planning
│   ├── Phase0-Alignment/          # User profile & project context
│   ├── Phase1-Ideation/           # Goals, scope, and requirements
│   ├── Phase2-POC/                # Research & architecture
│   ├── Phase3-MVP/                # Implementation & delivery
│   ├── templates/                 # Reusable templates
│   └── .cursor/rules/             # Development guidelines
├── Code/                          # Implementation
│   ├── Backend/                   # Server-side code
│   └── Frontend/                  # Client-side code
├── Data/                          # Excel files and test data
├── Resources/                     # Supporting materials
│   ├── Documentation/             # PDFs and guides
│   └── Images/                    # Charts and visuals
└── README.md                      # This file
```

## About This Template

This project uses the **Promptgramming / Translation Hill** methodology, which structures AI-assisted development into four phases:

### 📋 Phase 0: Alignment
**Purpose**: Establish collaboration norms and define the main idea  
**Outputs**: User profile, project context  
**Time**: 5-10 minutes

[→ Start Phase 0](docs/Phase0-Alignment/README.md)

### 💡 Phase 1: Ideation
**Purpose**: Refine goals, scope, and assumptions  
**Outputs**: Structured idea note with objectives and metrics  

[→ View Phase 1](docs/Phase1-Ideation/README.md)

### 🔬 Phase 2: POC (Proof of Concept)
**Purpose**: Research feasibility and validate architecture  
**Outputs**: POC plan, technical spikes, architecture decisions  

[→ View Phase 2](docs/Phase2-POC/README.md)

### 🚀 Phase 3: MVP (Minimum Viable Product)
**Purpose**: Implement and deliver working prototype  
**Outputs**: PRD, working code, tests, documentation  

[→ View Phase 3](docs/Phase3-MVP/README.md)

## 🎯 What This Repository Provides

### Claude Skills for Codex CLI (Anthropic Skills Format)

**Based on [Anthropic's Official Skills Spec](https://github.com/anthropics/skills)**

**Three production-ready skills:**

1. **[Bureaucratic Processing](skills/bureaucratic/SKILL.md)**
   - Form validation & compliance checking
   - Data completeness verification
   - Administrative workflows
   
2. **[Document Handling](skills/document_handling/SKILL.md)**
   - Excel/CSV/JSON processing
   - Format conversion & data extraction
   - Document merging & chart generation

3. **[Skill Template](skills/template/SKILL.md)**
   - Official Anthropic format template
   - YAML frontmatter structure
   - Best practices guide

**Quick Usage:**
```bash
# Validate bureaucratic compliance
codex "validate Data/Test_Excel_Recrutement_v3.0.xlsx for compliance"

# Convert document format
codex "convert Data/Aitor-Patino.xlsx to CSV"

# Create new skill (Anthropic format)
cp -r skills/template skills/my_skill
```

[→ See all skills](skills/README.md)

---

## Current Assets

### Skills Repository (Anthropic Format)
- ✅ Bureaucratic processing skill
- ✅ Document handling skill  
- ✅ Skill template (official format)
- ✅ Anthropic's official skills cloned for reference (`Code/anthropic-skills/`)
- ✅ Complete documentation

### Test Data
- 6 Excel files with recruitment data
- Chart outputs for validation
- Sample personal data file

### Documentation
- Product requirements (PDF)
- Python automation guide (PDF)
- Phase-based development docs
- Skill usage examples

## Methodology

This project follows the **Translation Hill** framework:

1. **Context-Carrying**: Each document includes frontmatter linking to related artifacts
2. **Progressive Disclosure**: Start simple, add detail as needed
3. **Iterative Refinement**: Small edits with clear acceptance criteria
4. **Role-Based Agents**: Specialized AI personas for different tasks

## How to Use This Template

1. **Start with Alignment** (Phase 0)
   - Complete `PROFILE.yaml` with your details
   - Define the main project idea in `CONTEXT.md`

2. **Refine Your Idea** (Phase 1)
   - Set clear objectives and success metrics
   - Define scope and identify risks

3. **Validate Feasibility** (Phase 2)
   - Research technical approaches
   - Run time-boxed spikes
   - Select technology stack

4. **Build MVP** (Phase 3)
   - Implement core features
   - Write tests and documentation
   - Deliver working prototype

## Next Steps

1. ✅ Template structure created
2. ✅ Files organized  
3. ✅ Phase 0 (Alignment) - Complete
4. ✅ Phase 1 (Ideation) - Complete
5. ✅ Phase 2 (POC) - Complete
6. ⏳ **Phase 3 (MVP)** - Test skills with Codex CLI
7. ⏳ Refine based on actual usage
8. ⏳ Create integration examples
9. ⏳ Finalize for production

## Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills) ⭐ Official format we follow
- [Agent Skills Spec](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)
- [Promptgramming Template](https://github.com/rm2thaddeus/promptgramming)
- [Translation Hill Methodology](https://github.com/rm2thaddeus/promptgramming/tree/main/reference/research)

## Contributing

This is a personal project using AI-assisted development. The workflow emphasizes:
- Clear, conversational prompts
- Structured artifacts with frontmatter
- Iterative, checkpoint-based progress
- Context preservation across sessions

---

**Last Updated**: 2025-10-21  
**Owner**: Aitor  
**Template Version**: Promptgramming v1.0


