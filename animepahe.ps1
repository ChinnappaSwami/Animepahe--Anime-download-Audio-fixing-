# ====================================
# Activate VENV + Run animepahe-dl
# ====================================

$venvPath = "C:\Users\shrey\Desktop\My Overyy\mal_from_china"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (!(Test-Path $activateScript)) {
    Write-Host "❌ Virtual environment not found!"
    exit
}

# Go to environment folder
cd $venvPath

Write-Host ""
Write-Host "Activating environment..."
Write-Host ""

# Activate virtual environment
& $activateScript

Write-Host ""
Write-Host "Environment activated."
Write-Host "Running animepahe-dl..."
Write-Host ""

# Run animepahe-dl directly
animepahe-dl

Write-Host ""
Write-Host "Process finished."