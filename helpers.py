# -*- coding: utf-8 -*-
"""Reusable HTML/SVG building blocks for the Apex Team manual."""

NAV = [
    ("sumario", "Sumário"),
    ("partida", "Início"),
    ("processamento", "Processamento"),
    ("propulsao", "Propulsão"),
    ("direcao", "Direção"),
    ("sensores", "Sensores"),
    ("energia", "Energia"),
    ("comunicacao", "Comunicação"),
    ("software", "Software"),
    ("pecas", "Peças Mecânicas"),
    ("dados", "Dados Técnicos"),
]

DOC_CODE = "APEX-001-2026"

def sidebar(active_key):
    items = []
    for key, label in NAV:
        cls = "sb-item active" if key == active_key else "sb-item"
        items.append(f'<a class="{cls}" href="#sec-{key}"><span class="dot"></span>{label}</a>')
    return f'''<div class="sidebar">
      <div class="sb-logo"><img src="images/apex_logo.png"></div>
      <div class="sb-divider"></div>
      <div class="sb-nav">{"".join(items)}</div>
      <div class="sb-foot">
        <div class="code">{DOC_CODE}</div>
        <div class="team">Apex Team &middot; Engenharia Mecatrônica 4º Ano<br>FIAP &middot; Desafio Mercedes-Benz 2026</div>
      </div>
    </div>'''

_ANCHORED_SECTIONS = set()

def page(active_key, section_label, page_no, body_html, tight=False):
    main_cls = "main tight" if tight else "main"
    anchor_attr = ""
    if active_key not in _ANCHORED_SECTIONS:
        _ANCHORED_SECTIONS.add(active_key)
        anchor_attr = f' id="sec-{active_key}"'
    return f'''<div class="page"{anchor_attr}>
      {sidebar(active_key)}
      <div class="content">
        <div class="topbar">
          <div class="crumb"><b>Apex Team</b> &nbsp;&middot;&nbsp; Manual de Operação e Desenvolvimento</div>
          <div class="section-tag">{section_label}</div>
        </div>
        <div class="{main_cls}">{body_html}</div>
        <div class="footbar">
          <div>Apex Team &middot; Manual de Operação e Desenvolvimento</div>
          <div class="pageno">{page_no:02d} · {DOC_CODE}</div>
        </div>
      </div>
    </div>'''

def title(main, accent=None, sub=None):
    acc = f' <span class="accent">{accent}</span>' if accent else ""
    h = f'<h1 class="pt">{main}{acc}</h1><div class="pt-rule"></div>'
    if sub:
        h += f'<p class="lead">{sub}</p>'
    return h

def h2(text):
    return f'<h2 class="st">{text}</h2>'

def lead(text):
    return f'<p class="lead">{text}</p>'

ROW_MARKERS = {"__HL__": "hl", "__ALTO__": "alto", "__CRIT__": "crit"}

def table(headers, rows, compact=False, numeric_cols=None, col_widths=None):
    numeric_cols = numeric_cols or set()
    cls = "spec compact" if compact else "spec"
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = []
    for row in rows:
        marker = row[0] if row and row[0] in ROW_MARKERS else None
        cells = row[1:] if marker else row
        tds = []
        for i, c in enumerate(cells):
            tdcls = ' class="num"' if i in numeric_cols else ""
            tds.append(f"<td{tdcls}>{c}</td>")
        trcls = f' class="{ROW_MARKERS[marker]}"' if marker else ""
        trs.append(f"<tr{trcls}>{''.join(tds)}</tr>")
    colgroup = ""
    if col_widths:
        colgroup = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in col_widths) + "</colgroup>"
    return f'<table class="{cls}">{colgroup}<thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'

FLAG_LABEL = {
    "perigo": "⚠ Perigo",
    "atencao": "⚠ Atenção",
    "aviso": "✦ Aviso",
    "info": "ℹ Informação",
}

def callout(kind, text, label=None):
    lab = label or FLAG_LABEL.get(kind, kind.upper())
    return f'''<div class="callout {kind}"><div class="flag">{lab}</div><div class="body">{text}</div></div>'''

def icard(src, label, code=None, tall=False, tag=None, h=None):
    cls = "icard tall" if tall else "icard"
    tagd = f'<div class="tag">{tag}</div>' if tag else ""
    codeb = f"<b>{label}</b><span>{code}</span>" if code else f"<b>{label}</b>"
    style = f' style="height:{h}px"' if h else ""
    return f'''<div class="{cls}">
      <div class="ph"{style}>{tagd}<img src="{src}"></div>
      <div class="cap">{codeb}</div>
    </div>'''

def bare(src, h=170):
    """A free-floating PNG (transparent background) with no card, border or caption."""
    return f'<div class="bare-img" style="height:{h}px"><img src="{src}"></div>'

def pending(t1, t2, tall=False):
    cls = "icard tall" if tall else "icard"
    icon = '''<svg class="picto" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="5" width="20" height="15" rx="1.5" stroke="#8b959d" stroke-width="1.4"/>
      <circle cx="8" cy="11" r="2" stroke="#8b959d" stroke-width="1.4"/>
      <path d="M2 17l5.5-4.5a2 2 0 0 1 2.5 0L15 17M14 15l2-2a2 2 0 0 1 2.6 0L22 16" stroke="#8b959d" stroke-width="1.4" stroke-linecap="round"/>
    </svg>'''
    return f'''<div class="{cls}"><div class="pending">{icon}<div class="t1">{t1}</div><div class="t2">{t2}</div></div></div>'''

def imgrow(cards, cols=2):
    return f'<div class="imgrow c{cols}">{"".join(cards)}</div>'

def diagram(svg_inner, title_text, viewbox="0 0 1000 340", height=None):
    style = f' style="height:{height}px"' if height else ""
    return f'''<div class="diagram-panel"{style}>
      <div class="dtitle">{title_text}</div>
      <svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" style="width:100%; display:block;">{svg_inner}</svg>
    </div>'''

def idx_card(num, label, page_no, key=None):
    tag = "a" if key else "div"
    href = f' href="#sec-{key}"' if key else ""
    return f'''<{tag} class="idx-card"{href}><div class="n">SEÇÃO {num}</div><div class="t">{label}</div><div class="p">P. {page_no:02d}</div></{tag}>'''
