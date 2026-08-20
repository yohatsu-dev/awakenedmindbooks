const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replace all apostrophes
html = html.replace(/\uFFFD"t/g, "'t");
html = html.replace(/\uFFFD"s/g, "'s");

// Replace Avalokiteśvara
html = html.replace(/Avalokite\uFFFD:vara/g, 'Avalokiteshvara');

// Replace the weird comments
html = html.replace(/<!-- \uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"/g, '<!-- -----------------------------------------------------------------------------------------------------');
html = html.replace(/<!-- —"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"/g, '<!-- -----------------------------------------------------------------------------------------------------');

html = html.replace(/—"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"— -->/g, '----------------------------------------------------------------------------------------------------- -->');
html = html.replace(/\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD"\uFFFD" -->/g, '----------------------------------------------------------------------------------------------------- -->');

// Headers
html = html.replace(/<!-- — \uFFFD \uFFFD — TARA — \uFFFD \uFFFD — -->/g, '<!-- ✦ ✦ ✦ TARA ✦ ✦ ✦ -->');
html = html.replace(/<!-- — \uFFFD \uFFFD — AVALOKITESHVARA — \uFFFD \uFFFD — -->/g, '<!-- ✦ ✦ ✦ AVALOKITESHVARA ✦ ✦ ✦ -->');
html = html.replace(/<!-- — \uFFFD \uFFFD — MANJUSHRI — \uFFFD \uFFFD — -->/g, '<!-- ✦ ✦ ✦ MANJUSHRI ✦ ✦ ✦ -->');
html = html.replace(/<!-- — \uFFFD \uFFFD — VAJRASATTVA — \uFFFD \uFFFD — -->/g, '<!-- ✦ ✦ ✦ VAJRASATTVA ✦ ✦ ✦ -->');
html = html.replace(/<!-- — \uFFFD \uFFFD — VAJRAPANI — \uFFFD \uFFFD — -->/g, '<!-- ✦ ✦ ✦ VAJRAPANI ✦ ✦ ✦ -->');

html = html.replace(/\uFFFD<!DOCTYPE html>/g, '<!DOCTYPE html>');

fs.writeFileSync('index.html', html);
console.log('Fixed everything!');
