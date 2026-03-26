# ====================================
# Run animepahe-dl (Global Install)
# ====================================

Write-Host ""
Write-Host "====================================="
Write-Host "       Anime Downloader"
Write-Host "====================================="
Write-Host ""

# Check if animepahe-dl is available globally
if (-not (Get-Command animepahe-dl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ animepahe-dl not found! Installing globally..."
    Write-Host ""
    pip install animepahe-dl
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install animepahe-dl. Make sure pip is in PATH."
        Start-Sleep -Seconds 5
        exit 1
    }
    Write-Host ""
    Write-Host "✅ animepahe-dl installed successfully."
    Write-Host ""
}

Write-Host "Running animepahe-dl..."
Write-Host ""

# Run animepahe-dl globally
animepahe-dl

Write-Host ""
Write-Host "====================================="
Write-Host "        Process finished."
Write-Host "====================================="
Write-Host ""
