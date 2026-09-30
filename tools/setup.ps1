param([switch]$InstallOnly)
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Runtime = Join-Path $ProjectRoot 'runtime'
$EngineExe = Join-Path $Runtime 'Ikemen_GO.exe'
$Expected = '9338eaeb68599ceb13b0867819a091ea3f92eba58077e800b4540b7a1f9c3731'
$Url = 'https://github.com/ikemen-engine/Ikemen-GO/releases/download/v1.0.0/Ikemen_GO-v1.0.0-windows.zip'
try {
    if (-not (Test-Path $EngineExe)) {
        Write-Host 'Baixando Ikemen GO 1.0.0. Esta etapa so acontece na primeira execucao.'
        $Archive = Join-Path $ProjectRoot 'ikemen-download.zip'
        $Staging = Join-Path $ProjectRoot 'runtime-install'
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $Url -OutFile $Archive -UseBasicParsing
        if ((Get-FileHash $Archive -Algorithm SHA256).Hash.ToLower() -ne $Expected) {
            throw 'O arquivo do motor nao passou na verificacao SHA256.'
        }
        if (Test-Path $Staging) { throw 'A pasta runtime-install ja existe. Renomeie-a para preservar seu conteudo e tente novamente.' }
        Expand-Archive -Path $Archive -DestinationPath $Staging
        if (-not (Test-Path (Join-Path $Staging 'Ikemen_GO.exe'))) { throw 'Executavel do motor ausente no arquivo baixado.' }
        if (Test-Path $Runtime) { throw 'runtime existe sem o executavel. Renomeie a pasta e tente novamente.' }
        Move-Item $Staging $Runtime
        Remove-Item $Archive
    }
    # Apply only this project's content; player settings in save/ are preserved.
    Copy-Item -Path (Join-Path $ProjectRoot 'game\*') -Destination $Runtime -Recurse -Force
    $Save = Join-Path $Runtime 'save'
    New-Item -ItemType Directory -Path $Save -Force | Out-Null
    $Config = Join-Path $Save 'eter.ini'
    if (-not (Test-Path $Config)) {
        Copy-Item (Join-Path $ProjectRoot 'game\data\eter\config.ini') $Config
    }
    Write-Host 'CODE-ETER-COF pronto.'
    if (-not $InstallOnly) {
        Push-Location $Runtime
        try { & $EngineExe -config save/eter.ini } finally { Pop-Location }
        if ($LASTEXITCODE -ne 0) { throw "O jogo terminou com codigo $LASTEXITCODE. Consulte runtime/Ikemen.log." }
    }
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

