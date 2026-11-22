# Cards (fixture)

The card format the gate reads in the fixture tree.

## Kinds

- **Kinds:** config, habit, belief
- **Index line limit:** 12

## Fields

| Field | Where | Kinds | Meaning |
|---|---|---|---|
| `kind` | frontmatter | all | The kind. |
| `why` | frontmatter | all | Why it matters. |
| `applies_when` | frontmatter | all | When it applies. |
| `last_reviewed` | frontmatter | all | The last review date. |
| `Check` | section | all | How to check. |
| `Fix` | section | config | How to fix. |
| `Learn` | section | all | Links. |
| `Evidence for` | section | all | Dated bullets. |
| `Evidence against` | section | all | Dated bullets. |
| `Guards` | section | optional | Class doc links. |
