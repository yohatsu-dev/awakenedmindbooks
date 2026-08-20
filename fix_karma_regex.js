const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const regex = /(<div class=\"book-info\">\s*)(<div class=\"book-badges\">)/;
const injection = `            <h2 class="book-title" data-lang="pt">Karma aí, pessoal!</h2>
            <h2 class="book-title hidden" data-lang="en">That's Karma, Man!</h2>
            <p class="book-tagline" data-lang="pt">Pare de surtar, aceite o óbvio e aprenda a plantar melhor o que você quer colher.</p>
            <p class="book-tagline hidden" data-lang="en">Stop freaking out, accept the obvious, and learn to better plant what you want to harvest.</p>
            <p class="book-blurb" data-lang="pt">O volume mais direto e sem cerimônia da série. Karma aqui não é destino nem punição cósmica — é consequência, e consequência se maneja. Um livro mais curto, tom mais ácido e mais pop, para quem já testou os outros métodos da série e quer aplicar a mesma lógica de causa e efeito de forma mais rápida e menos solene, sem perder a substância.</p>
            <p class="book-blurb hidden" data-lang="en">The most direct and unceremonious volume of the series. Karma here is not destiny or cosmic punishment — it is consequence, and consequence can be managed. A shorter book, with a more acid and pop tone, for those who have already tested the other methods of the series and want to apply the same logic of cause and effect in a faster and less solemn way, without losing substance.</p>
            <blockquote class="book-excerpt active" data-lang="pt">
              <p>“Karma não é uma entidade com um caderninho anotando os seus pecados. Karma não é o universo querendo te dar uma lição. Karma é física básica, só que aplicada à mente. É causa e efeito.⬝</p>
            </blockquote>
            <blockquote class="book-excerpt hidden" data-lang="en">
              <p>“Karma is not an entity with a little notebook recording your sins. Karma is not the universe trying to teach you a lesson. Karma is basic physics, just applied to the mind. It is cause and effect.⬝</p>
            </blockquote>
            <blockquote class="book-inline-review">
              <p class="inline-review-text" data-lang="pt">"Linguagem leve, descontraída e fácil de ler. Traz reflexões práticas sobre responsabilidade pessoal."</p>
              <p class="inline-review-text hidden" data-lang="en">"Light, relaxed language and easy to read. Brings practical reflections on personal responsibility."</p>
              <footer class="inline-review-author" data-lang="pt">- Gabriela (via Amazon)</footer>
              <footer class="inline-review-author hidden" data-lang="en">- Gabriela (via Amazon)</footer>
            </blockquote>
`;

if (regex.test(html)) {
    html = html.replace(regex, `$1` + injection + `$2`);
    fs.writeFileSync('index.html', html);
    console.log('Fixed Karma section!');
} else {
    console.log('Regex did not match!');
}
