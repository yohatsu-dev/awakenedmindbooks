const fs = require('fs');
let script = fs.readFileSync('script.js', 'utf8');

// 1. Remove the Substack logic from the end of the file
const substackBlockStart = script.indexOf('/* -------------------------------------------------- *\n   *  10  Substack Feed');
if (substackBlockStart === -1) {
    console.log("Could not find substack block start");
    process.exit(1);
}

// Keep everything before the Substack block
let beforeSubstack = script.substring(0, substackBlockStart);

// Now we need to insert the Substack function inside the IIFE, before DOMContentLoaded
const domContentLoadedStart = beforeSubstack.lastIndexOf('/* -------------------------------------------------- *\n   * 13 · Bootstrap');

const substackCode = `  /* -------------------------------------------------- *
   * 13 · Substack Feed (RSS to JSON)
   * -------------------------------------------------- */
  const initSubstackFeed = () => {
    const feedContainer = document.getElementById("substack-feed");
    if (!feedContainer) return;

    const rssUrl = encodeURIComponent("https://mentedespertabooks.substack.com/feed");
    const apiUrl = \`https://api.rss2json.com/v1/api.json?rss_url=\${rssUrl}\`;

    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        if (data.status === "ok") {
          const items = data.items.slice(0, 3);
          feedContainer.innerHTML = "";
          const enTranslations = {
            "E se você não fosse você por uma hora?": "What if you weren't you for an hour?",
            "A jornada de escritor e o tribunal de uma pessoa só.": "The writer's journey and the one-person tribunal.",
            "A Segunda Flecha": "The Second Arrow"
          };
          items.forEach(item => {
            const pubDate = new Date(item.pubDate).toLocaleDateString(navigator.language, { month: "short", day: "numeric", year: "numeric" });
            const title = item.title;
            const enTitle = enTranslations[title] || title;
            const link = item.link;

            const card = document.createElement("a");
            card.className = "article-card";
            card.href = link;
            card.target = "_blank";
            card.rel = "noopener noreferrer";

            card.innerHTML = \`
              <div class="article-date"></div>
              <h3 class="article-title" data-lang="pt"></h3>
              <h3 class="article-title hidden" data-lang="en"></h3>
              <span class="article-link"><span data-lang="pt">Ler no Substack &rarr;</span><span data-lang="en">Read on Substack &rarr;</span></span>
            \`;
            
            card.querySelector('.article-date').textContent = pubDate;
            card.querySelector('h3[data-lang="pt"]').textContent = title;
            card.querySelector('h3[data-lang="en"]').textContent = enTitle;

            feedContainer.appendChild(card);
          });
          // Update language visibility if the global setting dictates it
          const currentLang = localStorage.getItem('site_lang') || (navigator.language.startsWith('pt') ? 'pt' : 'en');
          feedContainer.querySelectorAll('[data-lang]').forEach(el => {
              if(el.getAttribute('data-lang') === currentLang) {
                  el.classList.remove('hidden');
              } else {
                  el.classList.add('hidden');
              }
          });
        } else {
          feedContainer.textContent = "Nenhum artigo encontrado no momento.";
        }
      })
      .catch(error => {
        console.error("Error fetching Substack feed:", error);
        feedContainer.textContent = "Não foi possível carregar os artigos.";
      });
  };

`;

let part1 = beforeSubstack.substring(0, domContentLoadedStart);
let part2 = beforeSubstack.substring(domContentLoadedStart);

// Inject the substack initialization inside the Bootstrap block
part2 = part2.replace('initCarousel();', 'initCarousel();\n    initSubstackFeed();');

const finalScript = part1 + substackCode + part2;

fs.writeFileSync('script.js', finalScript);
console.log('Script updated successfully!');
