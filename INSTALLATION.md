# Installation Guide — Pasadu standalone skill

Pasadu is a standalone Agent Skill for Thai government procurement and public supplies law. The installable skill lives at `skills/pasadu/` and contains its own instructions, legal references, retrieval scripts, and search index. It does not require custom subagents or platform-specific agent configuration.

Repository: <https://github.com/RobbyGrean/PassaduAIagent>

## Quick start for ordinary Windows users

Node.js, npm, and Git are not required. Open a new Codex task and paste the complete text from
[`newbie user guide/prompt.txt`](<./newbie user guide/prompt.txt>). Codex will download a ZIP over
HTTPS, inspect the included installer, copy the standalone skill into the current user's global
Codex skill directory, and verify the runtime files.

This is the recommended path for non-technical users.

## Skills CLI option

Use this option when Node.js/npm is already installed.

### Windows PowerShell

```powershell
npx.cmd --yes skills@latest add RobbyGrean/PassaduAIagent `
  --skill pasadu --agent codex --global --copy --yes
```

For Claude Code, replace `codex` with `claude-code`. To install for both:

```powershell
npx.cmd --yes skills@latest add RobbyGrean/PassaduAIagent `
  --skill pasadu --agent codex claude-code --global --copy --yes
```

### macOS and Linux

```bash
npx --yes skills@latest add RobbyGrean/PassaduAIagent \
  --skill pasadu --agent codex --global --copy --yes
```

## What gets installed

Skills CLI discovers `skills/pasadu/SKILL.md` and copies only the standalone skill directory:

```text
pasadu/
├── SKILL.md
├── pasadu.md
├── agents/openai.yaml
├── reference/
│   ├── law/
│   └── circulars/
├── scripts/pasadu/
└── data/
    ├── index/
    └── release.json
```

Development files such as repository documentation, screenshots, tests, evals, and platform-specific project instructions are not installed as part of the skill.

## Global installation paths

| Host | User-level path |
|---|---|
| Codex | `~/.agents/skills/pasadu/` |
| Claude Code | `~/.claude/skills/pasadu/` |
| Gemini CLI | `~/.gemini/skills/pasadu/` |

On Windows, `~` means `%USERPROFILE%`.

## Verify the installation

### Skills CLI

```powershell
npx.cmd --yes skills@latest list --global --json
```

The output must contain a skill named `pasadu` with scope `global`.

### Codex on Windows

```powershell
$pasaduPath = "$env:USERPROFILE\.agents\skills\pasadu"
Test-Path "$pasaduPath\SKILL.md"
Test-Path "$pasaduPath\pasadu.md"
Test-Path "$pasaduPath\reference\law\prb60.md"
Test-Path "$pasaduPath\reference\law\rbb60.md"
Test-Path "$pasaduPath\reference\law\rbb60-3.md"
Test-Path "$pasaduPath\scripts\pasadu\evidence_packet.py"
Test-Path "$pasaduPath\data\index\chunks.json"
Get-Content "$pasaduPath\data\release.json"
```

Every `Test-Path` command must return `True`, and `release.json` must contain valid release metadata.

### Claude Code on Windows

```powershell
$pasaduPath = "$env:USERPROFILE\.claude\skills\pasadu"
Test-Path "$pasaduPath\SKILL.md"
Test-Path "$pasaduPath\pasadu.md"
Test-Path "$pasaduPath\reference\law\prb60.md"
Test-Path "$pasaduPath\scripts\pasadu\evidence_packet.py"
```

Every command must return `True`.

If the top-level skills directory did not exist when the host started, restart the host once after installation.

## AI-assisted fallback installation

Keep this fallback for users who cannot complete the Skills CLI flow. Give the destination AI
[`newbie user guide/prompt.txt`](<./newbie user guide/prompt.txt>) and ask it to perform the
installation, not merely explain the commands.

The AI does not need to install Node.js, npm, or Git. It can download the repository ZIP into a
temporary directory with built-in Windows PowerShell, inspect the installer, and run it:

```powershell
$workPath = Join-Path $env:TEMP ("pasadu-" + [guid]::NewGuid().ToString("N"))
$zipPath = Join-Path $workPath "pasadu.zip"
New-Item -ItemType Directory -Path $workPath | Out-Null
Invoke-WebRequest `
  -Uri "https://github.com/RobbyGrean/PassaduAIagent/archive/refs/heads/main.zip" `
  -OutFile $zipPath
Expand-Archive -LiteralPath $zipPath -DestinationPath $workPath
Set-Location (Join-Path $workPath "PassaduAIagent-main")
Get-Content .\scripts\install-pasadu.ps1
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\install-pasadu.ps1 -Agent codex
```

