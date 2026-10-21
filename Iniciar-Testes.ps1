param([switch]$Supabase)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force '.tmp' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot '.tmp'
$env:TMP = $env:TEMP
if (!(Test-Path '.venv/Scripts/python.exe')) { python -m venv .venv }
if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python' }
if ($Supabase) {
    $env:SOS_MODO = 'supabase'
} else {
    $env:SOS_MODO = 'local'
    if (!$env:SOS_SENHA_INICIAL) { $env:SOS_SENHA_INICIAL = 'TesteLocal2026!' }
    $env:SOS_DATA_DIR = Join-Path $PSScriptRoot 'dados_teste'
}
& .venv/Scripts/python.exe -m streamlit run SOS_PAE/app.py --server.address=127.0.0.1 --server.port=8501
