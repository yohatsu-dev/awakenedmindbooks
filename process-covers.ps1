Add-Type -AssemblyName System.Drawing

function Save-Image {
    param ($src, $dest)
    try {
        $img = [System.Drawing.Image]::FromFile($src)
        # Create a new bitmap to strip any weird alpha channels and force RGB
        $bmp = New-Object System.Drawing.Bitmap($img.Width, $img.Height)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.Clear([System.Drawing.Color]::White)
        $g.DrawImage($img, 0, 0, $img.Width, $img.Height)
        
        # Save as high-quality JPG
        $codecs = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()
        $jpegCodec = $codecs | Where-Object { $_.MimeType -eq 'image/jpeg' }
        $encoderParams = New-Object System.Drawing.Imaging.EncoderParameters(1)
        $encoderParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 90L)
        
        $bmp.Save($dest, $jpegCodec, $encoderParams)
        
        $g.Dispose()
        $bmp.Dispose()
        $img.Dispose()
        Write-Host "Processed $dest"
    } catch {
        Write-Host "Error processing $src : $($_.Exception.Message)"
    }
}

$desktopDir = "C:\Users\hugos\OneDrive\Desktop\site"
$targetDir = "C:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers"

$map = @{
    "AVALOFINAL EN.png" = "avalo-en.jpg"
    "AVALOFINAL PT.png" = "avalo-pt.jpg"
    "MANJUFINAL EN.png" = "manjushri-en.jpg"
    "MANJUFINAL PT.png" = "manjushri-pt.jpg"
    "TARAFINAL EN.png"  = "tara-en.jpg"
    "TARAFINAL PT.png"  = "tara-pt.jpg"
    "VAJRAFINAL EN.png" = "vajra-en.jpg"
    "VAJRAFINAL PT.png" = "vajra-pt.jpg"
}

foreach ($key in $map.Keys) {
    $srcFile = Join-Path $desktopDir $key
    $destFile = Join-Path $targetDir $map[$key]
    if (Test-Path $srcFile) {
        Save-Image -src $srcFile -dest $destFile
    } else {
        Write-Host "Missing $srcFile"
    }
}

