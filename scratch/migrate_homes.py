#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migra index.html (antiga PT) para pt/index.html e en/index.html para a raiz index.html.
Ajusta canonicals, hreflang, schemas e links internos.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Preparar PT (pt/index.html) a partir da index.html atual
pt_content = (ROOT / "index.html").read_text(encoding="utf-8")

# Substituir domain
pt_content = pt_content.replace("https://mentedesperta.com", "https://awakenedmindbooks.com")

# Substituir tags do head
pt_content = re.sub(
    r'<link href="https://awakenedmindbooks\.com/" rel="canonical"/><link href="https://awakenedmindbooks\.com/" hreflang="pt-BR" rel="alternate"/><link href="https://awakenedmindbooks\.com/en/" hreflang="en" rel="alternate"/><link href="https://awakenedmindbooks\.com/" hreflang="x-default" rel="alternate"/>',
    r'<link href="https://awakenedmindbooks.com/pt/" rel="canonical"/><link href="https://awakenedmindbooks.com/" hreflang="en" rel="alternate"/><link href="https://awakenedmindbooks.com/pt/" hreflang="pt-BR" rel="alternate"/><link href="https://awakenedmindbooks.com/" hreflang="x-default" rel="alternate"/>',
    pt_content
)
pt_content = pt_content.replace('<meta content="https://awakenedmindbooks.com/" property="og:url"/>', '<meta content="https://awakenedmindbooks.com/pt/" property="og:url"/>')

# Substituir URLs nos links internos PT
pt_content = pt_content.replace('href="/livros/"', 'href="/pt/livros/"')
pt_content = pt_content.replace('href="/autor/"', 'href="/pt/autor/"')
pt_content = pt_content.replace('href="/avalie/"', 'href="/pt/avalie/"')
pt_content = re.sub(r'href="/livros/([a-z-]+)/"', r'href="/pt/livros/\1/"', pt_content)

# Language switcher no nav PT
pt_content = re.sub(
    r'<div aria-label="Selecionar idioma" class="global-lang-toggle bp-lang" role="group">\s*<a aria-current="page" class="active" href="/" hreflang="pt-BR" lang="pt-BR">PT</a>\s*<a href="/en/" hreflang="en" lang="en">EN</a>\s*</div>',
    r'<div aria-label="Selecionar idioma" class="global-lang-toggle bp-lang" role="group">\n<a aria-current="page" class="active" href="/pt/" hreflang="pt-BR" lang="pt-BR">PT</a>\n<a href="/" hreflang="en" lang="en">EN</a>\n</div>',
    pt_content
)

# Salvar pt/index.html
(ROOT / "pt").mkdir(parents=True, exist_ok=True)
(ROOT / "pt/index.html").write_text(pt_content, encoding="utf-8")
print("pt/index.html criado com sucesso.")


# 2. Preparar EN (raiz index.html) a partir da en/index.html atual
en_content = (ROOT / "en/index.html").read_text(encoding="utf-8")

# Substituir domain
en_content = en_content.replace("https://mentedesperta.com", "https://awakenedmindbooks.com")

# Substituir tags do head
en_content = re.sub(
    r'<link href="https://awakenedmindbooks\.com/en/" rel="canonical"/><link href="https://awakenedmindbooks\.com/" hreflang="pt-BR" rel="alternate"/><link href="https://awakenedmindbooks\.com/en/" hreflang="en" rel="alternate"/><link href="https://awakenedmindbooks\.com/" hreflang="x-default" rel="alternate"/>',
    r'<link href="https://awakenedmindbooks.com/" rel="canonical"/><link href="https://awakenedmindbooks.com/" hreflang="en" rel="alternate"/><link href="https://awakenedmindbooks.com/pt/" hreflang="pt-BR" rel="alternate"/><link href="https://awakenedmindbooks.com/" hreflang="x-default" rel="alternate"/>',
    en_content
)
en_content = en_content.replace('<meta content="https://awakenedmindbooks.com/en/" property="og:url"/>', '<meta content="https://awakenedmindbooks.com/" property="og:url"/>')

# Substituir URLs nos links internos EN
en_content = en_content.replace('href="/en/books/"', 'href="/books/"')
en_content = en_content.replace('href="/en/author/"', 'href="/author/"')
en_content = en_content.replace('href="/en/review/"', 'href="/review/"')
en_content = re.sub(r'href="/en/books/([a-z-]+)/"', r'href="/books/\1/"', en_content)
en_content = en_content.replace('href="/en/#sobre"', 'href="/#about"')
en_content = en_content.replace('href="/en/#novidades"', 'href="/#news"')

# Language switcher no nav EN
en_content = re.sub(
    r'<div aria-label="Select language" class="global-lang-toggle bp-lang" role="group">\s*<a href="/" hreflang="pt-BR" lang="pt-BR">PT</a>\s*<a aria-current="page" class="active" href="/en/" hreflang="en" lang="en">EN</a>\s*</div>',
    r'<div aria-label="Select language" class="global-lang-toggle bp-lang" role="group">\n<a aria-current="page" class="active" href="/" hreflang="en" lang="en">EN</a>\n<a href="/pt/" hreflang="pt-BR" lang="pt-BR">PT</a>\n</div>',
    en_content
)

# Salvar raiz index.html
(ROOT / "index.html").write_text(en_content, encoding="utf-8")
print("index.html (EN na raiz) criado com sucesso.")
