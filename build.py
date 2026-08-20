#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Awakened Mind / Mente Desperta — gerador estático do ecossistema de conteúdo e SEO.
Domínio Principal Internacional: https://awakenedmindbooks.com (Inglês como raiz primária)

Gera:
  /books/<slug>/index.html                 (páginas de livro EN)
  /pt/livros/<slug>/index.html             (páginas de livro PT)
  /books/<slug>/excerpt/index.html         (páginas de trecho EN)
  /pt/livros/<slug>/trecho/index.html      (páginas de trecho PT)
  /topics/<slug>/index.html                (páginas-pilar por tema EN)
  /pt/temas/<slug>/index.html              (páginas-pilar por tema PT)
  /glossary/<slug>/index.html              (verbetes de glossário EN)
  /pt/glossario/<slug>/index.html          (verbetes de glossário PT)
  /books/index.html                        (hub EN)
  /pt/livros/index.html                    (hub PT)
  /author/index.html                       (autor EN)
  /pt/autor/index.html                     (autor PT)
  /review/index.html                       (avaliações EN)
  /pt/avalie/index.html                    (avaliações PT)
  /sitemap.xml                             (sitemap índice)
  /sitemap-en.xml                          (sitemap EN)
  /sitemap-pt.xml                          (sitemap PT)

Uso:  python build.py
"""
import json, os, re, sys, html, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "books.json").read_text(encoding="utf-8"))
SITE = DATA["site"]
BOOKS = DATA["books"]
DOMAIN = SITE["domain"]
TODAY = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()

DIMS_PATH = ROOT / "dims.json"
if not DIMS_PATH.exists():
    sys.exit("ERRO: dims.json ausente. Sem ele as capas saem com width/height errados "
             "e a pagina sofre layout shift. Rode o otimizador de imagens antes.")
DIMS = json.loads(DIMS_PATH.read_text(encoding="utf-8"))

# ---------------------------------------------------------------- excerpts
def extract_excerpts():
    """Puxa os trechos (.book-excerpt) das homes."""
    out = {}
    for lang, path in (("pt", "pt/index.html"), ("en", "index.html")):
        f = ROOT / path
        if not f.exists():
            # Fallback se ainda nao tiver migrado
            fallback = "index.html" if lang == "pt" else "en/index.html"
            f = ROOT / fallback
            if not f.exists():
                print(f"  ! aviso: {path} nao encontrado, trechos em {lang} ficarao vazios")
                continue
        for card in re.split(r'<article class="book-card', f.read_text(encoding="utf-8"))[1:]:
            m = re.search(r'id="livro-([a-z]+)"', card)
            if not m:
                continue
            key = {"avalo": "avalo", "vajra": "vajrasattva"}.get(m.group(1), m.group(1))
            bq = re.search(r'<blockquote class="book-excerpt[^"]*"\s*>(.*?)</blockquote>', card, re.S)
            if bq:
                paras = re.findall(r"<p>(.*?)</p>", bq.group(1), re.S)
                out.setdefault(key, {})[lang] = [p.strip() for p in paras]
    return out


EXCERPTS = extract_excerpts()

# ---------------------------------------------------------------- i18n
T = {
    "en": {
        "lang": "en", "locale": "en_US", "alt_locale": "pt_BR",
        "home": "Home", "books": "Books", "series": "About the Series",
        "author": "Author", "news": "News", "topics": "Topics", "glossary": "Glossary",
        "skip": "Skip to content",
        "brand": SITE["brand_en"], "series_name": SITE["series_en"],
        "about_book": "About the book",
        "for_whom": "Who this book is for",
        "inside": "What you will find inside",
        "excerpt": "From the book",
        "read_full_excerpt": "Read extended chapter excerpt",
        "faq": "Frequently asked questions",
        "buy_br": "Buy on Amazon BR",
        "pre_br": "Pre-order on Amazon BR",
        "buy_us": "Buy on Amazon US",
        "pre_us": "Pre-order on Amazon US",
        "read_ku": "Read free on Kindle Unlimited",
        "review": "Already read? Leave a review on Amazon",
        "ku": "Kindle Unlimited",
        "series_badge": "Awakened Mind Series",
        "standalone_badge": "Standalone work",
        "related": "Continue through the series",
        "related_other": "Other books",
        "author_box_title": "About the author",
        "author_more": "Meet the author",
        "cta_final": "Start reading today",
        "cta_final_sub": "Available in English and Portuguese, on Amazon and Kindle Unlimited.",
        "book_n": "Book %d · %s",
        "standalone": "Standalone work",
        "hub_title": "All Books — Awakened Mind | Hugo Salles",
        "hub_meta": "Every book by Hugo Salles: The Technologies of the Awakened Mind series, plus the standalone works on overthinking and karma. On Amazon and Kindle Unlimited.",
        "hub_h1": "All books",
        "hub_lead": "Each volume isolates a specific mental pattern — fear, attachment, confusion, guilt, anger — and translates centuries of Tibetan contemplative practice into applicable steps. Method first; meaning later, for readers who want to dig deeper.",
        "hub_series_h2": "The series: The Technologies of the Awakened Mind",
        "hub_other_h2": "Standalone works",
        "hub_theme_h2": "Start with what weighs most right now",
        "read_more": "View the book",
        "product_details": "Book details",
        "format_label": "Format",
        "format_val": "Kindle eBook (readable on any phone, tablet, or Kindle device)",
        "avail_label": "Availability",
        "avail_val": "Kindle Unlimited & Amazon purchase",
        "author_label": "Author",
        "publisher_label": "Publisher",
        "legal": "Amazon, Kindle and Kindle Unlimited are trademarks of Amazon.com, Inc.",
        "copyright": "&copy; 2026 Awakened Mind. All rights reserved.",
        "footer_series": "Series",
        "all_books": "All books",
        "breadcrumb_home": "Home",
    },
    "pt": {
        "lang": "pt-BR", "locale": "pt_BR", "alt_locale": "en_US",
        "home": "Início", "books": "Livros", "series": "Sobre a Série",
        "author": "Autor", "news": "Novidades", "topics": "Temas", "glossary": "Glossário",
        "skip": "Pular para o conteúdo",
        "brand": SITE["brand_pt"], "series_name": SITE["series_pt"],
        "about_book": "Sobre o livro",
        "for_whom": "Para quem é este livro",
        "inside": "O que você vai encontrar",
        "excerpt": "Trecho do livro",
        "read_full_excerpt": "Ler amostra estendida do capítulo",
        "faq": "Perguntas frequentes",
        "buy_br": "Comprar na Amazon BR",
        "pre_br": "Pré-venda na Amazon BR",
        "buy_us": "Comprar na Amazon US",
        "pre_us": "Pré-venda na Amazon US",
        "read_ku": "Leia grátis no Kindle Unlimited",
        "review": "Já leu? Deixe sua avaliação na Amazon",
        "ku": "Kindle Unlimited",
        "series_badge": "Série Mente Desperta",
        "standalone_badge": "Obra independente",
        "related": "Continue pela série",
        "related_other": "Outros livros",
        "author_box_title": "Sobre o autor",
        "author_more": "Conhecer o autor",
        "cta_final": "Comece a ler hoje",
        "cta_final_sub": "Disponível em português e em inglês, na Amazon e no Kindle Unlimited.",
        "book_n": "Livro %d · %s",
        "standalone": "Obra independente",
        "hub_title": "Todos os livros — Mente Desperta | Hugo Salles",
        "hub_meta": "Todos os livros de Hugo Salles: a série As Tecnologias da Mente Desperta e as obras independentes sobre overthinking e karma. Na Amazon e no Kindle.",
        "hub_h1": "Todos os livros",
        "hub_lead": "Cada volume isola um padrão mental específico — medo, apego, confusão, culpa, raiva — e traduz séculos de prática contemplativa tibetana em passos aplicáveis. Método primeiro; significado depois, para quem quiser ir mais fundo.",
        "hub_series_h2": "A série: As Tecnologias da Mente Desperta",
        "hub_other_h2": "Obras independentes",
        "hub_theme_h2": "Comece pelo que mais pesa agora",
        "read_more": "Ver o livro",
        "product_details": "Detalhes do livro",
        "format_label": "Formato",
        "format_val": "eBook Kindle (compatível com qualquer dispositivo via app gratuito Kindle)",
        "avail_label": "Disponibilidade",
        "avail_val": "Kindle Unlimited e compra avulsa na Amazon",
        "author_label": "Autor",
        "publisher_label": "Editora",
        "legal": "Amazon, Kindle e Kindle Unlimited são marcas registradas da Amazon.com, Inc.",
        "copyright": "&copy; 2026 Mente Desperta. Todos os direitos reservados.",
        "footer_series": "Série",
        "all_books": "Todos os livros",
        "breadcrumb_home": "Início",
    },
}

HOME = {"en": "/", "pt": "/pt/"}
HUB = {"en": "/books/", "pt": "/pt/livros/"}
AUTHOR_URL = {"en": "/author/", "pt": "/pt/autor/"}
REVIEW_URL = {"en": "/review/", "pt": "/pt/avalie/"}

AUTHOR_BLURB = {
    "en": "Hugo Salles is a writer, lawyer and executive. For over twenty years he has led teams and projects — an experience that brought his study of Mahayana and Tibetan Buddhism into contact with the concrete problems of everyday life. He has translated selected Buddhist sutras into Portuguese and writes The Technologies of the Awakened Mind.",
    "pt": "Hugo Salles é escritor, advogado e executivo. Há mais de vinte anos atua na liderança de equipes e projetos — experiência que aproximou seu estudo do budismo Mahayana e tibetano das questões concretas do dia a dia. Traduziu para o português sutras budistas selecionados e escreve a série As Tecnologias da Mente Desperta.",
}

ICON_EXT = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>'
            '<polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>')

ICON_KU = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
           '<path d="M21 5c-1.11-.35-2.33-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5-1.45-1.1-3.55-1.5-5.5-1.5S2.45 4.9 1 6v14.65c0 '
           '.25.25.5.5.5.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5 1.35-.85 3.8-1.5 5.5-1.5 1.65 0 '
           '3.35.3 4.75 1.05.1.05.15.05.25.05.25 0 .5-.25.5-.5V6c-.6-.45-1.25-.75-2-1zM21 18.5c-1.1-.35-2.3-.5-3.5-.5-1.7 '
           '0-4.15.65-5.5 1.5V8c1.35-.85 3.8-1.5 5.5-1.5 1.2 0 2.4.15 3.5.5v11.5z"/></svg>')

_GF = ("https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600&"
       "family=Outfit:wght@300;400;500;600&display=swap")
FONTS = (f'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         f'  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         f'  <link rel="preload" as="style" href="{_GF}">\n'
         f'  <link rel="stylesheet" href="{_GF}" media="print" onload="this.media=\'all\'">\n'
         f'  <noscript><link rel="stylesheet" href="{_GF}"></noscript>')


def e(s):
    return html.escape(s, quote=True)


def url_of(book, lang):
    slug = book[lang]["slug"]
    return f"/books/{slug}/" if lang == "en" else f"/pt/livros/{slug}/"


def excerpt_url_of(book, lang):
    slug = book[lang]["slug"]
    return f"/books/{slug}/excerpt/" if lang == "en" else f"/pt/livros/{slug}/trecho/"


def cover(book, lang):
    return f"/assets/covers/{book['cover']}-{lang}"


def cover_dims(book, lang):
    return DIMS.get(f"{book['cover']}-{lang}", [640, 1024])


# ---------------------------------------------------------------- chrome
def nav(lang, alt_href, current=None):
    t = T[lang]
    pt_cls = ' class="active"' if lang == "pt" else ""
    en_cls = ' class="active"' if lang == "en" else ""
    about_hash = "#about" if lang == "en" else "#sobre"
    news_hash = "#news" if lang == "en" else "#novidades"
    return f"""  <nav class="site-nav" role="navigation" aria-label="{t['books']}">
    <div class="nav-inner container">
      <a href="{HOME[lang]}" class="nav-logo" aria-label="{t['brand']}">
        <span class="logo-text">{t['brand']}</span>
      </a>
      <div class="nav-controls">
        <div class="global-lang-toggle bp-lang" role="group" aria-label="Select language">
          <a href="{alt_href['en']}"{en_cls} hreflang="en" lang="en"{' aria-current="page"' if lang=='en' else ''}>EN</a>
          <a href="{alt_href['pt']}"{pt_cls} hreflang="pt-BR" lang="pt-BR"{' aria-current="page"' if lang=='pt' else ''}>PT</a>
        </div>
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="{t['books']}">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
      <ul class="nav-menu" id="nav-menu" role="list">
        <li><a href="{HUB[lang]}"{' aria-current="page"' if current=='books' else ''}>{t['books']}</a></li>
        <li><a href="{HOME[lang]}{about_hash}">{t['series']}</a></li>
        <li><a href="{AUTHOR_URL[lang]}"{' aria-current="page"' if current=='author' else ''}>{t['author']}</a></li>
        <li><a href="{HOME[lang]}{news_hash}">{t['news']}</a></li>
      </ul>
    </div>
  </nav>"""


def footer(lang):
    t = T[lang]
    about_hash = "#about" if lang == "en" else "#sobre"
    links = "\n".join(
        f'            <li><a href="{url_of(b, lang)}">{e(b[lang]["name"])}</a></li>' for b in BOOKS)
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <span class="footer-logo">{t['brand']}</span>
        <p class="footer-copy">{t['copyright']}</p>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <p class="footer-col-title">{t['footer_series']}</p>
          <ul>
            <li><a href="{HUB[lang]}">{t['all_books']}</a></li>
            <li><a href="{HOME[lang]}{about_hash}">{t['series']}</a></li>
            <li><a href="{AUTHOR_URL[lang]}">{t['author']}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <p class="footer-col-title">{t['books']}</p>
          <ul>
{links}
          </ul>
        </div>
      </div>
    </div>
    <hr class="gold-thread gold-thread--full" aria-hidden="true">
    <div class="container footer-bottom">
      <p class="footer-legal">{t['legal']}</p>
    </div>
  </footer>"""


