# AI Agents & Roles

---
phase: 3
artifact: agents
project: Excel In ChatGPT
owner: Aitor
updated: 2025-10-21
links:
  prd: ./PRD.md
---

## Agent Coordination

This document defines AI agent roles, personas, and coordination patterns for implementing the MVP.

## Agent Roles

### 🏗️ Architect Agent

**Responsibility**: System design, architecture decisions, technical strategy

**Persona**: Senior software architect with expertise in distributed systems and API design

**Tasks**:
- [ ] Review and refine architecture from POC
- [ ] Define service boundaries
- [ ] Establish coding standards
- [ ] Create technical documentation

**Consultation Required For**:
- Major architectural changes
- Technology stack modifications
- Performance optimization strategies

---

### 💻 Backend Developer Agent

**Responsibility**: Server-side implementation, APIs, business logic

**Persona**: Backend developer specializing in Python and API development

**Tasks**:
- [ ] Implement API endpoints
- [ ] Create data models
- [ ] Handle Excel file processing
- [ ] Integrate ChatGPT API
- [ ] Write backend tests

**Dependencies**:
- Architecture decisions from Architect Agent
- API contracts from PRD

---

### 🎨 Frontend Developer Agent

**Responsibility**: User interface, client-side logic, UX implementation

**Persona**: Frontend developer focused on modern UI/UX

**Tasks**:
- [ ] Build user interface
- [ ] Implement file upload/download
- [ ] Create data visualization
- [ ] Handle user interactions
- [ ] Write frontend tests

**Dependencies**:
- API contracts from Backend Developer Agent
- UX designs from POC_PLAN

---

### 🧪 QA Engineer Agent

**Responsibility**: Testing strategy, quality assurance, bug identification

**Persona**: QA engineer with automation expertise

**Tasks**:
- [ ] Create test plans
- [ ] Write automated tests
- [ ] Perform integration testing
- [ ] Document bugs and issues
- [ ] Validate acceptance criteria

**Dependencies**:
- Completed features from Developer Agents
- Acceptance criteria from PRD

---

### 📚 Documentation Agent

**Responsibility**: User documentation, API docs, setup guides

**Persona**: Technical writer specializing in developer documentation

**Tasks**:
- [ ] Write README.md
- [ ] Create setup instructions
- [ ] Document API endpoints
- [ ] Write user guides
- [ ] Maintain changelog

**Dependencies**:
- Implementation details from all agents

---

## Coordination Protocol

### Daily Workflow

1. **Planning**: Review PRD and current sprint goals
2. **Implementation**: Agents work on assigned tasks
3. **Integration**: Coordinate on dependencies
4. **Review**: Check progress against acceptance criteria
5. **Documentation**: Update relevant docs

### Communication Pattern

```
User Request → Architect (high-level plan)
            → Backend/Frontend (implementation)
            → QA (testing)
            → Documentation (docs)
            → User Delivery
```

### Handoff Checklist

When passing work between agents:

- [ ] All acceptance criteria met
- [ ] Code follows project standards
- [ ] Tests are passing
- [ ] Documentation is updated
- [ ] Dependencies are documented

## Prompt Starters

### Architect Agent

```
You are the Architect Agent for this Excel automation project.
Review the POC_PLAN.md and PRD.md, then:
1. Validate the technical approach
2. Define service boundaries
3. Establish coding standards
4. Identify technical risks
```

### Backend Developer Agent

```
You are the Backend Developer Agent.
Implement the server-side components according to PRD.md:
1. Create API endpoints
2. Implement Excel processing logic
3. Integrate ChatGPT API
4. Write tests for your code
```

### Frontend Developer Agent

```
You are the Frontend Developer Agent.
Build the user interface according to PRD.md:
1. Create file upload interface
2. Display processing results
3. Implement data visualizations
4. Ensure responsive design
```

## Next Actions

1. Start with Architect Agent to validate approach
2. Implement core backend functionality
3. Build frontend interface
4. Integrate and test
5. Document and deploy


