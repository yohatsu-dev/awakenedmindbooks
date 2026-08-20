const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

let lines = html.split('\n');
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('<!--') && lines[i].includes('-->') && (lines[i].includes('\uFFFD') || lines[i].includes(''))) {
     if (lines[i].includes('TARA')) lines[i] = '<!-- ✦ ✦ ✦ TARA ✦ ✦ ✦ -->';
     else if (lines[i].includes('AVALOKITESHVARA')) lines[i] = '<!-- ✦ ✦ ✦ AVALOKITESHVARA ✦ ✦ ✦ -->';
     else if (lines[i].includes('MANJUSHRI')) lines[i] = '<!-- ✦ ✦ ✦ MANJUSHRI ✦ ✦ ✦ -->';
     else if (lines[i].includes('VAJRASATTVA')) lines[i] = '<!-- ✦ ✦ ✦ VAJRASATTVA ✦ ✦ ✦ -->';
     else if (lines[i].includes('VAJRAPANI')) lines[i] = '<!-- ✦ ✦ ✦ VAJRAPANI ✦ ✦ ✦ -->';
  }
  // For multi-line comments that are separators:
  if (lines[i].includes('<!--') && !lines[i].includes('-->') && (lines[i].includes('\uFFFD') || lines[i].includes(''))) {
     lines[i] = '<!-- -----------------------------------------------------------------------------------------------------';
  }
  if (!lines[i].includes('<!--') && lines[i].includes('-->') && (lines[i].includes('\uFFFD') || lines[i].includes(''))) {
     lines[i] = '----------------------------------------------------------------------------------------------------- -->';
  }
}

fs.writeFileSync('index.html', lines.join('\n'));
console.log('Fixed comment separators!');