def head(lang, *, title, desc, canonical, alt, og_image, og_type="website",
         jsonld="", extra="", keywords=None, robots="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"):
    t = T[lang]
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="{robots}">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="author" content="Hugo Salles">
  <link rel="canonical" href="{DOMAIN}{canonical}">
  <link rel="alternate" hreflang="en" href="{DOMAIN}{alt['en']}">
  <link rel="alternate" hreflang="pt-BR" href="{DOMAIN}{alt['pt']}">
  <link rel="alternate" hreflang="x-default" href="{DOMAIN}{alt['en']}">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <meta property="og:site_name" content="{t['brand']}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{DOMAIN}{canonical}">
  <meta property="og:image" content="{DOMAIN}{og_image}">
  <meta property="og:image:alt" content="{e(title)}">
  <meta property="og:locale" content="{t['locale']}">
  <meta property="og:locale:alternate" content="{t['alt_locale']}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(desc)}">
  <meta name="twitter:image" content="{DOMAIN}{og_image}">
{extra}  {FONTS}
  <link rel="stylesheet" href="/styles.css">
{jsonld}</head>
<body>
  <script>document.documentElement.classList.add('js');</script>

  <a href="#conteudo" class="skip-link">{t['skip']}</a>
"""


def ld(obj):
    return ('  <script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n  </script>\n")


def breadcrumb(lang, trail):
    """trail: list of (name, href|None)"""
    t = T[lang]
    items = []
    for i, (name, href) in enumerate(trail):
        if href:
            items.append(f'<li><a href="{href}">{e(name)}</a></li>')
        else:
            items.append(f'<li><span aria-current="page">{e(name)}</span></li>')
    return ('  <nav class="bp-breadcrumb container" aria-label="Breadcrumb">\n'
            '    <ol>\n      ' + "\n      ".join(items) + "\n    </ol>\n  </nav>\n")


def breadcrumb_ld(lang, trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             **({"item": DOMAIN + h} if h else {})}
            for i, (n, h) in enumerate(trail)
        ],
    }


PERSON = {
    "@type": "Person",
    "@id": f"{DOMAIN}/#hugo-salles",
    "name": "Hugo Salles",
    "url": f"{DOMAIN}/author/",
    "image": f"{DOMAIN}/assets/favicon.png",
    "jobTitle": "Escritor",
    "description": "Escritor, advogado e executivo. Autor da série The Technologies of the Awakened Mind / As Tecnologias da Mente Desperta.",
    "sameAs": [
        "https://www.amazon.com/stores/Hugo-Salles/author/B0H6CC28L9",
        "https://www.amazon.com.br/stores/Hugo-Salles/author/B0H6CC28L9",
        "https://www.instagram.com/despertabooks",
        "https://mentedespertabooks.substack.com",
    ],
}


# ---------------------------------------------------------------- book page
def cta_block(book, lang, big=False):
    t = T[lang]
    br = t["pre_br"] if book["status_br"] == "preorder" else t["buy_br"]
    us = t["pre_us"] if book["status_us"] == "preorder" else t["buy_us"]
    book_slug = book[lang]['slug']
    utm = f"?tag=mentedesperta-20&utm_source=awakenedmindbooks&utm_medium=site&utm_campaign={book_slug}"
    first_label, first_url = (us, f"https://www.amazon.com/dp/{book['asin_us']}{utm}")
    second_label, second_url = (br, f"https://www.amazon.com.br/dp/{book['asin_br']}{utm}")
    review_asin = book["asin_us"]
    review_dom = "amazon.com"
    if lang == "pt":
        first_label, first_url, second_label, second_url = second_label, second_url, first_label, first_url
        review_asin, review_dom = book["asin_br"], "amazon.com.br"
    review_url = f"https://www.{review_dom}/review/create-review?asin={review_asin}&tag=mentedesperta-20&utm_source=awakenedmindbooks&utm_medium=site&utm_campaign={book_slug}"
    
    return f"""      <div class="book-ctas bp-ctas" data-book="{book_slug}">
        <a href="{first_url}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--primary">{first_label} {ICON_EXT}</a>
        <a href="{second_url}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--secondary">{second_label} {ICON_EXT}</a>
      </div>
      <p class="bp-review-hint"><a href="{review_url}" target="_blank" rel="noopener noreferrer">{t['review']} &rarr;</a></p>"""


def related_block(book, lang):
    t = T[lang]
    others = [b for b in BOOKS if b["key"] != book["key"]]
    same = [b for b in others if b["series"] == book["series"]]
    rest = [b for b in others if b["series"] != book["series"]]
    ordered = (same + rest)[:6]
    cards = []
    for b in ordered:
        d = cover_dims(b, lang)
        cards.append(f"""        <a class="bp-rel-card" href="{url_of(b, lang)}" style="--book-accent: {b['accent']}">
          <picture>
            <source srcset="{cover(b, lang)}.webp" type="image/webp">
            <img src="{cover(b, lang)}.jpg" width="{d[0]}" height="{d[1]}" alt="{e(b[lang]['full_title'])} — {e('capa do livro' if lang=='pt' else 'book cover')}" loading="lazy" decoding="async">
          </picture>
          <span class="bp-rel-name">{e(b[lang]['name'])}</span>
          <span class="bp-rel-theme">{e(b[lang]['theme'])}</span>
        </a>""")
    return f"""  <section class="bp-section bp-related">
    <div class="container">
      <h2 class="bp-h2">{t['related'] if book['series'] else t['related_other']}</h2>
      <div class="bp-rel-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>"""


