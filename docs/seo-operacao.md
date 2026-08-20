# SEO — Guia de Operação

## Google Search Console

### 1. Cadastrar propriedade de domínio

1. Acesse [Google Search Console](https://search.google.com/search-console/)
2. Clique em **"Adicionar propriedade"**
3. Escolha **"Propriedade de domínio"**
4. Digite: `mentedesperta.com`
5. Clique em **Continuar**
6. O Google vai pedir verificação por registro DNS TXT:
   - Copie o código fornecido (ex: `google-site-verification=XXXXXXX`)
   - No painel do seu provedor de DNS (Netlify DNS ou registrador de domínio), adicione um registro TXT na raiz (`@`) com o valor copiado
   - Aguarde até 72h para propagação (geralmente leva minutos)
7. Volte ao Search Console e clique em **Verificar**

> **Importante:** Propriedade de domínio cobre todas as variantes (www, sem www, http, https). É a opção correta.

### 2. Submeter o sitemap

1. No menu lateral, vá em **Sitemaps**
2. No campo "Adicionar novo sitemap", digite: `sitemap.xml`
3. Clique em **Enviar**
4. O Search Console vai descobrir automaticamente os sub-sitemaps (`sitemap-pt.xml` e `sitemap-en.xml`)
5. Verifique se o status aparece como **"Sucesso"** após o processamento

### 3. Verificações recorrentes

| Frequência | O que verificar |
|---|---|
| Semanal | **Cobertura** → Erros e Avisos |
| Semanal | **Core Web Vitals** → Mobile |
| Mensal | **Sitemaps** → Última leitura bem-sucedida |
| Mensal | **Links** → Links internos e externos |
| Após deploy | **Inspeção de URL** → Testar URLs alteradas |

### 4. Depuração rápida

- **URL não indexada:** Inspecionar URL → Solicitar indexação
- **Página mostrando idioma errado:** Verificar hreflang no relatório de Melhorias Internacionais
- **Queda de tráfego:** Verificar Ações Manuais e Problemas de Segurança

---

## Estrutura de Sitemaps

```
sitemap.xml (índice)
├── sitemap-pt.xml  (URLs em português)
└── sitemap-en.xml  (URLs em inglês)
```

Ambos os sub-sitemaps contêm anotações `xhtml:link` de hreflang cruzado.

O sitemap é regenerado automaticamente pelo `build.py`. A data `lastmod` é derivada da variável de ambiente `BUILD_DATE` ou da data atual.

---

## Checklist de deploy

Antes de cada deploy:

- [ ] Rodar `python build.py` na raiz do repositório
- [ ] Verificar que `sitemap.xml`, `sitemap-pt.xml` e `sitemap-en.xml` foram gerados
- [ ] Validar pelo menos 1 página no [Rich Results Test](https://search.google.com/test/rich-results)
- [ ] Verificar que nenhuma URL retorna 404 (testar `/livros/`, `/en/books/`, `/autor/`, `/en/author/`)
- [ ] Após deploy, submeter sitemap atualizado no Search Console
