# Batch detect fake PNG files script
# Detect real format of all PNG files in the project

$projectRoot = "i:\Github\Ultimate-_tarter_Kit_for_Pico_W_PDF\Ultimate-Starter-Kit-for-Pico-W"
$outputDir = "i:\Github\Ultimate-_tarter_Kit_for_Pico_W_PDF\Ultimate-Starter-Kit-for-Pico-W\伪png"
$csvFile = "i:\Github\Ultimate-_tarter_Kit_for_Pico_W_PDF\Ultimate-Starter-Kit-for-Pico-W\fake_png_report.csv"

# Create output directory
if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force
}

# Initialize result arrays
$results = @()
$fakePngFiles = @()

# Get all PNG files
$pngFiles = Get-ChildItem -Path $projectRoot -Recurse -Filter "*.png" | Where-Object { !$_.PSIsContainer }

Write-Host "Found $($pngFiles.Count) PNG files, starting detection..."

foreach ($file in $pngFiles) {
    try {
        # Read first 16 bytes of file header
        $bytes = Get-Content -Path $file.FullName -Encoding Byte -TotalCount 16
        
        if ($bytes.Length -ge 8) {
            # Check PNG file header (89 50 4E 47 0D 0A 1A 0A)
            $isPng = ($bytes[0] -eq 0x89) -and ($bytes[1] -eq 0x50) -and ($bytes[2] -eq 0x4E) -and ($bytes[3] -eq 0x47)
            
            # Check other formats
            $actualFormat = "Unknown"
            if ($isPng) {
                $actualFormat = "PNG"
            } elseif (($bytes[0] -eq 0x52) -and ($bytes[1] -eq 0x49) -and ($bytes[2] -eq 0x46) -and ($bytes[3] -eq 0x46)) {
                # RIFF format, might be WebP
                if (($bytes[8] -eq 0x57) -and ($bytes[9] -eq 0x45) -and ($bytes[10] -eq 0x42) -and ($bytes[11] -eq 0x50)) {
                    $actualFormat = "WebP"
                } else {
                    $actualFormat = "RIFF"
                }
            } elseif (($bytes[0] -eq 0xFF) -and ($bytes[1] -eq 0xD8) -and ($bytes[2] -eq 0xFF)) {
                $actualFormat = "JPEG"
            } elseif (($bytes[0] -eq 0x47) -and ($bytes[1] -eq 0x49) -and ($bytes[2] -eq 0x46)) {
                $actualFormat = "GIF"
            } elseif (($bytes[0] -eq 0x42) -and ($bytes[1] -eq 0x4D)) {
                $actualFormat = "BMP"
            }
            
            # Create result object
            $result = [PSCustomObject]@{
                FileName = $file.Name
                FilePath = $file.FullName
                RelativePath = $file.FullName.Replace($projectRoot, "").TrimStart('\\')
                FileSize = $file.Length
                ActualFormat = $actualFormat
                IsFakePng = ($actualFormat -ne "PNG")
                HexHeader = ($bytes[0..15] | ForEach-Object { $_.ToString("X2") }) -join " "
            }
            
            $results += $result
            
            # If it's a fake PNG file, add to copy list
            if ($result.IsFakePng) {
                $fakePngFiles += $file
                Write-Host "Found fake PNG file: $($file.Name) (actual format: $actualFormat)" -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "Error processing file: $($file.FullName) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Generate CSV report
$results | Export-Csv -Path $csvFile -NoTypeInformation -Encoding UTF8
Write-Host "`nDetection completed!" -ForegroundColor Green
Write-Host "Total files: $($results.Count)"
Write-Host "Real PNG files: $(($results | Where-Object { !$_.IsFakePng }).Count)"
Write-Host "Fake PNG files: $(($results | Where-Object { $_.IsFakePng }).Count)"
Write-Host "CSV report saved to: $csvFile"

# Copy fake PNG files to specified directory
if ($fakePngFiles.Count -gt 0) {
    Write-Host "`nStarting to copy fake PNG files to directory: $outputDir" -ForegroundColor Cyan
    
    foreach ($file in $fakePngFiles) {
        try {
            $destPath = Join-Path $outputDir $file.Name
            
            # If target file already exists, add sequence number
            $counter = 1
            $originalDestPath = $destPath
            while (Test-Path $destPath) {
                $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
                $ext = [System.IO.Path]::GetExtension($file.Name)
                $destPath = Join-Path $outputDir "$nameWithoutExt`_$counter$ext"
                $counter++
            }
            
            Copy-Item -Path $file.FullName -Destination $destPath -Force
            Write-Host "Copied: $($file.Name) -> $(Split-Path $destPath -Leaf)"
        } catch {
            Write-Host "Failed to copy file: $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host "`nFake PNG files copy completed!" -ForegroundColor Green
} else {
    Write-Host "`nNo fake PNG files found." -ForegroundColor Green
}

Write-Host "`nScript execution completed!"