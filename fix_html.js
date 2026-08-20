const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// The original lines were either corrupted with `?  ` or `  `
// Let's replace anything between data-lang=".*"> and the author name.
// Basically, we look for data-lang="pt"> (or en), followed by any non-word characters, up to the first alphanumeric character,
// and replace those non-word characters with "— ".
html = html.replace(/(<footer class="inline-review-author[^>]*>)[^A-Za-z0-9]*(.*?)(<\/footer>)/g, '$1— $2$3');

fs.writeFileSync('index.html', html);
console.log('Fixed em-dashes in index.html');
