const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const dir = 'assets/covers';

// Resize to 600px width (plenty for high-DPI cards) and convert to WebP
fs.readdirSync(dir)
  .filter(f => f.endsWith('.jpg'))
  .forEach(f => {
    const inputPath = path.join(dir, f);
    const outputPath = path.join(dir, f.replace('.jpg', '.webp'));
    
    // Convert to webp
    sharp(inputPath)
      .resize({ width: 600, withoutEnlargement: true })
      .webp({ quality: 80, effort: 6 })
      .toFile(outputPath)
      .then(() => console.log('Optimized to WebP:', f))
      .catch(console.error);
      
    // Overwrite the original JPG with a smaller version for the fallback
    sharp(inputPath)
      .resize({ width: 600, withoutEnlargement: true })
      .jpeg({ quality: 80, progressive: true })
      .toBuffer()
      .then(data => {
         fs.writeFileSync(inputPath, data);
         console.log('Optimized JPG Fallback:', f);
      })
      .catch(console.error);
  });
