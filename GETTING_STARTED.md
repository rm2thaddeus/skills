# Getting Started with Excel In ChatGPT

Welcome! This guide will help you begin your AI-assisted development journey using the Promptgramming methodology.

## 🚀 Quick Start

### Step 1: Start Phase 0 (Alignment)

Copy and paste this prompt to your AI assistant:

```
You are my AI pair programmer. Start Phase 0 (Alignment).

- Ask about my editor, OS, experience, and preferences.
- Infer my prompting expertise and communication style.
- Help me articulate the main project idea in one sentence.

Output: update docs/Phase0-Alignment/PROFILE.yaml and CONTEXT.md.
```

**Time box**: 5-10 minutes

### Step 2: Review Existing Documentation

Before moving forward, review the materials in:
- `Resources/Documentation/Excel automation prd.pdf`
- `Resources/Documentation/Excel automation with Python.pdf`

This will help clarify your project requirements.

### Step 3: Examine Test Data

Look at the Excel files in `Data/` directory:
- Test recruitment data files
- Example outputs (charts in `Resources/Images/`)

Understand what data you're working with.

### Step 4: Move to Phase 1 (Ideation)

Once Phase 0 is complete, use this prompt:

```
Move to Phase 1. Refine the idea into structured goals, scope, and assumptions.

Output: fill docs/Phase1-Ideation/IDEA_NOTE.md with frontmatter and a clear objective.
```

## 📁 Project Structure Overview

```
Excel In ChatGPT/
│
├── README.md                      # Project overview
├── GETTING_STARTED.md             # This file
├── .gitignore                     # Git ignore rules
│
├── docs/                          # 📚 All documentation
│   ├── Phase0-Alignment/          # ✅ START HERE
│   │   ├── PROFILE.yaml          # Your profile & preferences
│   │   ├── CONTEXT.md            # Project context
│   │   └── README.md             # Phase 0 guide
│   │
│   ├── Phase1-Ideation/           # 💡 Define goals
│   │   ├── IDEA_NOTE.md          # Refined requirements
│   │   └── README.md             # Phase 1 guide
│   │
│   ├── Phase2-POC/                # 🔬 Validate approach
│   │   ├── POC_PLAN.md           # Research & architecture
│   │   └── README.md             # Phase 2 guide
│   │
│   ├── Phase3-MVP/                # 🚀 Build it
│   │   ├── PRD.md                # Product requirements
│   │   ├── agents.md             # AI agent roles
│   │   └── README.md             # Phase 3 guide
│   │
│   ├── templates/                 # 📋 Reusable templates
│   │   └── README.md             # Template guide
│   │
│   └── .cursor/rules/             # 📏 Development rules
│       └── project-guidelines.mdc
│
├── Code/                          # 💻 Implementation
│   ├── Backend/                   # Server-side code
│   └── Frontend/                  # Client-side code
│
├── Data/                          # 📊 Excel files (6 files)
│   ├── Aitor- Patino (1).xlsx
│   └── Test_Excel_Recrutement_*.xlsx
│
└── Resources/                     # 📦 Supporting materials
    ├── Documentation/             # PDFs (2 files)
    │   ├── Excel automation prd.pdf
    │   └── Excel automation with Python.pdf
    ├── Images/                    # Charts (3 files)
    │   ├── chart_coverage.png
    │   ├── chart_modes_region.png
    │   └── chart_monthly_visits.png
    └── excel_automation.zip       # Archive
```

## 🎯 The Four Phases

### Phase 0: Alignment (5-10 min)
**Goal**: Understand who you are and what you want to build

**Activities**:
- Define your technical background
- Clarify collaboration preferences
- Articulate the core idea

**Output**: Filled `PROFILE.yaml` and `CONTEXT.md`

---

### Phase 1: Ideation (15-30 min)
**Goal**: Transform idea into structured requirements

**Activities**:
- Set clear objectives
- Define success metrics
- Identify scope and constraints
- List risks and assumptions

**Output**: Complete `IDEA_NOTE.md`

---

### Phase 2: POC (1-3 hours)
**Goal**: Validate technical feasibility

**Activities**:
- Research architecture options
- Select technology stack
- Run technical spikes (time-boxed experiments)
- Create proof of concept

**Output**: Detailed `POC_PLAN.md` and prototype code

---

### Phase 3: MVP (Varies)
**Goal**: Build minimal viable product

**Activities**:
- Write detailed PRD
- Coordinate AI agent roles
- Implement features
- Test and document

**Output**: Working code, tests, documentation

## 💡 Key Concepts

### Frontmatter
Every document includes metadata at the top:
```yaml
---
phase: 0
artifact: context
project: Excel In ChatGPT
owner: Aitor
updated: 2025-10-21
---
```

**Always update the `updated` field when editing!**

### Context Carrying
Documents link to related artifacts:
```yaml
links:
  profile: ../Phase0-Alignment/PROFILE.yaml
  context: ../Phase0-Alignment/CONTEXT.md
```

### Progressive Disclosure
Start simple, add detail as needed:
- **Level 1**: Basic prompt starters
- **Level 2**: Guided questions
- **Level 3**: Detailed specifications

### Iterative Refinement
Make small changes, validate frequently:
1. Make targeted edit
2. Check against acceptance criteria
3. Update documentation
4. Move to next item

## 🛠️ Development Workflow

### Daily Development

1. **Check Current Phase**
   - Read main README to see where you are
   - Review current phase README

2. **Review Context**
   - Read linked documents in frontmatter
   - Understand what's been done

3. **Make Changes**
   - Use AI agents for specific tasks
   - Keep edits small and focused
   - Update timestamps

4. **Document Progress**
   - Check off completed items
   - Update phase documents
   - Note decisions and learnings

### Moving Between Phases

1. Complete checklist in current phase
2. Review outputs
3. Update main README
4. Start next phase with prompt starter

## 🤖 AI Agent System

In Phase 3, you'll work with specialized AI agents:

- **🏗️ Architect**: System design, technical decisions
- **💻 Backend Developer**: Server-side implementation
- **🎨 Frontend Developer**: User interface
- **🧪 QA Engineer**: Testing and quality
- **📚 Documentation**: Guides and docs

Each agent has specific roles and prompt starters in `docs/Phase3-MVP/agents.md`.

## 📖 Additional Resources

- **Project Guidelines**: `docs/.cursor/rules/project-guidelines.mdc`
- **Template Guide**: `docs/templates/README.md`
- **Promptgramming GitHub**: https://github.com/rm2thaddeus/promptgramming

## ❓ Common Questions

**Q: Can I skip phases?**  
A: You can, but each phase builds on the previous. Skipping may miss important context.

**Q: How long should each phase take?**  
A: Phase 0: 5-10 min, Phase 1: 15-30 min, Phase 2: 1-3 hours, Phase 3: varies by scope.

**Q: Can I go back to previous phases?**  
A: Absolutely! Iterate as needed. Just update the frontmatter dates.

**Q: What if I already know what I want to build?**  
A: Still do Phase 0-1 quickly. The structure helps AI assistants understand your context better.

## ✅ Your First Action

**Right now, copy this prompt and start Phase 0:**

```
You are my AI pair programmer. Start Phase 0 (Alignment).

- Ask about my editor, OS, experience, and preferences.
- Infer my prompting expertise and communication style.
- Help me articulate the main project idea in one sentence.

Output: update docs/Phase0-Alignment/PROFILE.yaml and CONTEXT.md.
```

---

**Happy Coding!** 🎉

If you get stuck, refer to the README files in each phase directory for guidance.