def book_page(book, lang):
    t = T[lang]
    d = book[lang]
    alt = {"en": url_of(book, "en"), "pt": url_of(book, "pt")}
    canonical = url_of(book, lang)
    dims = cover_dims(book, lang)
    eyebrow = (t["book_n"] % (book["order"], t["series_name"])) if book["series"] else t["standalone"]

    excerpt = EXCERPTS.get(book["key"], {}).get(lang, [])
    excerpt_html = ""
    if excerpt:
        paras = "\n".join(f"          <p>{p}</p>" for p in excerpt)
        excerpt_url = excerpt_url_of(book, lang)
        excerpt_html = f"""  <section class="bp-section" id="trecho">
    <div class="container bp-narrow">
      <h2 class="bp-h2">{t['excerpt']}</h2>
      <blockquote class="book-excerpt active">
{paras}
      </blockquote>
      <p style="text-align: right; margin-top: 1rem;"><a class="bp-inline-link" href="{excerpt_url}">{t['read_full_excerpt']} &rarr;</a></p>
    </div>
  </section>"""

    faq_html = "\n".join(
        f"""        <details class="bp-faq-item">
          <summary>{e(f['q'])}</summary>
          <div class="bp-faq-a"><p>{e(f['a'])}</p></div>
        </details>""" for f in d["faq"])

    body_html = "\n".join(f"        <p>{p}</p>" for p in d["body"])
    for_whom = "\n".join(f"          <li>{e(x)}</li>" for x in d["for_whom"])
    inside = "\n".join(f"          <li>{e(x)}</li>" for x in d["inside"])

    trail = [(t["breadcrumb_home"], HOME[lang]), (t["books"], HUB[lang]), (d["name"], None)]

    # WorkExample & ReadAction
    work_example = {
        "@type": "Book",
        "@id": f"{DOMAIN}{canonical}#ebook",
        "name": d["full_title"],
        "bookFormat": "https://schema.org/EBook",
        "inLanguage": t["lang"],
        "isbn": book["asin_us"] if lang == "en" else book["asin_br"],
        "potentialAction": {
            "@type": "ReadAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"https://www.amazon.com/dp/{book['asin_us']}" if lang == "en" else f"https://www.amazon.com.br/dp/{book['asin_br']}"
            },
            "expectsAcceptanceOf": {
                "@type": "Offer",
                "priceCurrency": "USD" if lang == "en" else "BRL",
                "availability": "https://schema.org/InStock" if (book["status_us"] == "available" if lang == "en" else book["status_br"] == "available") else "https://schema.org/PreOrder",
                "seller": {"@type": "Organization", "name": "Amazon"}
            }
        },
        "offers": {
            "@type": "Offer",
            "url": f"https://www.amazon.com/dp/{book['asin_us']}" if lang == "en" else f"https://www.amazon.com.br/dp/{book['asin_br']}",
            "priceCurrency": "USD" if lang == "en" else "BRL",
            "availability": "https://schema.org/InStock" if (book["status_us"] == "available" if lang == "en" else book["status_br"] == "available") else "https://schema.org/PreOrder"
        }
    }

    graph = [
        PERSON,
        {
            "@type": "Book",
            "@id": f"{DOMAIN}{canonical}#book",
            "name": d["full_title"],
            "alternateName": d["name"],
            "headline": d["subtitle"],
            "description": d["meta"],
            "url": f"{DOMAIN}{canonical}",
            "image": f"{DOMAIN}{cover(book, lang)}.jpg",
            "inLanguage": t["lang"],
            "bookFormat": "https://schema.org/EBook",
            "datePublished": book["published"],
            "author": {"@id": f"{DOMAIN}/#hugo-salles"},
            "publisher": {"@type": "Organization", "name": SITE["brand_en"] if lang=="en" else SITE["brand_pt"], "url": DOMAIN},
            "about": d["theme"],
            "keywords": d["keywords"],
            "workExample": [work_example],
            "sameAs": [
                f"https://www.amazon.com/dp/{book['asin_us']}",
                f"https://www.amazon.com.br/dp/{book['asin_br']}",
            ],
            **({"isPartOf": {
                "@type": "BookSeries",
                "@id": f"{DOMAIN}{HUB[lang]}#series",
                "name": t["series_name"],
                "url": f"{DOMAIN}{HUB[lang]}",
            }, "position": book["order"]} if book["series"] else {}),
        },
        {
            "@type": "FAQPage",
            "@id": f"{DOMAIN}{canonical}#faq",
            "mainEntity": [
                {"@type": "Question", "name": f["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                for f in d["faq"]
            ],
        },
        breadcrumb_ld(lang, trail),
    ]
    jsonld = ld({"@context": "https://schema.org", "@graph": graph})

    extra = (f'  <link rel="preload" as="image" href="{cover(book, lang)}.webp" '
             f'type="image/webp" fetchpriority="high">\n')

    is_avail = (book["status_us"] == "available" if lang == "en" else book["status_br"] == "available")
    ku_badge_html = f'<span class="badge badge--ku" aria-label="{t["ku"]}">{ICON_KU} {t["ku"]}</span>' if is_avail else ''

    parts = [head(lang, title=d["seo_title"], desc=d["meta"], keywords=d["keywords"],
                  canonical=canonical, alt=alt, og_image=f"{cover(book, lang)}.jpg",
                  og_type="book", jsonld=jsonld, extra=extra)]
    parts.append(nav(lang, alt, current="books"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    parts.append(f"""
  <article class="bp" style="--book-accent: {book['accent']}">
    <header class="bp-hero">
      <div class="container bp-hero-inner">
        <div class="bp-cover">
          <div class="book-cover-wrapper">
            <picture>
              <source srcset="{cover(book, lang)}.webp" type="image/webp">
              <img class="book-cover active" src="{cover(book, lang)}.jpg" width="{dims[0]}" height="{dims[1]}" alt="{e(d['full_title'])} — {e('book cover, by Hugo Salles' if lang=='en' else 'capa do livro, de Hugo Salles')}" fetchpriority="high" decoding="async">
            </picture>
            <div class="cover-light-effect" aria-hidden="true"></div>
          </div>
        </div>
        <div class="bp-headline">
          <p class="bp-eyebrow">{e(eyebrow)}</p>
          <h1 class="bp-h1">{e(d['name'])}</h1>
          <p class="bp-subtitle">{e(d['subtitle'])}</p>
          <div class="book-badges">
            {ku_badge_html}
            <span class="badge badge--series">{t['series_badge'] if book['series'] else t['standalone_badge']}</span>
          </div>
{cta_block(book, lang)}
        </div>
      </div>
    </header>

    <section class="bp-section" id="sobre-o-livro">
      <div class="container bp-narrow">
        <h2 class="bp-h2">{t['about_book']}</h2>
        <p class="bp-lead">{e(d['lead'])}</p>
{body_html}
      </div>
    </section>

    <section class="bp-section bp-section--alt" id="detalhes">
      <div class="container bp-narrow">
        <h2 class="bp-h2">{t['product_details']}</h2>
        <div class="product-meta-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.8rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{t['format_label']}</p>
            <p style="margin: 0; font-size: 0.95rem;">{t['format_val']}</p>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.8rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{t['avail_label']}</p>
            <p style="margin: 0; font-size: 0.95rem;">{t['avail_val']}</p>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.8rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{t['author_label']}</p>
            <p style="margin: 0; font-size: 0.95rem;">Hugo Salles</p>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 8px;">
            <p style="font-size: 0.8rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{t['publisher_label']}</p>
            <p style="margin: 0; font-size: 0.95rem;">{'Awakened Mind' if lang=='en' else 'Mente Desperta'}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="bp-section" id="para-quem">
      <div class="container bp-cols">
        <div>
          <h2 class="bp-h2">{t['for_whom']}</h2>
          <ul class="bp-list">
{for_whom}
          </ul>
        </div>
        <div>
          <h2 class="bp-h2">{t['inside']}</h2>
          <ul class="bp-list">
{inside}
          </ul>
        </div>
      </div>
    </section>
""")
    if excerpt_html:
        parts.append(excerpt_html + "\n")
    parts.append(f"""
  <section class="bp-section bp-section--alt" id="faq">
    <div class="container bp-narrow">
      <h2 class="bp-h2">{t['faq']}</h2>
      <div class="bp-faq">
{faq_html}
      </div>
    </div>
  </section>

  <section class="bp-section bp-final">
    <div class="container bp-narrow">
      <h2 class="bp-h2">{t['cta_final']}</h2>
      <p class="bp-final-sub">{t['cta_final_sub']}</p>
{cta_block(book, lang)}
    </div>
  </section>

  <section class="bp-section bp-authorbox">
    <div class="container bp-narrow">
      <h2 class="bp-h2">{t['author_box_title']}</h2>
      <p>{AUTHOR_BLURB[lang]}</p>
      <p><a class="bp-inline-link" href="{AUTHOR_URL[lang]}">{t['author_more']} <span aria-hidden="true">&rarr;</span></a></p>
    </div>
  </section>
""")
    parts.append(related_block(book, lang))
    parts.append("\n  </article>\n  </main>\n\n")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- excerpt page
def excerpt_page(book, lang):
    t = T[lang]
    d = book[lang]
    canonical = excerpt_url_of(book, lang)
    alt = {"en": excerpt_url_of(book, "en"), "pt": excerpt_url_of(book, "pt")}
    book_url = url_of(book, lang)
    title = f"{d['name']} — {t['excerpt']} | Hugo Salles"
    desc = f"Read an excerpt from {d['name']}, by Hugo Salles. {d['meta']}" if lang == 'en' else f"Leia um trecho de {d['name']}, de Hugo Salles. {d['meta']}"
    
    trail = [(t["breadcrumb_home"], HOME[lang]), (t["books"], HUB[lang]), (d["name"], book_url), (t["excerpt"], None)]
    
    excerpt = EXCERPTS.get(book["key"], {}).get(lang, [])
    paras = "\n".join(f"          <p>{p}</p>" for p in excerpt) if excerpt else "<p><!-- TODO: author excerpt text --></p>"

    graph = [
        PERSON,
        {
            "@type": "Article",
            "@id": f"{DOMAIN}{canonical}#article",
            "headline": title,
            "description": desc,
            "inLanguage": t["lang"],
            "url": f"{DOMAIN}{canonical}",
            "author": {"@id": f"{DOMAIN}/#hugo-salles"},
            "publisher": {"@type": "Organization", "name": SITE["brand_en"] if lang=="en" else SITE["brand_pt"], "url": DOMAIN},
            "about": {"@id": f"{DOMAIN}{book_url}#book"}
        },
        breadcrumb_ld(lang, trail),
    ]

    parts = [head(lang, title=title, desc=desc, canonical=canonical, alt=alt,
                  og_image=f"{cover(book, lang)}.jpg", og_type="article",
                  jsonld=ld({"@context": "https://schema.org", "@graph": graph}))]
    parts.append(nav(lang, alt, current="books"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    parts.append(f"""
  <article class="bp" style="--book-accent: {book['accent']}">
    <header class="bp-hub-header">
      <div class="container bp-narrow">
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
        <p class="bp-eyebrow"><a href="{book_url}" class="bp-inline-link">&larr; {d['name']}</a></p>
        <h1 class="bp-h1">{t['excerpt']}: {e(d['name'])}</h1>
        <p class="bp-lead">{e(d['subtitle'])}</p>
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
      </div>
    </header>

    <section class="bp-section">
      <div class="container bp-narrow">
        <blockquote class="book-excerpt active" style="font-size: 1.15rem; line-height: 1.8;">
{paras}
        </blockquote>
        
        <div style="margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.03); border-radius: 12px; text-align: center;">
          <h2 class="bp-h2" style="margin-bottom: 0.5rem;">{t['cta_final']}</h2>
          <p style="margin-bottom: 1.5rem;">{t['cta_final_sub']}</p>
{cta_block(book, lang)}
        </div>
      </div>
    </section>
  </article>
  </main>
""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- topic pages
THEMES = [
    {
        "key": "ansiedade",
        "book_key": "tara",
        "en": {
            "slug": "anxiety",
            "name": "Anxiety",
            "title": "How to Deal with Anxiety: The Tibetan Method of Tara | Awakened Mind",
            "meta": "Anxiety is not conquered through mental debate. Discover the practical Tibetan Buddhist method to dissolve anxiety loops and act with courage.",
            "lead": "Anxiety is neither a design flaw nor a personal failure: it is a state of hypervigilance where attention has learned to anticipate future dangers.",
        },
        "pt": {
            "slug": "ansiedade",
            "name": "Ansiedade",
            "title": "Como Lidar com a Ansiedade: O Método Tibetano de Tara | Mente Desperta",
            "meta": "Ansiedade não se vence no debate mental. Conheça o método prático do budismo tibetano para dissolver o ciclo da ansiedade e agir com coragem.",
            "lead": "A ansiedade não é um defeito de fábrica nem uma falha de caráter: é uma resposta de hipervigilância da atenção que aprendeu a antecipar perigos futuros.",
        }
    },
    {
        "key": "medo",
        "book_key": "tara",
        "en": {
            "slug": "fear",
            "name": "Fear",
            "title": "Fear as Technology: How to Act Despite Panic | Awakened Mind",
            "meta": "Courage is not the absence of fear, but the ability to act in its presence. Tibetan practices to break through paralysis.",
            "lead": "There is a fundamental difference between feeling fear and being governed by it. The Tara tradition teaches how to move through contraction rather than fighting it.",
        },
        "pt": {
            "slug": "medo",
            "name": "Medo",
            "title": "O Medo como Tecnologia: Como Agir Apesar do Pânico | Mente Desperta",
            "meta": "Coragem não é a ausência de medo, mas a capacidade de agir na presença dele. Práticas tibetanas para atravessar a paralisia.",
            "lead": "Existe uma diferença crucial entre sentir medo e ser governado pelo medo. A tradição de Tara ensina a atravessar a contração em vez de lutar contra ela.",
        }
    },
    {
        "key": "apego-emocional",
        "book_key": "avalo",
        "en": {
            "slug": "emotional-attachment",
            "name": "Emotional Attachment",
            "title": "Emotional Attachment vs Genuine Love: The Avalokiteshvara View | Awakened Mind",
            "meta": "Love without dependency, embrace without suffocating. Understand the Buddhist difference between clinging and lucid compassion.",
            "lead": "Attachment mistakes possession for care and dependency for love. When we demand that another person serve as our emotional anchor, relationships turn into contracts of mutual surveillance.",
        },
        "pt": {
            "slug": "apego-emocional",
            "name": "Apego Emocional",
            "title": "Apego Emocional vs Amor Genuíno: A Visão de Avalokiteshvara | Mente Desperta",
            "meta": "Amar sem depender, acolher sem aprisionar. Entenda a diferença budista entre apego que gera sofrimento e compaixão lúcida.",
            "lead": "O apego confunde posse com cuidado e dependência com amor. Quando exigimos que o outro seja a nossa âncora, transformamos a relação em um contrato de vigilância mútua.",
        }
    },
    {
        "key": "confusao-mental",
        "book_key": "manjushri",
        "en": {
            "slug": "mental-confusion",
            "name": "Mental Confusion",
            "title": "Mental Confusion and Decision Paralysis: The Sword of Manjushri | Awakened Mind",
            "meta": "How to cut through cognitive fog, overcome decision paralysis, and perceive reality with sharp discernment.",
            "lead": "Mental confusion does not stem from a lack of information, but from a buildup of unexamined interpretations. The sword of Manjushri represents discernment that severs the superfluous.",
        },
        "pt": {
            "slug": "confusao-mental",
            "name": "Confusão Mental",
            "title": "Confusão Mental e Paralisia de Decisão: A Espada de Manjushri | Mente Desperta",
            "meta": "Como cortar o excesso de opções, sair da névoa mental e enxergar a realidade com discernimento afiado.",
            "lead": "A confusão mental não surge da falta de informação, mas do excesso de interpretações não examinadas. A espada de Manjushri representa a clareza que corta o supérfluo.",
        }
    },
    {
        "key": "culpa",
        "book_key": "vajrasattva",
        "en": {
            "slug": "guilt",
            "name": "Guilt and Self-Punishment",
            "title": "Overcoming Guilt Without Self-Punishment: Vajrasattva Practice | Awakened Mind",
            "meta": "Guilt cannot fix the past; it only prolongs suffering. Learn the four opponent powers of Tibetan Buddhist purification.",
            "lead": "A person carrying guilt often seeks a sentence rather than freedom. Vajrasattva teaches how to cleanse regret without erasing responsibility.",
        },
        "pt": {
            "slug": "culpa",
            "name": "Culpa e Autopunição",
            "title": "Como Superar a Culpa sem Autopunição: A Prática de Vajrasattva | Mente Desperta",
            "meta": "A culpa não repara o passado; apenas perpetua a paralisia. Conheça as quatro forças de purificação do budismo tibetano.",
            "lead": "Quem carrega culpa muitas vezes não busca alívio, mas confirmação de condenação. Vajrasattva ensina a lavar o erro sem apagar a responsabilidade.",
        }
    },
    {
        "key": "raiva",
        "book_key": "vajrapani",
        "en": {
            "slug": "anger",
            "name": "Anger and Powerlessness",
            "title": "Transforming Anger into Conscious Power: Vajrapani Method | Awakened Mind",
            "meta": "Repressed anger poisons; uncontrolled rage destroys. Discover how to channel the energy of anger into resolute determination.",
            "lead": "Anger is rapid, concentrated energy triggered by felt powerlessness before an obstacle. Vajrapani teaches how to harness force without the poison.",
        },
        "pt": {
            "slug": "raiva",
            "name": "Raiva e Impotência",
            "title": "Transformando Raiva em Poder Consciente: O Método de Vajrapani | Mente Desperta",
            "meta": "A raiva reprimida intoxica; a descontrolada destrói. Descubra como canalizar a energia da raiva em determinação inabalável.",
            "lead": "A raiva é uma energia veloz e potente que surge quando nos sentimos impotentes diante de um obstáculo. Vajrapani ensina a usar a força sem o veneno.",
        }
    },
    {
        "key": "overthinking",
        "book_key": "buda",
        "en": {
            "slug": "overthinking",
            "name": "Overthinking and Rumination",
            "title": "How to Stop Overthinking: The Buddhist Protocol to End the Loop | Awakened Mind",
            "meta": "21 Buddhist practices to switch off middle-of-the-night rumination and regain control over your attention.",
            "lead": "Overthinking does not solve problems: it generates an endless simulation that drains the energy to live. The Buddha provided sequential protocols to displace intrusive thought patterns.",
        },
        "pt": {
            "slug": "overthinking",
            "name": "Overthinking e Ruminação",
            "title": "Como Parar de Pensar Demais: O Protocolo Budista para Encerrar o Looping | Mente Desperta",
            "meta": "21 práticas budistas para desativar a ruminação mental às duas da manhã e retomar o controle da atenção.",
            "lead": "Pensar demais não resolve problemas: cria uma simulação infinita que consome a energia de viver. O Buda deixou procedimentos objetivos para substituir pensamentos intrusivos.",
        }
    },
    {
        "key": "karma",
        "book_key": "karma",
        "en": {
            "slug": "karma",
            "name": "Karma: Cause and Effect",
            "title": "What Karma Really Means: Cause, Consequence, and Practical Action | Awakened Mind",
            "meta": "Karma is neither cosmic retribution nor rigid fate: it is the natural consequence of accumulated intentions and deeds.",
            "lead": "Demystifying the most misunderstood Eastern concept in the West: karma simply means intentional action, and understanding its mechanisms is the only way to reshape your path.",
        },
        "pt": {
            "slug": "karma",
            "name": "Karma e Causa e Efeito",
            "title": "O que é Karma de Verdade: Causa, Consequência e Ação Prática | Mente Desperta",
            "meta": "Karma não é destino nem castigo cósmico: é consequência natural de atos, decisões e hábitos acumulados.",
            "lead": "Desmistificando o conceito oriental mais distorcido no Ocidente: karma é ação com intenção, e compreender suas engrenagens é o único modo de mudar o futuro.",
        }
    },
    {
        "key": "luto",
        "book_key": None,
        "en": {
            "slug": "grief",
            "name": "Grief and Loss",
            "title": "Navigating Grief: The Compassion of Kshitigarbha | Awakened Mind",
            "meta": "Unacknowledged loss, quiet farewells, and grief with no social licence. Find shelter in the contemplative tradition of Kshitigarbha.",
            "lead": "Not all grief comes with a funeral or public recognition. The wisdom of Kshitigarbha offers grounded presence for wounds the world tries to rush past.",
        },
        "pt": {
            "slug": "luto",
            "name": "Luto e Perda",
            "title": "Como Atravessar o Luto: A Visão de Kshitigarbha | Mente Desperta",
            "meta": "Perda sem licença social, despedidas silenciosas e o luto que não teve velório. Encontre apoio na tradição de Kshitigarbha.",
            "lead": "Nem toda perda tem velório ou reconhecimento público. A sabedoria de Kshitigarbha oferece um refúgio para as dores que a sociedade insiste em apressar.",
        }
    }
]


def topic_url_of(topic, lang):
    slug = topic[lang]["slug"]
    return f"/topics/{slug}/" if lang == "en" else f"/pt/temas/{slug}/"


def topic_page(topic, lang):
    t = T[lang]
    d = topic[lang]
    canonical = topic_url_of(topic, lang)
    alt = {"en": topic_url_of(topic, "en"), "pt": topic_url_of(topic, "pt")}
    
    book = next((b for b in BOOKS if b["key"] == topic["book_key"]), None) if topic.get("book_key") else None
    trail = [(t["breadcrumb_home"], HOME[lang]), (t["topics"], None), (d["name"], None)]
    
    graph = [
        PERSON,
        {
            "@type": "Article",
            "@id": f"{DOMAIN}{canonical}#article",
            "headline": d["title"],
            "description": d["meta"],
            "inLanguage": t["lang"],
            "url": f"{DOMAIN}{canonical}",
            "author": {"@id": f"{DOMAIN}/#hugo-salles"},
            "publisher": {"@type": "Organization", "name": SITE["brand_en"] if lang=="en" else SITE["brand_pt"], "url": DOMAIN},
        },
        breadcrumb_ld(lang, trail),
    ]
    
    book_card_html = ""
    if book:
        bd = book[lang]
        book_dims = cover_dims(book, lang)
        book_url = url_of(book, lang)
        book_card_html = f"""
        <div style="margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.03); border: 1px solid var(--gold); border-radius: 12px; display: flex; flex-wrap: wrap; gap: 2rem; align-items: center;">
          <div style="flex: 0 0 140px;">
            <a href="{book_url}">
              <picture>
                <source srcset="{cover(book, lang)}.webp" type="image/webp">
                <img src="{cover(book, lang)}.jpg" width="{book_dims[0]}" height="{book_dims[1]}" alt="{e(bd['full_title'])}" style="border-radius: 6px; width: 100%; height: auto;" loading="lazy">
              </picture>
            </a>
          </div>
          <div style="flex: 1 1 300px;">
            <p style="font-size: 0.85rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{'Recommended book to go deeper' if lang=='en' else 'Livro recomendado para aprofundar'}</p>
            <h3 style="font-family: 'Oswald', sans-serif; font-size: 1.4rem; margin: 0 0 0.5rem 0;"><a href="{book_url}" class="bp-inline-link">{e(bd['name'])}</a></h3>
            <p style="font-size: 0.95rem; margin-bottom: 1rem;">{e(bd['subtitle'])}</p>
            {cta_block(book, lang)}
          </div>
        </div>
        """
        
    parts = [head(lang, title=d["title"], desc=d["meta"], canonical=canonical, alt=alt,
                  og_image="/assets/social-share-en.jpg" if lang=="en" else "/assets/social-share.jpg",
                  og_type="article", jsonld=ld({"@context": "https://schema.org", "@graph": graph}))]
    parts.append(nav(lang, alt, current="books"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    parts.append(f"""
  <article class="bp">
    <header class="bp-hub-header">
      <div class="container bp-narrow">
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
        <p class="bp-eyebrow">{'Topic · The Technologies of the Awakened Mind' if lang=='en' else 'Tema · As Tecnologias da Mente Desperta'}</p>
        <h1 class="bp-h1">{e(d['name'])}</h1>
        <p class="bp-lead">{e(d['lead'])}</p>
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
      </div>
    </header>

    <section class="bp-section">
      <div class="container bp-narrow">
        <div style="line-height: 1.8; font-size: 1.1rem;">
          <h2 class="bp-h2">{'1. Understanding the pattern' if lang=='en' else '1. Compreendendo o padrão'}</h2>
          <p>{'How the Tibetan contemplative tradition analyzes the root of this disturbance and why fighting it often reinforces the cycle.' if lang=='en' else 'Como a tradição contemplativa tibetana analisa a raiz desta perturbação e por que lutar contra ela costuma agravar o ciclo.'}</p>
          
          <h2 class="bp-h2">{'2. The transformative technology' if lang=='en' else '2. A tecnologia de transformação'}</h2>
          <p>{'The practical procedure to observe the mind in action, interrupt automatic reactivity, and anchor attention in the present moment.' if lang=='en' else 'O procedimento prático para observar a mente em ação, interromper a reação automática e ancorar a atenção no presente.'}</p>
          
          <h2 class="bp-h2">{'3. Step-by-step practice' if lang=='en' else '3. Prática passo a passo'}</h2>
          <p>{'A 5 to 10-minute applicable exercise for moments of tension or daily routine.' if lang=='en' else 'Exercício aplicável de 5 a 10 minutos para momentos de crise ou rotina diária.'}</p>
        </div>

        {book_card_html}
      </div>
    </section>
  </article>
  </main>
""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- glossary pages
GLOSSARY = [
    {
        "key": "tara",
        "book_key": "tara",
        "en": {
            "slug": "tara",
            "term": "Tara (Noble Tara)",
            "title": "Who is Tara in Tibetan Buddhism: Meaning, Practice, and Origin | Awakened Mind",
            "meta": "Definition of Tara in Mahayana and Tibetan Buddhism. The embodiment of swift compassionate action and fearless courage.",
            "def": "Tara (Sanskrit: तारा, Tārā; Tibetan: སྒྲོལ་མ, Drolma, 'She Who Liberates') is one of the most revered figures in Mahayana and Vajrayana Buddhism, personifying swift, fearless compassion in action.",
        },
        "pt": {
            "slug": "tara",
            "term": "Tara (Nobre Tara)",
            "title": "O que é Tara no Budismo Tibetano: Significado, Prática e Origem | Mente Desperta",
            "meta": "Definição de Tara no budismo Mahayana e tibetano. A personificação da compaixão em ação e da coragem destemida.",
            "def": "Tara (em sânscrito: तारा, Tārā; em tibetano: སྒྲོལ་མ, Drolma, 'Aquela que Liberta') é uma das figuras mais veneradas do budismo Mahayana e Vajrayana. Representa a atividade rápida e compassiva dos seres despertos diante do sofrimento e do medo.",
        }
    },
    {
        "key": "avalokiteshvara",
        "book_key": "avalo",
        "en": {
            "slug": "avalokiteshvara",
            "term": "Avalokiteshvara",
            "title": "Avalokiteshvara: The Bodhisattva of Boundless Compassion | Awakened Mind",
            "meta": "Who is Avalokiteshvara (Chenrezig) in Buddhism. Meaning, teachings on unattached compassion, and the six-syllable mantra.",
            "def": "Avalokiteshvara (Sanskrit: अवलोकितेश्वर, 'Lord Who Looks Down with Compassion'; Tibetan: སྤྱན་རས་གཟིགས, Chenrezig) is the Bodhisattva embodying the universal compassion of all Buddhas.",
        },
        "pt": {
            "slug": "avalokiteshvara",
            "term": "Avalokiteshvara",
            "title": "Avalokiteshvara: O Bodhisattva da Infinita Compaixão | Mente Desperta",
            "meta": "Quem é Avalokiteshvara (Chenrezig) no budismo. Significado, ensinamentos de compaixão desapegada e o mantra de seis sílabas.",
            "def": "Avalokiteshvara (sânscrito: अवलोकितेश्वर, 'Aquele que ouve os lamentos do mundo'; tibetano: སྤྱན་རས་གཟིགས, Chenrezig) é o Bodhisattva que personifica a compaixão perfeita de todos os Budas.",
        }
    },
    {
        "key": "manjushri",
        "book_key": "manjushri",
        "en": {
            "slug": "manjushri",
            "term": "Manjushri",
            "title": "Manjushri: The Bodhisattva of Transcendent Wisdom | Awakened Mind",
            "meta": "Definition of Manjushri, the Bodhisattva of wisdom wielding the flaming sword of discernment and the Prajnaparamita text.",
            "def": "Manjushri (Sanskrit: मञ्जुश्री, Mañjuśrī, 'Gentle Glory'; Tibetan: འཇམ་དཔལ་དབྱངས, Jampelyang) personifies transcendent wisdom (prajna) and the razor-sharp discernment that cuts delusion.",
        },
        "pt": {
            "slug": "manjushri",
            "term": "Manjushri",
            "title": "Manjushri: O Bodhisattva da Sabedoria Transcendental | Mente Desperta",
            "meta": "Definição de Manjushri, o Bodhisattva da sabedoria que empunha a espada flamejante do discernimento e o livro da prajnaparamita.",
            "def": "Manjushri (sânscrito: मञ्जुश्री, Mañjuśrī, 'Glória Suave'; tibetano: འཇམ་དཔལ་དབྱངས, Jampelyang) personifica a sabedoria transcendental (prajna) e o discernimento que corta a ignorância.",
        }
    },
    {
        "key": "vajrasattva",
        "book_key": "vajrasattva",
        "en": {
            "slug": "vajrasattva",
            "term": "Vajrasattva",
            "title": "Vajrasattva: The Principle of Purification in Tibetan Buddhism | Awakened Mind",
            "meta": "Meaning of Vajrasattva (Dorje Sempa), the Four Opponent Powers, and the purification of karmic imprints and guilt.",
            "def": "Vajrasattva (Sanskrit: वज्रसत्त्व; Tibetan: རྡོ་རྗེ་སེམས་དཔའ, Dorje Sempa, 'Vajra Being') represents primordial purity and serves as the core practice of karmic purification in Tibetan Buddhism.",
        },
        "pt": {
            "slug": "vajrasattva",
            "term": "Vajrasattva",
            "title": "Vajrasattva: O Princípio da Purificação no Budismo Tibetano | Mente Desperta",
            "meta": "Significado de Vajrasattva (Dorje Sempa), a prática dos Quatro Poderes Oponentes e a purificação de erros e culpas.",
            "def": "Vajrasattva (sânscrito: वज्रसत्त्व; tibetano: རྡོ་རྗེ་སེམས་དཔའ, Dorje Sempa, 'Ser Adamantino') é a representação primordial da mente imaculada e a principal prática de purificação cármica no budismo tibetano.",
        }
    },
    {
        "key": "vajrapani",
        "book_key": "vajrapani",
        "en": {
            "slug": "vajrapani",
            "term": "Vajrapani",
            "title": "Vajrapani: The Holder of the Thunderbolt and Spiritual Power | Awakened Mind",
            "meta": "Who is Vajrapani (Channa Dorje), the Bodhisattva representing the fierce power of all Buddhas to overcome fear and stagnation.",
            "def": "Vajrapani (Sanskrit: वज्रपाणि, 'Thunderbolt Holder'; Tibetan: ཕྱག་ན་རྡོ་རྗེ, Chana Dorje) embodies the concentrated power and resolute energy of awakened awareness overcoming inner obstacles.",
        },
        "pt": {
            "slug": "vajrapani",
            "term": "Vajrapani",
            "title": "Vajrapani: O Portador do Raio e o Poder Espiritual | Mente Desperta",
            "meta": "Quem é Vajrapani (Channa Dorje), o Bodhisattva que personifica o poder de todos os Budas para subjugar o medo e a letargia.",
            "def": "Vajrapani (sânscrito: वज्रपाणि, 'Aquele que segura o raio'; tibetano: ཕྱག་ན་རྡོ་རྗེ, Chana Dorje) personifica o poder irrestrito da mente desperta e a energia resoluta necessária para superar obstáculos interiores.",
        }
    },
    {
        "key": "kshitigarbha",
        "book_key": None,
        "en": {
            "slug": "kshitigarbha",
            "term": "Kshitigarbha",
            "title": "Kshitigarbha: Guardian of the Realms of Suffering | Awakened Mind",
            "meta": "Meaning of Kshitigarbha (Earth Treasury), the Bodhisattva who vowed never to enter Nirvana until all suffering beings are guided to peace.",
            "def": "Kshitigarbha (Sanskrit: क्षितिगर्भ, 'Earth Matrix' or 'Earth Treasury'; Tibetan: ས་ཡི་སྙིང་པོ, Sa'i Nyingpo) is revered for his vow to accompany and liberate beings in states of grief and profound darkness.",
        },
        "pt": {
            "slug": "kshitigarbha",
            "term": "Kshitigarbha",
            "title": "Kshitigarbha: O Guardião dos Reinos de Sofrimento | Mente Desperta",
            "meta": "Significado de Kshitigarbha (Tesouro da Terra), o Bodhisattva que fez o voto de não atingir a iluminação enquanto houver seres em sofrimento.",
            "def": "Kshitigarbha (sânscrito: क्षितिगर्भ, 'Matriz da Terra' ou 'Tesouro da Terra'; tibetano: ས་ཡི་སྙིང་པོ, Sa'i Nyingpo) é conhecido por seu voto imenso de resgatar os seres nos momentos de maior escuridão e luto.",
        }
    },
    {
        "key": "bodhisattva",
        "book_key": None,
        "en": {
            "slug": "bodhisattva",
            "term": "Bodhisattva",
            "title": "What is a Bodhisattva in Mahayana Buddhism: Definition and Vow | Awakened Mind",
            "meta": "Understand the Bodhisattva ideal: an awakened practitioner dedicated to reaching full enlightenment for the liberation of all beings.",
            "def": "A Bodhisattva (Sanskrit: बोधिसत्त्व; Tibetan: བྱང་ཆུབ་སེམས་དཔའ, Jangchub Sempa, 'Hero of Awakening') is an individual cultivating Bodhicitta—the altruistic motivation to attain enlightenment for the liberation of all beings.",
        },
        "pt": {
            "slug": "bodhisattva",
            "term": "Bodhisattva",
            "title": "O que é um Bodhisattva no Budismo Mahayana: Definição e Voto | Mente Desperta",
            "meta": "Entenda o conceito de Bodhisattva: um praticante dedicado a atingir o despertar pleno pelo benefício e libertação de todos os seres.",
            "def": "Bodhisattva (sânscrito: बोधिसत्त्व; tibetano: བྱང་ཆུབ་སེམས་དཔའ, Jangchub Sempa, 'Herói do Despertar') é o ser que cultiva a Bodhicitta — a aspiração sincera de alcançar a iluminação para libertar todos os seres sencientes do sofrimento.",
        }
    },
    {
        "key": "karma",
        "book_key": "karma",
        "en": {
            "slug": "karma",
            "term": "Karma",
            "title": "The Concept of Karma in Buddhism: Causality and Intentional Action | Awakened Mind",
            "meta": "What Karma means in foundational Buddhist philosophy: dynamic causality and how intentional deeds shape present and future reality.",
            "def": "Karma (Sanskrit: कर्म, 'Action'; Pali: Kamma; Tibetan: ལས, Le) denotes the principle of intentional cause and effect, whereby every volitional act plants psychological and experiential seeds.",
        },
        "pt": {
            "slug": "karma",
            "term": "Karma",
            "title": "O Conceito de Karma no Budismo: Causalidade e Intenção | Mente Desperta",
            "meta": "O que significa Karma no budismo original. A lei de causalidade dinâmica e como nossas intenções moldam a experiência presente.",
            "def": "Karma (sânscrito: कर्म, 'Ação'; pali: Kamma; tibetano: ལས, Le) refere-se à lei universal de causa e efeito segundo a qual toda ação intencional (física, verbal ou mental) gera sementes e consequências correspondentes.",
        }
    },
    {
        "key": "mantra-om-mani-padme-hum",
        "book_key": "avalo",
        "en": {
            "slug": "om-mani-padme-hum-mantra",
            "term": "Om Mani Padme Hum",
            "title": "Meaning of the Om Mani Padme Hum Mantra | Awakened Mind",
            "meta": "Origin, translation, and significance of the six sacred syllables of Avalokiteshvara's mantra in Tibetan Buddhism.",
            "def": "Om Mani Padme Hum (Sanskrit: ॐ मणि पद्मे हूँ; Tibetan: ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ) is the six-syllable mantra of Avalokiteshvara, symbolizing the inseparable union of transcendent wisdom and unconditional compassion.",
        },
        "pt": {
            "slug": "mantra-om-mani-padme-hum",
            "term": "Om Mani Padme Hum",
            "title": "O Significado do Mantra Om Mani Padme Hum | Mente Desperta",
            "meta": "Origem, tradução e significado das seis sílabas sagradas do mantra de Avalokiteshvara no budismo tibetano.",
            "def": "Om Mani Padme Hum (sânscrito: ॐ मणि पद्मे हूँ; tibetano: ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ) é o mantra de seis sílabas associado a Avalokiteshvara. Traduz-se poeticamente como 'A Joia no Lótus' e simboliza a união inseparável de sabedoria e compaixão.",
        }
    },
    {
        "key": "om-tare-tuttare-ture-soha",
        "book_key": "tara",
        "en": {
            "slug": "om-tare-tuttare-ture-soha-mantra",
            "term": "Om Tare Tuttare Ture Soha",
            "title": "Green Tara Mantra: Om Tare Tuttare Ture Soha | Awakened Mind",
            "meta": "Meaning and practical contemplation of the Green Tara mantra to overcome fear, anxiety, and the eight inner perils.",
            "def": "Om Tare Tuttare Ture Soha (Sanskrit: ॐ तारे तुत्तारे तुरे स्वाहा; Tibetan: ཨོཾ་ཏཱ་རེ་ཏུཏྟཱ་རེ་ཏུ་རེ་སྭཱ་ཧཱ) is the core mantra of Noble Tara, chanted to pacify fear, anxiety, and internal hindrances.",
        },
        "pt": {
            "slug": "om-tare-tuttare-ture-soha",
            "term": "Om Tare Tuttare Ture Soha",
            "title": "O Mantra de Tara Verde: Om Tare Tuttare Ture Soha | Mente Desperta",
            "meta": "Significado e aplicação prática do mantra de Tara Verde para superar o medo, a ansiedade e os oito perigos interiores.",
            "def": "Om Tare Tuttare Ture Soha (sânscrito: ॐ तारे तुत्तारे तुरे स्वाहा; tibetano: ཨོཾ་ཏཱ་རེ་ཏུཏྟཱ་རེ་ཏུ་རེ་སྭཱ་ཧཱ) é o mantra fundamental de Nobre Tara, invocado para dissolver as oito formas de medo interior e proteger a mente.",
        }
    },
    {
        "key": "mantra-das-cem-silabas",
        "book_key": "vajrasattva",
        "en": {
            "slug": "hundred-syllable-mantra",
            "term": "Hundred-Syllable Mantra",
            "title": "Vajrasattva's 100-Syllable Mantra: Meaning and Practice | Awakened Mind",
            "meta": "Structure, translation, and meditative application of Vajrasattva's hundred-syllable purification mantra.",
            "def": "The Hundred-Syllable Mantra of Vajrasattva is one of the most profound purification practices in Tibetan Buddhism, recited to cleanse karmic imprints and restore clarity of mind.",
        },
        "pt": {
            "slug": "mantra-das-cem-silabas",
            "term": "Mantra das Cem Sílabas",
            "title": "O Mantra das 100 Sílabas de Vajrasattva: Significado e Prática | Mente Desperta",
            "meta": "Estrutura, tradução e instruções contemplativas do poderoso mantra de purificação de Vajrasattva.",
            "def": "O Mantra das Cem Sílabas de Vajrasattva é uma das mais profundas fórmulas meditativas do budismo tântrico tibetano, praticado para restaurar compromissos espirituais (samayas) e purificar impressões cármicas dolorosas.",
        }
    }
]


def glossary_url_of(term, lang):
    slug = term[lang]["slug"]
    return f"/glossary/{slug}/" if lang == "en" else f"/pt/glossario/{slug}/"


def glossary_page(term, lang):
    t = T[lang]
    d = term[lang]
    canonical = glossary_url_of(term, lang)
    alt = {"en": glossary_url_of(term, "en"), "pt": glossary_url_of(term, "pt")}
    
    book = next((b for b in BOOKS if b["key"] == term.get("book_key")), None) if term.get("book_key") else None
    trail = [(t["breadcrumb_home"], HOME[lang]), (t["glossary"], None), (d["term"], None)]
    
    graph = [
        PERSON,
        {
            "@type": "DefinedTerm",
            "@id": f"{DOMAIN}{canonical}#term",
            "name": d["term"],
            "description": d["def"],
            "inLanguage": t["lang"],
            "url": f"{DOMAIN}{canonical}",
        },
        {
            "@type": "Article",
            "@id": f"{DOMAIN}{canonical}#article",
            "headline": d["title"],
            "description": d["meta"],
            "inLanguage": t["lang"],
            "url": f"{DOMAIN}{canonical}",
            "author": {"@id": f"{DOMAIN}/#hugo-salles"},
            "publisher": {"@type": "Organization", "name": SITE["brand_en"] if lang=="en" else SITE["brand_pt"], "url": DOMAIN},
        },
        breadcrumb_ld(lang, trail),
    ]
    
    book_showcase_html = ""
    if book:
        bd = book[lang]
        book_dims = cover_dims(book, lang)
        book_url = url_of(book, lang)
        book_showcase_html = f"""
        <div style="margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.03); border: 1px solid var(--gold); border-radius: 12px; display: flex; flex-wrap: wrap; gap: 2rem; align-items: center;">
          <div style="flex: 0 0 140px;">
            <a href="{book_url}">
              <picture>
                <source srcset="{cover(book, lang)}.webp" type="image/webp">
                <img src="{cover(book, lang)}.jpg" width="{book_dims[0]}" height="{book_dims[1]}" alt="{e(bd['full_title'])}" style="border-radius: 6px; width: 100%; height: auto;" loading="lazy">
              </picture>
            </a>
          </div>
          <div style="flex: 1 1 300px;">
            <p style="font-size: 0.85rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.25rem;">{'Recommended book to go deeper' if lang=='en' else 'Livro recomendado para aprofundar'}</p>
            <h3 style="font-family: 'Oswald', sans-serif; font-size: 1.4rem; margin: 0 0 0.5rem 0;"><a href="{book_url}" class="bp-inline-link">{e(bd['name'])}</a></h3>
            <p style="font-size: 0.95rem; margin-bottom: 1rem;">{e(bd['subtitle'])}</p>
            {cta_block(book, lang)}
          </div>
        </div>
        """

    series_cards = []
    for b in [bk for bk in BOOKS if bk["series"]]:
        d_dim = cover_dims(b, lang)
        series_cards.append(f"""        <a class="bp-rel-card" href="{url_of(b, lang)}" style="--book-accent: {b['accent']}">
          <picture>
            <source srcset="{cover(b, lang)}.webp" type="image/webp">
            <img src="{cover(b, lang)}.jpg" width="{d_dim[0]}" height="{d_dim[1]}" alt="{e(b[lang]['full_title'])}" loading="lazy" decoding="async">
          </picture>
          <span class="bp-rel-name">{e(b[lang]['name'])}</span>
          <span class="bp-rel-theme">{e(b[lang]['theme'])}</span>
        </a>""")

    parts = [head(lang, title=d["title"], desc=d["meta"], canonical=canonical, alt=alt,
                  og_image="/assets/social-share-en.jpg" if lang=="en" else "/assets/social-share.jpg",
                  og_type="article", jsonld=ld({"@context": "https://schema.org", "@graph": graph}))]
    parts.append(nav(lang, alt, current="books"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    parts.append(f"""
  <article class="bp">
    <header class="bp-hub-header">
      <div class="container bp-narrow">
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
        <p class="bp-eyebrow">{'Glossary · Buddhist Philosophy & Practice' if lang=='en' else 'Glossário · Filosofia e Prática Budista'}</p>
        <h1 class="bp-h1">{e(d['term'])}</h1>
        <p class="bp-lead">{e(d['def'])}</p>
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
      </div>
    </header>

    <section class="bp-section">
      <div class="container bp-narrow" style="line-height: 1.8; font-size: 1.1rem;">
        <h2 class="bp-h2">{'Origins and Canonical Sources' if lang=='en' else 'Origem e Fontes Canônicas'}</h2>
        <p>{'This term is rooted in canonical sutras and traditional commentaries of Mahayana and Tibetan Buddhism, understood as a rigorous contemplative technology for mind training.' if lang=='en' else 'Este termo tem raízes nos sutras canônicos e comentários da tradição Mahayana e tibetana, sendo compreendido como um método rigoroso de investigação e transformação da consciência.'}</p>
        
        {book_showcase_html}
      </div>
    </section>

    <section class="bp-section bp-related">
      <div class="container">
        <h2 class="bp-h2">{'Explore the series books' if lang=='en' else 'Conheça os livros da série'}</h2>
        <div class="bp-rel-grid">
{chr(10).join(series_cards)}
        </div>
      </div>
    </section>
  </article>
  </main>
""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- hub page
def hub_page(lang):
    t = T[lang]
    alt = {"en": HUB["en"], "pt": HUB["pt"]}
    trail = [(t["breadcrumb_home"], HOME[lang]), (t["books"], None)]

    def card(b):
        d = cover_dims(b, lang)
        bd = b[lang]
        return f"""        <article class="bp-hub-card" style="--book-accent: {b['accent']}">
          <a class="bp-hub-cover" href="{url_of(b, lang)}" tabindex="-1" aria-hidden="true">
            <div class="book-cover-wrapper">
              <picture>
                <source srcset="{cover(b, lang)}.webp" type="image/webp">
                <img class="book-cover active" src="{cover(b, lang)}.jpg" width="{d[0]}" height="{d[1]}" alt="" loading="lazy" decoding="async">
              </picture>
              <div class="cover-light-effect" aria-hidden="true"></div>
            </div>
          </a>
          <div class="bp-hub-info">
            <p class="bp-hub-theme">{e(bd['theme'])}</p>
            <h3 class="bp-hub-title"><a href="{url_of(b, lang)}">{e(bd['name'])}</a></h3>
            <p class="bp-hub-sub">{e(bd['subtitle'])}</p>
            <p><a class="bp-inline-link" href="{url_of(b, lang)}">{t['read_more']} <span aria-hidden="true">&rarr;</span></a></p>
          </div>
        </article>"""

    series = [b for b in BOOKS if b["series"]]
    others = [b for b in BOOKS if not b["series"]]

    themes = "\n".join(
        f'          <li><a href="{url_of(b, lang)}"><strong>{e(b[lang]["theme"])}</strong> — {e(b[lang]["name"])}</a></li>'
        for b in BOOKS)

    graph = [
        PERSON,
        {
            "@type": "CollectionPage",
            "@id": f"{DOMAIN}{HUB[lang]}#page",
            "name": t["hub_h1"],
            "description": t["hub_meta"],
            "url": f"{DOMAIN}{HUB[lang]}",
            "inLanguage": t["lang"],
        },
        {
            "@type": "BookSeries",
            "@id": f"{DOMAIN}{HUB[lang]}#series",
            "name": t["series_name"],
            "url": f"{DOMAIN}{HUB[lang]}",
            "author": {"@id": f"{DOMAIN}/#hugo-salles"},
            "inLanguage": t["lang"],
            "numberOfItems": len(series),
            "hasPart": [{"@type": "Book", "@id": f"{DOMAIN}{url_of(b, lang)}#book",
                         "name": b[lang]["full_title"], "url": f"{DOMAIN}{url_of(b, lang)}",
                         "position": b["order"]} for b in series],
        },
        {
            "@type": "ItemList",
            "@id": f"{DOMAIN}{HUB[lang]}#list",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}{url_of(b, lang)}",
                 "name": b[lang]["full_title"]}
                for i, b in enumerate(BOOKS)
            ],
        },
        breadcrumb_ld(lang, trail),
    ]

    parts = [head(lang, title=t["hub_title"], desc=t["hub_meta"],
                  keywords=", ".join(b[lang]["name"] for b in BOOKS) + ", Hugo Salles",
                  canonical=HUB[lang], alt=alt,
                  og_image="/assets/social-share-en.jpg" if lang=="en" else "/assets/social-share.jpg",
                  jsonld=ld({"@context": "https://schema.org", "@graph": graph}))]
    parts.append(nav(lang, alt, current="books"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    parts.append(f"""
  <header class="bp-hub-header">
    <div class="container bp-narrow">
      <hr class="solid-separator" aria-hidden="true">
      <h1 class="bp-h1">{t['hub_h1']}</h1>
      <p class="bp-lead">{t['hub_lead']}</p>
      <hr class="solid-separator" aria-hidden="true">
    </div>
  </header>

  <section class="bp-section">
    <div class="container">
      <h2 class="bp-h2">{t['hub_series_h2']}</h2>
      <div class="bp-hub-grid">
{chr(10).join(card(b) for b in series)}
      </div>
    </div>
  </section>

  <section class="bp-section bp-section--alt">
    <div class="container">
      <h2 class="bp-h2">{t['hub_other_h2']}</h2>
      <div class="bp-hub-grid">
{chr(10).join(card(b) for b in others)}
      </div>
    </div>
  </section>

  <section class="bp-section">
    <div class="container bp-narrow">
      <h2 class="bp-h2">{t['hub_theme_h2']}</h2>
      <ul class="bp-list bp-themes">
{themes}
      </ul>
    </div>
  </section>
  </main>

""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- author page
def author_page(lang):
    t = T[lang]
    alt = {"en": AUTHOR_URL["en"], "pt": AUTHOR_URL["pt"]}
    trail = [(t["breadcrumb_home"], HOME[lang]), (t["author"], None)]
    
    if lang == "en":
        title = "Hugo Salles — Author | Awakened Mind"
        desc = "Hugo Salles is a writer, lawyer and executive, author of The Technologies of the Awakened Mind and translator of Buddhist sutras into Portuguese."
        bios = [
            "Hugo Salles is a writer, lawyer, and executive. For over twenty years, he has led teams and projects — an experience that bridged his study of Mahayana and Tibetan Buddhism with concrete everyday issues such as fear, conflict, guilt, attachment, and decision-making.",
            "As part of this independent study path, he has translated selected Buddhist sutras into Portuguese, working with canonical texts, recognized translations, and traditional commentaries.",
            "In the series <em>The Technologies of the Awakened Mind</em>, he investigates how teachings, symbols, and practices related to figures like Tara, Manjushri, Avalokiteshvara, Vajrasattva, and Vajrapani can contribute to cultivating courage, clarity, compassion, and discernment.",
            "His books follow a simple principle: teachings should not be accepted solely on the authority of those presenting them, but should be put into practice, observed, and evaluated through one's own experience.",
        ]
        h1 = "Hugo Salles"
        btn_text = "All books"
    else:
        title = "Hugo Salles — Autor | Mente Desperta"
        desc = "Escritor, advogado e executivo. Autor da série As Tecnologias da Mente Desperta e tradutor de sutras budistas para o português."
        bios = [
            "Hugo Salles é escritor, advogado e executivo. Há mais de vinte anos atua na liderança de equipes e projetos — experiência que aproximou seu estudo do budismo Mahayana e tibetano das questões concretas do dia a dia, como medo, conflito, culpa, apego e tomada de decisão.",
            "Como parte desse percurso independente de estudo, traduziu para o português sutras budistas selecionados, trabalhando a partir de textos canônicos, traduções reconhecidas e comentários tradicionais.",
            "Na série <em>As Tecnologias da Mente Desperta</em>, investiga como ensinamentos, símbolos e práticas associados a figuras como Tara, Manjushri, Avalokiteshvara, Vajrasattva e Vajrapani podem contribuir para o cultivo de coragem, clareza, compaixão e discernimento.",
            "Seus livros partem de um princípio simples: ensinamentos não devem ser aceitos apenas pela autoridade de quem os apresenta, mas colocados em prática, observados e avaliados na própria experiência.",
        ]
        h1 = "Hugo Salles"
        btn_text = "Todos os livros"

    graph = [
        PERSON,
        {"@type": "ProfilePage", "@id": f"{DOMAIN}{AUTHOR_URL[lang]}#page",
         "name": title, "url": f"{DOMAIN}{AUTHOR_URL[lang]}",
         "inLanguage": t["lang"], "mainEntity": {"@id": f"{DOMAIN}/#hugo-salles"}},
        breadcrumb_ld(lang, trail),
    ]

    parts = [head(lang, title=title, desc=desc,
                  keywords="Hugo Salles, author, Tibetan Buddhism, Technologies of the Awakened Mind",
                  canonical=AUTHOR_URL[lang], alt=alt,
                  og_image="/assets/social-share-en.jpg" if lang=="en" else "/assets/social-share.jpg",
                  og_type="profile", jsonld=ld({"@context": "https://schema.org", "@graph": graph}))]
    parts.append(nav(lang, alt, current="author"))
    parts.append('\n  <main id="conteudo" class="bp-main">\n')
    parts.append(breadcrumb(lang, trail))
    body = "\n".join(f'          <p class="author-bio">{b}</p>' for b in bios)
    parts.append(f"""
  <section class="author-section" id="author">
    <div class="container">
      <div class="author-content">
        <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
        <h1 class="author-name">{h1}</h1>
        <div class="author-bio-content">
{body}
        </div>
      </div>
    </div>
  </section>

  <section class="bp-section bp-section--alt">
    <div class="container bp-narrow">
      <p><a class="bp-inline-link" href="{HUB[lang]}">{btn_text} <span aria-hidden="true">&rarr;</span></a></p>
    </div>
  </section>
  </main>

""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- review page
def review_page(lang):
    t = T[lang]
    alt = {"en": REVIEW_URL["en"], "pt": REVIEW_URL["pt"]}
    canonical = REVIEW_URL[lang]
    
    if lang == "en":
        title = "Review the Books — Awakened Mind | Hugo Salles"
        desc = "Leave your review for the books in The Technologies of the Awakened Mind series and works by Hugo Salles on Amazon."
        h1 = "Your review makes all the difference"
        lead = "Amazon reviews help other readers find these books and allow independent work to continue. Choose the book you've read:"
        back_text = "&larr; Back to homepage"
    else:
        title = "Avalie os Livros — Mente Desperta | Hugo Salles"
        desc = "Deixe sua avaliação para os livros da série As Tecnologias da Mente Desperta e obras de Hugo Salles na Amazon."
        h1 = "Sua avaliação faz a diferença"
        lead = "Avaliações na Amazon ajudam outros leitores a encontrar estes livros e permitem que o trabalho independente continue crescendo. Escolha o título que você leu:"
        back_text = "&larr; Voltar para a página inicial"

    cards = []
    for b in BOOKS:
        bd = b[lang]
        utm = f"?tag=mentedesperta-20&utm_source=awakenedmindbooks&utm_medium=site&utm_campaign={bd['slug']}"
        rev_us = f"https://www.amazon.com/review/create-review?asin={b['asin_us']}{utm}"
        rev_br = f"https://www.amazon.com.br/review/create-review?asin={b['asin_br']}{utm}"
        
        btn_us = f'<a href="{rev_us}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--primary">Review on Amazon US &rarr;</a>' if lang=="en" else f'<a href="{rev_us}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--secondary">Avaliar na Amazon US &rarr;</a>'
        btn_br = f'<a href="{rev_br}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--secondary">Review on Amazon BR &rarr;</a>' if lang=="en" else f'<a href="{rev_br}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn--primary">Avaliar na Amazon BR &rarr;</a>'
        
        cards.append(f"""        <article class="review-card">
          <div>
            <h3>{e(bd['name'])}</h3>
            <p>{e(bd['subtitle'])}</p>
          </div>
          <div class="review-actions">
            {btn_us if lang=='en' else btn_br}
            {btn_br if lang=='en' else btn_us}
          </div>
        </article>""")

    parts = [head(lang, title=title, desc=desc, canonical=canonical, alt=alt,
                  og_image="/assets/social-share-en.jpg" if lang=="en" else "/assets/social-share.jpg",
                  robots="noindex, follow")]
    parts.append(nav(lang, alt, current="review"))
    parts.append(f"""  <main id="conteudo" class="bp-main">
    <div class="container bp-narrow" style="padding-top: 3rem; text-align: center;">
      <hr class="gold-thread gold-thread--narrow" aria-hidden="true">
      <h1 class="bp-h1">{h1}</h1>
      <p class="bp-lead">{lead}</p>
      <hr class="gold-thread gold-thread--narrow" aria-hidden="true">

      <div class="review-grid">
{chr(10).join(cards)}
      </div>

      <p style="margin-top: 2rem;"><a href="{HOME[lang]}" class="bp-inline-link">{back_text}</a></p>
    </div>
  </main>
""")
    parts.append(footer(lang))
    parts.append('\n\n  <script src="/script.js"></script>\n</body>\n</html>\n')
    return "".join(parts)


# ---------------------------------------------------------------- sitemaps
def generate_sitemaps():
    """Gera sitemap índice apontando para sitemap-en.xml (primario) e sitemap-pt.xml."""
    def build_sitemap(url_list):
        urls = []
        for loc, alts in url_list:
            block = [f"  <url>", f"    <loc>{DOMAIN}{loc}</loc>",
                     f"    <lastmod>{TODAY}</lastmod>"]
            if alts:
                for hl, href in alts:
                    block.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{DOMAIN}{href}"/>')
            block.append("  </url>")
            urls.append("\n".join(block))
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + "\n".join(urls) + "\n</urlset>\n")

    home_alts = [("en", "/"), ("pt-BR", "/pt/"), ("x-default", "/")]
    hub_alts = [("en", "/books/"), ("pt-BR", "/pt/livros/"), ("x-default", "/books/")]
    author_alts = [("en", "/author/"), ("pt-BR", "/pt/autor/"), ("x-default", "/author/")]

    urls_en = [
        ("/", home_alts),
        ("/books/", hub_alts),
    ]
    urls_pt = [
        ("/pt/", home_alts),
        ("/pt/livros/", hub_alts),
    ]

    for b in BOOKS:
        alts = [("en", url_of(b, "en")), ("pt-BR", url_of(b, "pt")), ("x-default", url_of(b, "en"))]
        urls_en.append((url_of(b, "en"), alts))
        urls_pt.append((url_of(b, "pt"), alts))

    urls_en.append(("/author/", author_alts))
    urls_pt.append(("/pt/autor/", author_alts))

    sitemap_en = build_sitemap(urls_en)
    sitemap_pt = build_sitemap(urls_pt)
    
    index = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '  <sitemap>',
             f'    <loc>{DOMAIN}/sitemap-en.xml</loc>',
             '  </sitemap>',
             '  <sitemap>',
             f'    <loc>{DOMAIN}/sitemap-pt.xml</loc>',
             '  </sitemap>',
             '</sitemapindex>\n']
             
    return "\n".join(index), sitemap_en, sitemap_pt


# ---------------------------------------------------------------- main
def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  · {path}  ({len(content)//1024} KB)")


def main():
    print("Gerando páginas com Inglês como Raiz Primária (awakenedmindbooks.com)…")
    for b in BOOKS:
        for lang in ("en", "pt"):
            write(url_of(b, lang).strip("/") + "/index.html", book_page(b, lang))
            write(excerpt_url_of(b, lang).strip("/") + "/index.html", excerpt_page(b, lang))
            
    for topic in THEMES:
        for lang in ("en", "pt"):
            write(topic_url_of(topic, lang).strip("/") + "/index.html", topic_page(topic, lang))
            
    for term in GLOSSARY:
        for lang in ("en", "pt"):
            write(glossary_url_of(term, lang).strip("/") + "/index.html", glossary_page(term, lang))
            
    write("books/index.html", hub_page("en"))
    write("pt/livros/index.html", hub_page("pt"))
    
    write("author/index.html", author_page("en"))
    write("pt/autor/index.html", author_page("pt"))
    
    write("review/index.html", review_page("en"))
    write("pt/avalie/index.html", review_page("pt"))
    
    idx, sen, spt = generate_sitemaps()
    write("sitemap.xml", idx)
    write("sitemap-en.xml", sen)
    write("sitemap-pt.xml", spt)
    print("OK.")


if __name__ == "__main__":
    main()
