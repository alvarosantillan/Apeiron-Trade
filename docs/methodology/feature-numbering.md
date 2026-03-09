# Feature Numbering Guide (Spec Kit)

Use this guide before running `/speckit.specify` to avoid duplicate feature numbers.

## Rule

- Feature branches and folders MUST be sequential and unique.
- Current format: `NNN-short-name` (example: `009-persistence-hardening`).

## Manual Steps (Always)

1. Fetch latest refs:
   - `git fetch --all --prune`
2. Choose short name (2-4 words):
   - example: `persistence-hardening`
3. Search highest number in three sources:
   - Remote branches: `git ls-remote --heads origin`
   - Local branches: `git branch --format "%(refname:short)"`
   - Specs folders: `specs/*`
4. Use next number `max + 1`.
5. Create feature only once with that number.

## PowerShell Helper (example)

```powershell
$short = "persistence-hardening"
$remote = git ls-remote --heads origin | Select-String -Pattern "refs/heads/[0-9]+-$short$" | ForEach-Object { if ($_ -match 'refs/heads/([0-9]+)-') { [int]$matches[1] } }
$local = git branch --format "%(refname:short)" | Select-String -Pattern "^[0-9]+-$short$" | ForEach-Object { if ($_ -match '^([0-9]+)-') { [int]$matches[1] } }
$specs = Get-ChildItem specs -Directory | Select-Object -ExpandProperty Name | Select-String -Pattern "^[0-9]+-$short$" | ForEach-Object { if ($_ -match '^([0-9]+)-') { [int]$matches[1] } }
$all = @($remote)+@($local)+@($specs) | Where-Object { $_ -ne $null }
$next = if ($all.Count -eq 0) { 1 } else { (($all | Measure-Object -Maximum).Maximum + 1) }
$next
```

## Checklist Before Starting Implementation

- Branch name matches feature folder name.
- `spec.md` exists and uses the correct feature number.
- Checklist file exists under `checklists/requirements.md`.
- Only after this: run `/speckit.plan` and `/speckit.tasks`.
