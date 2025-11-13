# Contributing

## Submodule Policy

The `Code/anthropic-skills` submodule is pinned to a specific commit to ensure reproducible behavior across clones. Do not update it on consumer clones.

To bump the submodule (maintainers only):
```bash
cd Code/anthropic-skills
git fetch
git checkout <new-commit>
cd ..
git add Code/anthropic-skills
git commit -m "chore(skills): bump submodule to <shortsha>"
```

## Validating Artifacts

GitHub Actions validate `artifacts/operations/*/audit.json` against `schemas/audit.schema.json`. You can run local checks with:
```bash
npm i -g ajv-cli
ajv validate -s schemas/audit.schema.json -d artifacts/operations/<op>/audit.json
```

## Creating Operations

Use the helper script:
```bash
tools/op new my-task
tools/op approve <operation_id>   # gate writes to output/
tools/op validate <operation_id>  # schema validation
```

## Code of Conduct

Respect privacy, avoid committing PII, and prefer redaction in logs.

