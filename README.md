# Apex Team: Manual (código-fonte)

Gerador do manual em Python + HTML/CSS, renderizado para PDF via Playwright (Chromium headless).

## Estrutura

- `build.py`: monta o manual inteiro (todo o conteúdo, página por página) e escreve `manual.html`.
  É aqui que você edita textos, tabelas, ordem das seções etc.
- `helpers.py`: funções reutilizáveis (título, tabela, callout, imagem "solta", card, etc.) e a barra lateral de navegação.
- `svg_diagrams.py`: os diagramas técnicos desenhados em SVG (arquitetura do sistema, rede CAN, pipeline de visão, malha PID, desenho do pinhão/cremalheira e o gráfico PERT/CPM).
- `style.css`: todo o visual: cores, tipografia, layout das páginas, tabelas, callouts etc.
- `images/`: fotos dos componentes e da capa.
- `fonts/`: fontes (Inter, Barlow Semi Condensed, JetBrains Mono) em `.woff2`, usadas via `@font-face` no CSS.
- `render.py`: abre `manual.html` no Chromium headless e exporta `outputs/Apex_Team_Manual.pdf`
  (sempre sobrescrevendo o PDF anterior nessa pasta).
- `manual.html`: o manual em HTML puro (autocontido, abre em qualquer navegador). Tem um botão
  "Gerar PDF" fixo no canto: ele só chama `window.print()`; some automaticamente na hora de imprimir/exportar.

## Como editar

1. Abra `build.py` e procure a seção da página que quer mudar (está tudo comentado por página,
   ex: `# PAGE 8: PROPULSÃO`).
2. Textos usam as funções de `helpers.py`: `title(...)`, `h2(...)`, `lead(...)`, `table(...)`,
   `callout(...)`, `bare(...)` (imagem solta, sem moldura), `pending(...)` (placeholder tracejado
   para fotos que ainda faltam), `imgrow([...], cols=2)` (grade de imagens/placeholders lado a lado).
3. Para trocar/adicionar uma foto: coloque o arquivo em `images/` e aponte o `src` para ele.
4. Para mudar cores/fontes/espaçamento: edite `style.css` (as variáveis de cor estão no topo, em `:root`).
5. Os diagramas (SVG) ficam em `svg_diagrams.py`: cada função monta um diagrama e retorna o SVG como string.

## Como gerar o HTML e o PDF de novo

Requer Python 3 com Playwright já instalado (`pip install playwright && playwright install chromium`,
ou usar o Chromium do sistema).

```bash
python3 build.py     # gera manual.html a partir do conteúdo em build.py
python3 render.py    # abre manual.html no Chromium headless e exporta outputs/Apex_Team_Manual.pdf
```

`render.py` já usa `page.pdf(width="1123px", height="794px", print_background=True, margin=0)` :
mesmas dimensões usadas no `.page` do CSS (proporção A4 paisagem). Se mudar o tamanho da página no
CSS, ajuste as mesmas dimensões em `render.py`.

O PDF é sempre escrito em `outputs/Apex_Team_Manual.pdf` (nome fixo). Cada execução de
`render.py` apaga o arquivo anterior antes de gerar o novo, então o PDF gerado sempre substitui
o existente na pasta `outputs` — nunca cria versões numeradas ou duplicadas.

## Gerar o PDF sem rodar Python

Basta abrir `manual.html` em qualquer navegador e clicar no botão **"Gerar PDF"** (canto inferior
direito): ele abre a caixa de impressão do navegador; escolha "Salvar como PDF", sem margens e com
"gráficos de fundo" ativado para manter as cores. O botão não aparece no PDF gerado.
