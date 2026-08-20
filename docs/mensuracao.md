# Mensuração — Estratégia de Tracking

## Objetivo

Medir a eficácia de cada página em gerar cliques para a Amazon, por livro, idioma e posição do botão.

---

## 1. UTM nos links da Amazon

Todos os links de saída para a Amazon seguem o padrão:

```
https://www.amazon.com.br/dp/{ASIN}?utm_source=mentedesperta&utm_medium=site&utm_campaign={slug-do-livro}
```

| Parâmetro | Valor | Propósito |
|---|---|---|
| `utm_source` | `mentedesperta` | Identifica o site como origem |
| `utm_medium` | `site` | Diferencia de e-mail, social, etc. |
| `utm_campaign` | slug do livro (ex: `tara`, `karma`) | Identifica qual livro gerou o clique |

> **Nota:** Esses parâmetros não interferem no rastreamento da Amazon Associates nem no KDP. Eles ficam visíveis no relatório do Google Analytics/Plausible e podem ser cruzados com o relatório do KDP por data.

---

## 2. Eventos de clique de saída

Implementados em `script.js`. Cada clique em link para a Amazon dispara um evento com:

| Campo | Exemplo | Descrição |
|---|---|---|
| `event` | `outbound_click` | Nome do evento |
| `book` | `tara` | Slug do livro |
| `lang` | `pt-BR` | Idioma da página |
| `position` | `hero`, `cta-final`, `sidebar` | Onde o botão está na página |
| `destination` | `amazon.com.br` | Domínio de destino |

---

## 3. Eventos de conversão de e-mail

O formulário de newsletter (`#newsletter-form`) dispara:

| Campo | Exemplo |
|---|---|
| `event` | `newsletter_signup` |
| `lang` | `pt-BR` |
| `source` | `homepage`, `book-page` |

---

## 4. Ferramenta de analytics

<!-- TODO: Definir Plausible ou GA4 -->

**Recomendação:** Plausible (leve, sem cookies, GDPR-compliant, self-hosted disponível).

Alternativa: GA4 com modo de consentimento configurado.

### Configuração (quando definido)

1. Adicionar o script de analytics no `<head>` de todas as páginas
2. No `build.py`, injetar via `head()` function
3. Nas homes manuais (`index.html`, `en/index.html`), adicionar manualmente
4. Configurar os eventos custom listados acima

---

## 5. Relatório KDP — Cruzamento

Para cruzar dados do site com vendas:

1. Exportar relatório do KDP por período
2. No analytics, filtrar eventos `outbound_click` pelo mesmo período
3. Comparar por `utm_campaign` (slug do livro) com o título no KDP
4. A correlação não será 1:1 (nem todo clique vira compra, e há compras orgânicas), mas a tendência por livro será visível
