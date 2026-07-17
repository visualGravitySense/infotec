Copy-Item -Path "$PSScriptRoot\inner-page-3.html" -Destination "$PSScriptRoot\inner-page-metalworking.html" -Force
$lines = (Get-Content "$PSScriptRoot\inner-page-metalworking.html").Count
Write-Output "Copied. Line count: $lines"