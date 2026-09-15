# Copilot Project Init Instructions (peon-cli)

Read this file first at chat start for this repository.

## Startup Checklist
- Read CLAUDE.md in this repository.
- Apply workspace rules from /home/richard/development/.github/copilot-instructions.md.
- Keep changes minimal and repo-local unless the task is explicitly cross-repo.
- Use non-destructive validation first.

## Validation
- Prefer bash -n and help-flag checks for shell changes.

## Deployment Rule
- For deployment or release validation, build updated images from source under /home/richard/development and deploy through /home/richard/peon before sign-off.

## Safety
- Do not request or print secrets.
- Do not edit generated docs outputs directly.
