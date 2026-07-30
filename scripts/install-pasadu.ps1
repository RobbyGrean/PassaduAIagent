[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet("codex", "claude-code", "gemini-cli")]
    [string[]] $Agent = @("codex"),

    [Parameter()]
    [string] $Destination
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repositoryRoot "skills\pasadu"
$requiredFiles = @(
    "SKILL.md",
    "pasadu.md",
    "reference\law\prb60.md",
    "reference\law\rbb60.md",
    "reference\law\rbb60-3.md",
    "scripts\pasadu\evidence_packet.py",
    "data\index\chunks.json"
)

function Assert-PasaduSkill {
    param(
        [Parameter(Mandatory)][string] $Path,
        [switch] $RequireRelease
    )

    foreach ($relativePath in $requiredFiles) {
        $requiredPath = Join-Path $Path $relativePath
        if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
            throw "Invalid Pasadu skill: missing $relativePath at $Path"
        }
    }

    $manifest = Get-Content -LiteralPath (Join-Path $Path "SKILL.md") -Raw -Encoding utf8
    if ($manifest -notmatch "(?m)^name:\s*pasadu\s*$") {
        throw "Refusing to install: SKILL.md does not declare name: pasadu"
    }

    if ($RequireRelease -and -not (Test-Path -LiteralPath (Join-Path $Path "data\release.json") -PathType Leaf)) {
        throw "Invalid Pasadu skill: missing data\release.json at $Path"
    }
}

function Get-AgentDestination {
    param([Parameter(Mandatory)][string] $AgentName)

    $userProfile = [Environment]::GetFolderPath("UserProfile")
    if ([string]::IsNullOrWhiteSpace($userProfile)) {
        throw "Cannot resolve the current user profile."
    }

    switch ($AgentName) {
        "codex" { return Join-Path $userProfile ".agents\skills\pasadu" }
        "claude-code" { return Join-Path $userProfile ".claude\skills\pasadu" }
        "gemini-cli" { return Join-Path $userProfile ".gemini\skills\pasadu" }
    }
}

function Install-PasaduCopy {
    param([Parameter(Mandatory)][string] $Target)

    $targetParent = Split-Path -Parent $Target
    $targetName = Split-Path -Leaf $Target
    if ($targetName -ne "pasadu") {
        throw "Refusing destination whose final directory name is not 'pasadu': $Target"
    }
    $stage = Join-Path $targetParent ".$targetName.stage.$([guid]::NewGuid().ToString('N'))"
    $backup = $null
    $hadExisting = Test-Path -LiteralPath $Target

    New-Item -ItemType Directory -Force -Path $targetParent | Out-Null

    if ($hadExisting) {
        Assert-PasaduSkill -Path $Target
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
        $backup = Join-Path $targetParent "$targetName.backup.$timestamp"
        if (Test-Path -LiteralPath $backup) {
            throw "Backup path already exists: $backup"
        }
    }

    try {
        New-Item -ItemType Directory -Path $stage | Out-Null
        Get-ChildItem -Force -LiteralPath $sourceSkill |
            Copy-Item -Destination $stage -Recurse -Force
        Assert-PasaduSkill -Path $stage -RequireRelease

        if ($hadExisting) {
            Move-Item -LiteralPath $Target -Destination $backup
        }
        Move-Item -LiteralPath $stage -Destination $Target
        Assert-PasaduSkill -Path $Target -RequireRelease
    }
    catch {
        if (-not (Test-Path -LiteralPath $Target) -and $backup -and (Test-Path -LiteralPath $backup)) {
            Move-Item -LiteralPath $backup -Destination $Target
        }
        if (Test-Path -LiteralPath $stage) {
            Remove-Item -LiteralPath $stage -Recurse -Force
        }
        throw
    }

    if ($hadExisting) {
        Write-Output "PASADU_UPDATED: $Target"
        Write-Output "PASADU_BACKUP: $backup"
    }
    else {
        Write-Output "PASADU_INSTALLED: $Target"
    }
    $release = Get-Content -LiteralPath (Join-Path $Target "data\release.json") -Raw -Encoding utf8 |
        ConvertFrom-Json
    Write-Output "PASADU_RELEASE: $($release.package_release)"
}

Assert-PasaduSkill -Path $sourceSkill -RequireRelease

if ($Destination) {
    if ($Agent.Count -ne 1) {
        throw "-Destination can be used with exactly one -Agent value."
    }
    Install-PasaduCopy -Target $Destination
}
else {
    foreach ($agentName in $Agent) {
        Install-PasaduCopy -Target (Get-AgentDestination -AgentName $agentName)
    }
}