Use `claude-code` or `gemini-cli` instead of `codex` for another host. Multiple hosts are valid:

```powershell
& .\scripts\install-pasadu.ps1 -Agent codex,claude-code
```

The installer validates the source and destination, copies only `skills/pasadu`, stages the new
copy before switching it into place, and preserves the prior Pasadu installation as a timestamped
backup. It refuses to replace a destination whose `SKILL.md` does not declare `name: pasadu`.

Git clone remains an optional developer alternative. Do not pipe a remote script directly into
PowerShell.

## Use Pasadu

Pasadu supports automatic activation from procurement-law intent. A user can normally ask:

```text
วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด กรุณาอ้างตัวบท
```

Explicit invocation:

```text
Codex:       $pasadu มาตรา 56 กล่าวถึงอะไร
Claude Code: /pasadu มาตรา 56 กล่าวถึงอะไร
```

Pasadu also treats `/pasadu` and `/passadu` as explicit textual aliases when the host sends those strings to the model. Codex users should prefer `$pasadu` when they want the standard skill selector.

## Update

Give the destination AI
[`newbie user guide/update-prompt.txt`](<./newbie user guide/update-prompt.txt>) when the user
wants the update performed automatically.

For a GitHub-sourced Skills CLI installation, try:

```powershell
npx.cmd --yes skills@latest update pasadu --global --yes
```

Do not trust the process exit code alone: some Skills CLI releases return exit code `0` together
with `No installed skills found matching`. Read the output and verify the installed files after
every update:

```powershell
npx.cmd --yes skills@latest list --global --json
```

`update` requires source metadata from the original GitHub installation. If `list --global --json`
shows `source: null`, `sourceUrl: null`, or a local source, remove and add the skill again from
`RobbyGrean/PassaduAIagent`, or use the AI-managed installer below. Local-path copies used by CI
are intentionally not updateable through Skills CLI.

Reliable fallback update:

```powershell
$workPath = Join-Path $env:TEMP ("pasadu-update-" + [guid]::NewGuid().ToString("N"))
$zipPath = Join-Path $workPath "pasadu.zip"
New-Item -ItemType Directory -Path $workPath | Out-Null
Invoke-WebRequest `
  -Uri "https://github.com/RobbyGrean/PassaduAIagent/archive/refs/heads/main.zip" `
  -OutFile $zipPath
Expand-Archive -LiteralPath $zipPath -DestinationPath $workPath
Set-Location (Join-Path $workPath "PassaduAIagent-main")
powershell -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\install-pasadu.ps1 -Agent codex
```

This installs the current `main` copy only after validation and retains the old installation beside
it as `pasadu.backup.<timestamp>`. Run the file checks and smoke test before deleting any backup.
The updater covers legal references, indexes, scripts, and skill instructions as one consistent
snapshot. It reports `PASADU_RELEASE` from `data/release.json`; update that release marker whenever
the bundled legal-reference snapshot changes.

Do not use `git pull` inside a Skills CLI installation. Skills CLI copies skill files without the repository's `.git` directory.

### Maintainer release procedure for legal updates

When a law, regulation, ministerial regulation, or circular changes:

1. Update the Markdown reference and its metadata.
2. Rebuild `skills/pasadu/data/index/`.
3. Update `package_release` and `reference_snapshot_date` in
   `skills/pasadu/data/release.json`.
4. Run the Python tests, retrieval smoke test, and installation contract.
5. Merge the consistent snapshot into `main`.
6. Let the post-release CI install from GitHub and verify the real global update channel.

Users then receive the complete snapshot through `skills update` or the AI-managed fallback. Do not
publish a reference change without its matching index and release marker.

## Remove

Remove from Codex:

```powershell
npx.cmd --yes skills@latest remove pasadu `
  --global --agent codex --yes
```

Remove from Claude Code:

```powershell
npx.cmd --yes skills@latest remove pasadu `
  --global --agent claude-code --yes
```

Remove from both:

```powershell
npx.cmd --yes skills@latest remove pasadu `
  --global --agent codex claude-code --yes
```

## Optional Git-managed installation

Use this advanced method only when you want to update Pasadu with `git pull`. Clone the source repository outside the host's skill directory, then link only `skills/pasadu`.

### Windows — Codex

```powershell
$sourcePath = "$env:USERPROFILE\.pasadu-source"
$skillsPath = "$env:USERPROFILE\.agents\skills"

