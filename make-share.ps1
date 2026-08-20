Add-Type -AssemblyName System.Drawing
$width = 1200
$height = 630
$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

# Fill background with dark navy (from CSS var --bg-deep: #0c0e1a)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 12, 14, 26))
$graphics.FillRectangle($brush, 0, 0, $width, $height)
$brush.Dispose()

# Draw a subtle gold line across the middle
$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 212, 168, 83), 2)
$graphics.DrawLine($pen, 100, 315, 1100, 315)
$pen.Dispose()

# Load covers
$covers = @(
  "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers\tara-pt.jpg",
  "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers\avalo-pt.jpg",
  "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers\manjushri-pt.jpg",
  "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers\vajra-pt.jpg",
  "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\covers\karma-pt.jpg"
)

# Calculate sizing
# Target cover height: 400px
$targetHeight = 400
$targetWidth = [int]($targetHeight * (1500/2250)) # aspect ratio of standard kindle cover 2:3

# 5 covers + 4 gaps = 1200px width.
# Total width needed for covers = 5 * targetWidth
$gap = 40
$totalWidth = (5 * $targetWidth) + (4 * $gap)
$startX = ($width - $totalWidth) / 2
$startY = ($height - $targetHeight) / 2

for ($i = 0; $i -lt 5; $i++) {
    $img = [System.Drawing.Image]::FromFile($covers[$i])
    $x = $startX + ($i * ($targetWidth + $gap))
    
    # Draw shadow first (simple offset)
    $shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(100, 0, 0, 0))
    $graphics.FillRectangle($shadowBrush, $x + 10, $startY + 15, $targetWidth, $targetHeight)
    $shadowBrush.Dispose()
    
    # Draw image
    $graphics.DrawImage($img, $x, $startY, $targetWidth, $targetHeight)
    $img.Dispose()
}

$graphics.Dispose()
$savePath = "c:\Users\hugos\OneDrive\Documentos\GitHub\awakened\assets\social-share.jpg"
$bitmap.Save($savePath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
$bitmap.Dispose()
Write-Host "Created social-share.jpg"
