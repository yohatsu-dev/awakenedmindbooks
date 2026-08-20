# Mente Desperta — estrutura de SEO

Este arquivo documenta o que foi acrescentado ao site e como manter tudo funcionando
quando um livro novo entrar no catálogo. O visual, o CSS existente e a lógica da home
não foram alterados.

## Arquitetura de URLs

| URL | Arquivo | Idioma |
|---|---|---|
| `/` | `index.html` | PT (com toggle EN) |
| `/livros/` | `livros/index.html` | PT — hub de todos os livros |
| `/livros/<slug>/` | `livros/<slug>/index.html` | PT — 7 páginas de livro |
| `/en/books/` | `en/books/index.html` | EN — hub |
| `/en/books/<slug>/` | `en/books/<slug>/index.html` | EN — 7 páginas de livro |
| `/autor` | `autor.html` | PT |
| `/en/author/` | `en/author/index.html` | EN |
| `/404.html` | `404.html` | página de erro (noindex) |

Cada página de livro em PT aponta para a equivalente em EN via `hreflang`, e vice-versa.
O `x-default` aponta sempre para a versão em português.

## Como adicionar um livro novo

1. Coloque as capas em `assets/covers/` como `<nome>-pt.jpg` e `<nome>-en.jpg`.
2. Rode `python optimize-covers.py` — ele reduz as capas para 640px de largura,
   gera `.webp` e cria as miniaturas em `assets/covers/thumbs/` usadas no hero.
3. Acrescente o livro em `books.json` (copie o bloco de outro livro e troque os campos:
   `key`, `accent`, `cover`, `order`, ASINs, `status_br`/`status_us`, e os textos `pt` e `en`).
4. Rode `python build.py`. Ele regenera as 14 páginas de livro, os dois hubs,
   a página do autor em inglês e o `sitemap.xml`.
5. Acrescente o card do livro na home manualmente (a home continua sendo escrita à mão),
   incluindo o link `<p class="book-more">` para a página nova.

## Arquivos do gerador

- `books.json` — todo o conteúdo editorial das páginas (PT e EN).
- `build.py` — gerador estático. Não toca em `index.html` nem em `autor.html`.
- `optimize-covers.py` — compressão de capas e geração de miniaturas.
- `dims.json` — dimensões das capas (gerado por `optimize-covers.py`), usado para
  preencher `width`/`height` nas imagens e evitar layout shift.

Os trechos de livro (`.book-excerpt`) exibidos nas páginas são lidos direto do
`index.html` pelo `build.py` — não precisam ser duplicados em `books.json`.

## O que foi feito de SEO técnico

- Página própria para cada livro, em dois idiomas (14 páginas indexáveis onde antes
  havia âncoras `#livro-x` que o Google não indexa separadamente).
- `hreflang` recíproco pt-BR / en / x-default em todas as páginas com par.
- Canonical em todas as páginas; `/autor.html` passou a canonizar para `/autor`.
- Dados estruturados (JSON-LD) com `Book`, `BookSeries`, `Person`, `FAQPage`,
  `BreadcrumbList`, `ItemList`, `WebSite` e `CollectionPage`.
- Breadcrumbs visíveis e marcados.
- FAQ por livro — elegível para resultado enriquecido no Google.
- `sitemap.xml` com as 19 URLs reais e alternates de idioma (sem âncoras `#`).
- `robots.txt` liberando explicitamente os bots de busca generativa.
- Capas reduzidas de ~52 MB para ~2,9 MB no total; miniaturas de 320px no hero,
  `width`/`height` em todas as imagens e `preload` da capa principal de cada página.
- `netlify.toml` com cabeçalhos de cache e de segurança.


## Cache das capas — por que não é `immutable`

As capas têm nome fixo: `buddha-pt.jpg` continua `buddha-pt.jpg` quando a arte muda.
Com `Cache-Control: immutable, max-age=31536000`, o navegador de quem já visitou o site
guardaria a capa antiga por um ano e nunca pediria a nova — mesmo com o deploy correto no ar.
Por isso o `netlify.toml` usa `max-age=3600, must-revalidate`: a visita repetida na mesma
hora não refaz o download, e uma capa nova aparece para todo mundo em no máximo uma hora.

Se um dia as capas pararem de mudar e você quiser cache de um ano de volta, o caminho certo
é versionar o nome do arquivo (`buddha-pt.v2.jpg`) — nunca só aumentar o `max-age`.

Para conferir uma troca de capa na hora, sem esperar: `Ctrl+Shift+R` no desktop, ou uma aba
anônima no celular.

## Pendências para você

- **Search Console**: reenviar o `sitemap.xml` e pedir indexação das novas URLs.
- **Perfil do autor**: se você tiver página de autor na Amazon, Goodreads ou LinkedIn,
  acrescente as URLs em `PERSON["sameAs"]` dentro de `build.py` e em `patch` do
  `index.html` — isso reforça a entidade "Hugo Salles" para o Google.