git clone https://github.com/RobbyGrean/PassaduAIagent.git $sourcePath
New-Item -ItemType Directory -Force $skillsPath | Out-Null
New-Item -ItemType Junction `
  -Path "$skillsPath\pasadu" `
  -Target "$sourcePath\skills\pasadu"
```

### Windows — Claude Code

```powershell
$sourcePath = "$env:USERPROFILE\.pasadu-source"
$skillsPath = "$env:USERPROFILE\.claude\skills"

if (-not (Test-Path "$sourcePath\.git")) {
  git clone https://github.com/RobbyGrean/PassaduAIagent.git $sourcePath
}
New-Item -ItemType Directory -Force $skillsPath | Out-Null
New-Item -ItemType Junction `
  -Path "$skillsPath\pasadu" `
  -Target "$sourcePath\skills\pasadu"
```

### macOS and Linux

```bash
git clone https://github.com/RobbyGrean/PassaduAIagent.git ~/.pasadu-source
mkdir -p ~/.agents/skills
ln -s ~/.pasadu-source/skills/pasadu ~/.agents/skills/pasadu
```

For Claude Code, link the same source directory into `~/.claude/skills/pasadu`.

Update a Git-managed installation:

```powershell
git -C "$env:USERPROFILE\.pasadu-source" pull --ff-only
```

Never overwrite a non-Pasadu directory or delete local changes automatically. Inspect an existing destination before installing.

## Run retrieval scripts

Python 3.10 or newer is recommended when the host does not provide a Python runtime.

From an installed Codex skill on Windows:

```powershell
Set-Location "$env:USERPROFILE\.agents\skills\pasadu"
python scripts/pasadu/evidence_packet.py "มาตรา 56 กล่าวถึงอะไร" --limit 3
python scripts/pasadu/route_query.py "วิธีเฉพาะเจาะจงใช้ได้ในกรณีใด" --json
```

If Python is unavailable, the skill can search its Markdown references directly, but deterministic retrieval and citation checking will not run.

## Gemini CLI

Install globally with Skills CLI:

```powershell
npx.cmd --yes skills@latest add RobbyGrean/PassaduAIagent `
  --skill pasadu --agent gemini-cli --global --copy --yes
```

Then run:

```text
/skills list
/skills reload
```

Gemini CLI reads user skills from `~/.gemini/skills/`.

## ChatGPT desktop and Claude.ai

Standalone local skills are available only on host surfaces that can read the local skill directory. A web-only Claude.ai session cannot read files from `%USERPROFILE%`.

For Claude.ai on the web, use a Claude Project or a supported plugin workflow instead of claiming that a local installation is available.

## Troubleshooting

### PowerShell blocks `npx.ps1`

Use `npx.cmd`, as shown in this guide. Changing the machine-wide execution policy is not required.

### `node`, `npx.cmd`, or `git` is missing

Use the AI-assisted ZIP installation; ordinary users do not need these developer tools. Install
Node.js or Git only when deliberately choosing the Skills CLI or Git-managed option.

### A destination already exists

Do not rerun `add --yes` over an unknown directory. First check:

```powershell
Get-Content "$env:USERPROFILE\.agents\skills\pasadu\SKILL.md" -TotalCount 8
```

If it is a Skills CLI installation, use `skills update`. If it is a Git-managed installation, update `~/.pasadu-source` with `git pull --ff-only`.

### Skill is installed but not visible

1. Confirm `SKILL.md` at the exact global path.
2. Run `skills list --global --json`.
3. Restart the host if its top-level skill directory was created after startup.
4. In Codex, type `$` and select `pasadu`.
5. In Claude Code, try `/pasadu`.

### Python is missing

Install Python 3.10 or newer if deterministic retrieval is required. Otherwise ask the host to search the Markdown references directly and verify citations manually.

## Verified installation contract

The repository is ready for release only when CI and a clean local test confirm:

1. Skills CLI discovers exactly one skill named `pasadu`.
2. Only `skills/pasadu/` is copied.
3. Required runtime files exist.
4. Python unit tests pass.
5. A smoke query returns a verified evidence packet.
6. A clean copied installation appears in `list` and can be removed.
7. The released GitHub-sourced global installation can be updated when its source metadata is present.
8. The AI-managed installer can install, update, preserve a backup, and pass the same runtime verification without Skills CLI metadata.
