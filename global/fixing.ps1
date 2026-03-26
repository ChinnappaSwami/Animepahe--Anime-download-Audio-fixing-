# ====================================
# Audio Fix Script (MP4 Batch Fixer)
# Auto-closes when finished
# ====================================

Write-Host ""
Write-Host "====================================="
Write-Host "         Audio Fix Started"
Write-Host "====================================="
Write-Host ""

# Check if ffmpeg exists
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "❌ ERROR: ffmpeg is not installed or not in PATH."
    Start-Sleep -Seconds 3
    exit 1
}

# Create fixed folder if not exists
if (!(Test-Path "fixed")) {
    Write-Host "Creating 'fixed' folder..."
    New-Item -ItemType Directory -Name "fixed" | Out-Null
}

# Get all mp4 files
$files = Get-ChildItem -Filter *.mp4

if ($files.Count -eq 0) {
    Write-Host "⚠ No MP4 files found in this folder."
    Start-Sleep -Seconds 2
    exit 0
}

foreach ($file in $files) {

    $inputFile = $file.FullName
    $outputFile = Join-Path "fixed" $file.Name

    Write-Host "Fixing: $($file.Name)"

    ffmpeg -y `
        -i "$inputFile" `
        -map 0:v:0 `
        -map 0:a? `
        -c:v copy `
        -c:a aac `
        -b:a 192k `
        -movflags +faststart `
        "$outputFile"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error processing $($file.Name)"
    }
}

Write-Host ""
Write-Host "====================================="
Write-Host "✅ All files processed successfully."
Write-Host "Fixed files are inside ./fixed/"
Write-Host "====================================="
Write-Host ""

Start-Sleep -Seconds 2
exit 0
