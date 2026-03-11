param(
    [switch]$SkipWebSync,
    [switch]$SkipGradle,
    [switch]$ForceNpmInstall,
    [switch]$OpenAndroidStudio
)

$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

Write-Host '== Android Direct Build ==' -ForegroundColor Cyan
Write-Host "Repo: $repoRoot"

if (-not $SkipWebSync) {
    Write-Host '1/5 Syncing web assets into apps/mobile/www...' -ForegroundColor Yellow
    & powershell.exe -ExecutionPolicy Bypass -File (Join-Path $repoRoot 'scripts\sync-web.ps1')
}

Set-Location (Join-Path $repoRoot 'apps\mobile')

if ($ForceNpmInstall -or -not (Test-Path 'node_modules')) {
    Write-Host '2/5 Installing Capacitor dependencies...' -ForegroundColor Yellow
    & npm.cmd install
    if ($LASTEXITCODE -ne 0) { throw 'npm install failed in apps/mobile' }
} else {
    Write-Host '2/5 Reusing existing Capacitor dependencies.' -ForegroundColor DarkGray
}

if (-not (Test-Path 'android')) {
    Write-Host '3/5 Android platform missing; adding it now...' -ForegroundColor Yellow
    & npx.cmd cap add android
    if ($LASTEXITCODE -ne 0) { throw 'npx cap add android failed' }
} else {
    Write-Host '3/5 Android platform already present.' -ForegroundColor DarkGray
}

Write-Host '4/5 Syncing Capacitor Android project...' -ForegroundColor Yellow
& npx.cmd cap sync android
if ($LASTEXITCODE -ne 0) { throw 'npx cap sync android failed' }

$gradleUserHome = Join-Path $repoRoot '.gradle-user-home'
if (-not (Test-Path $gradleUserHome)) {
    New-Item -ItemType Directory -Path $gradleUserHome -Force | Out-Null
}
$env:GRADLE_USER_HOME = $gradleUserHome
Write-Host "Gradle user home: $env:GRADLE_USER_HOME" -ForegroundColor DarkGray

if (-not $SkipGradle) {
    Write-Host '5/5 Building debug APK with Gradle...' -ForegroundColor Yellow
    Set-Location (Join-Path $repoRoot 'apps\mobile\android')
    & .\gradlew.bat assembleDebug
    if ($LASTEXITCODE -ne 0) { throw 'Gradle assembleDebug failed' }

    $apkPath = Join-Path $repoRoot 'apps\mobile\android\app\build\outputs\apk\debug\app-debug.apk'
    if (-not (Test-Path $apkPath)) {
        throw "Build finished but APK not found at $apkPath"
    }

    $apk = Get-Item $apkPath
    Write-Host 'APK generated successfully.' -ForegroundColor Green
    Write-Host "APK: $($apk.FullName)"
    Write-Host "Size: $([Math]::Round($apk.Length / 1MB, 2)) MB"
}

if ($OpenAndroidStudio) {
    Set-Location (Join-Path $repoRoot 'apps\mobile')
    Write-Host 'Opening Android Studio via Capacitor...' -ForegroundColor Yellow
    & npx.cmd cap open android
}
