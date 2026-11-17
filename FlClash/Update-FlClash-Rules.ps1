param(
    [string]$ScriptId = '202611170001'
)
$ErrorActionPreference = 'Stop'
try {
    if ($ScriptId -notmatch '^\d+$') { throw 'Invalid script ID.' }
    $scriptDir = Join-Path $env:APPDATA 'com.follow\clash\scripts'
    $target = Join-Path $scriptDir ($ScriptId + '.js')
    if (-not (Test-Path -LiteralPath $target)) {
        throw 'Bound FlClash script not found. Import and bind the JS script in FlClash first.'
    }
    $uri = 'https://raw.githubusercontent.com/oyyj11/shadowrocket-daily-route/main/FlClash/OpenAI-Google-US.js'
    $temp = Join-Path $scriptDir ($ScriptId + '.' + [guid]::NewGuid().ToString('N') + '.tmp')
    Invoke-WebRequest -Uri $uri -OutFile $temp -TimeoutSec 45 -UseBasicParsing
    $content = [IO.File]::ReadAllText($temp)
    if ($content.Length -lt 500 -or $content.Length -gt 200000 -or -not $content.StartsWith('// DailyRoute-FlClash ') -or -not $content.Contains('const main =')) {
        Remove-Item -LiteralPath $temp
        throw 'Unexpected response. Existing script was not replaced.'
    }
    $backupDir = Join-Path $scriptDir 'dailyroute-backups'
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    $backup = Join-Path $backupDir ($ScriptId + '-' + [DateTime]::Now.ToString('yyyyMMdd-HHmmssfff') + '.js')
    [IO.File]::Replace($temp, $target, $backup)
    Write-Host 'Updated OpenAI / Google US routing script.' -ForegroundColor Green
    Write-Host 'Exit FlClash from its tray menu, then open it again to load the update.'
    Write-Host 'Keep routing mode set to Rule. Subscription Sync only updates nodes.'
    Write-Host "Backup: $backup"
} catch {
    Write-Host ('Update failed: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
