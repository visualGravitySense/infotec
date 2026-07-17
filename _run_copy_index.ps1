Copy-Item -Path "$PSScriptRoot\inner-page-1.html" -Destination "$PSScriptRoot\index.html" -Force
$src = (Get-Content "$PSScriptRoot\inner-page-1.html").Count
$dst = (Get-Content "$PSScriptRoot\index.html").Count
Write-Output "index.html exists: $(Test-Path '$PSScriptRoot\index.html')"
Write-Output "inner-page-1.html lines: $src"
Write-Output "index.html lines: $dst"