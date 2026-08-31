# -*- coding: utf-8 -*-
"""Custom technical diagrams (inline SVG) for the Apex Team manual."""

# Light palette — tuned to sit on the manual's white/paper page background
# with a transparent panel (see .diagram-panel in style.css).
BLUE = "#256a8f"        # accent stroke / arrows / links
BLUE_DARK = "#123a56"   # solid accent fill (master / critical / highlighted boxes)
BLUE_LIGHT = "#bcd9e9"  # light accent text, used on top of BLUE_DARK fills
BLUE_FILL = "#123a56"   # alias of BLUE_DARK, kept for readability at call sites
INK = "#181e24"         # primary text
INK_DIM = "#5b6670"     # secondary text
INK_FAINT = "#8b959d"   # tertiary / dim text
NODE_FILL = "#f5f7f8"   # default box fill
BORDER = "#c7d0d6"      # default box border
BORDER_SOFT = "#dde2e6" # lighter / de-emphasized border (ghost boxes)
LINE = "#d7dce0"        # generic thin rule / grid line
TEXT_ON_DARK = "#f5f8fa" # text placed on top of BLUE_DARK fills

DEFS = f'''<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/>
  </marker>
  <marker id="arrowSilver" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK_FAINT}"/>
  </marker>
</defs>'''

def _box(x, y, w, h, label, sub=None, kind="node", fs=13, fs_sub=9.5):
    """kind: node | accent | ghost"""
    if kind == "accent":
        fill, stroke, tcol, scol = BLUE_DARK, BLUE, TEXT_ON_DARK, BLUE_LIGHT
    elif kind == "ghost":
        fill, stroke, tcol, scol = "#fbfbfa", BORDER_SOFT, INK_DIM, INK_FAINT
    else:
        fill, stroke, tcol, scol = NODE_FILL, BORDER, INK, INK_DIM
    cy = y + (h/2 - (6 if sub else 0))
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
    s += f'<text x="{x+w/2}" y="{cy+5}" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="700" font-size="{fs}" fill="{tcol}">{label}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{cy+20}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="{fs_sub}" fill="{scol}">{sub}</text>'
    return s

def _arrow(x1, y1, x2, y2, label=None, dashed=False, color=None, lx=None, ly=None):
    color = color or BLUE
    dash = ' stroke-dasharray="4,3"' if dashed else ""
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.6"{dash} marker-end="url(#arrow)"/>'
    if label:
        tx = lx if lx is not None else (x1+x2)/2
        ty = ly if ly is not None else (y1+y2)/2 - 8
        s += f'<text x="{tx}" y="{ty}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{INK_DIM}">{label}</text>'
    return s

def _vline(x, y1, y2, color=None, dashed=False):
    color = color or INK_FAINT
    dash = ' stroke-dasharray="3,3"' if dashed else ""
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="1.3"{dash}/>'


# ------------------------------------------------------------------ #
# 1. System architecture overview
# ------------------------------------------------------------------ #
def architecture():
    s = DEFS
    y = 46
    bw, bh = 148, 56
    x_cam, x_note, x_mega = 40, 250, 520
    s += _box(x_cam, y, 118, bh, "Câmera USB", "Fisheye 160°", kind="node")
    s += _box(x_note, y, bw, bh, "Notebook", "Python 3 · OpenCV", kind="node")
    s += _box(x_mega, y, bw, bh, "Arduino Mega", "ATmega2560 · Mestre", kind="accent")
    s += _arrow(x_cam+118, y+bh/2, x_note, y+bh/2, "USB")
    s += _arrow(x_note+bw, y+bh/2, x_mega, y+bh/2, "Serial 115.200 bps")

    # CAN bus fan-out to 4 ATmega328P modules
    bus_y = 168
    bus_x1, bus_x2 = 120, 760
    s += _arrow(x_mega+bw/2, y+bh, x_mega+bw/2, bus_y, "CAN 2.0B / J1939 · 250 kbps")
    s += f'<line x1="{bus_x1}" y1="{bus_y}" x2="{bus_x2}" y2="{bus_y}" stroke="{BLUE}" stroke-width="2"/>'
    s += f'<circle cx="{bus_x1}" cy="{bus_y}" r="3" fill="{BLUE}"/><circle cx="{bus_x2}" cy="{bus_y}" r="3" fill="{BLUE}"/>'

    modules = [
        ("PCB Motores\nLado Direito", 120),
        ("PCB Motores\nLado Esquerdo", 294),
        ("PCB Sinalização", 468),
        ("PCB BMS", 642),
    ]
    mw, mh = 118, 54
    my = 210
    for label, mx in modules:
        s += _vline(mx+mw/2, bus_y, my)
        s += f'<circle cx="{mx+mw/2}" cy="{bus_y}" r="2.6" fill="{BLUE}"/>'
        parts = label.split("\n")
        box = f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="6" fill="{NODE_FILL}" stroke="{BORDER}" stroke-width="1.3"/>'
        for i, p in enumerate(parts):
            box += f'<text x="{mx+mw/2}" y="{my+22+i*13}" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="700" font-size="11" fill="{INK}">{p}</text>'
        box += f'<text x="{mx+mw/2}" y="{my+mh-8}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{BLUE}">ATmega328P</text>'
        s += box

    # ATmega328P dedicado: camada de segurança independente, fora do barramento CAN
    ux = 860
    s += f'<path d="M {x_mega+bw} {y+bh/2} H {ux+mw/2} V {my}" fill="none" stroke="{INK_DIM}" stroke-width="1.6" stroke-dasharray="4,3" marker-end="url(#arrow)"/>'
    s += f'<text x="{(x_mega+bw+ux+mw/2)/2}" y="{y+bh/2-8}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{INK_DIM}">Serial1 · PARE/PROSSIGA</text>'
    box = f'<rect x="{ux}" y="{my}" width="{mw}" height="{mh}" rx="6" fill="{NODE_FILL}" stroke="{BORDER}" stroke-width="1.3"/>'
    box += f'<text x="{ux+mw/2}" y="{my+22}" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="700" font-size="11" fill="{INK}">ATmega328P</text>'
    box += f'<text x="{ux+mw/2}" y="{my+mh-8}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{BLUE}">3x HC-SR04</text>'
    s += box

    return s

def architecture_wrapper():
    from helpers import diagram
    return diagram(architecture(), "ARQUITETURA GERAL DO SISTEMA", viewbox="0 0 1000 300", height=230)


# ------------------------------------------------------------------ #
# 1b. ATmega328P dedicated modules grid
# ------------------------------------------------------------------ #
def atmega_modules():
    s = DEFS
    modules = [
        ("PCB Motores Lado Direito", "Tração + encoder (Hall) do lado direito – BTS7960", "CAN"),
        ("PCB Motores Lado Esquerdo", "Tração + encoder (Hall) do lado esquerdo – BTS7960", "CAN"),
        ("PCB Sinalização", "LEDs RGB e lanternas", "CAN"),
        ("PCB BMS", "Monitoramento da bateria", "CAN"),
    ]
    cols = 3
    cw, ch = 300, 92
    gx, gy = 26, 22
    for i, (label, func, link) in enumerate(modules):
        col = i % cols
        row = i // cols
        x = 20 + col*(cw+gx)
        y = 16 + row*(ch+gy)
        s += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="7" fill="{NODE_FILL}" stroke="{BORDER}" stroke-width="1.3"/>'
        s += f'<rect x="{x}" y="{y}" width="4" height="{ch}" rx="2" fill="{BLUE}"/>'
        s += f'<text x="{x+18}" y="{y+26}" font-family="Barlow Semi Condensed, sans-serif" font-weight="700" font-size="13.5" fill="{INK}">{label}</text>'
        s += f'<text x="{x+18}" y="{y+47}" font-family="Inter, sans-serif" font-size="9.5" fill="{INK_DIM}">{func}</text>'
        s += f'<text x="{x+18}" y="{y+ch-16}" font-family="JetBrains Mono, monospace" font-size="9" fill="{BLUE}">ATmega328P · {link}</text>'
    return s

def atmega_modules_wrapper():
    from helpers import diagram
    return diagram(atmega_modules(), "4 MÓDULOS ATMEGA328P DEDICADOS · MAPA DE FUNÇÕES", viewbox="0 0 966 240", height=220)


# ------------------------------------------------------------------ #
# 2. CAN J1939 network topology
# ------------------------------------------------------------------ #
def can_network():
    s = DEFS
    nodes = [
        ("Arduino Mega", "SA 0x01", "PGN 0xFEF1", True),
        ("PCB Motores\nLado Direito", "SA 0x10", "PGN 0xFF00", False),
        ("PCB Motores\nLado Esquerdo", "SA 0x11", "PGN 0xFF00", False),
        ("PCB Sinalização", "SA 0x20", "PGN 0xFF10", False),
        ("PCB BMS", "SA 0x50", "PGN 0xFF40", False),
    ]
    bw, bh = 128, 70
    top_y = 30
    bus_y = 150
    spacing = 225
    x_first = 110
    x_last = x_first + (len(nodes)-1)*spacing
    bus_x1, bus_x2 = x_first-50, x_last+50

    s += f'<line x1="{bus_x1}" y1="{bus_y}" x2="{bus_x2}" y2="{bus_y}" stroke="{BLUE}" stroke-width="2.4"/>'
    # termination resistors
    for tx in (bus_x1, bus_x2):
        s += f'<rect x="{tx-3}" y="{bus_y-16}" width="6" height="32" fill="none" stroke="{INK_DIM}" stroke-width="1.4"/>'
        s += f'<text x="{tx}" y="{bus_y-24}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8.5" fill="{INK_FAINT}">120Ω</text>'

    for i, (label, sa, pgn, master) in enumerate(nodes):
        cx = x_first + i*spacing
        x = cx - bw/2
        s += _vline(cx, bus_y, top_y+bh)
        parts = label.split("\n")
        box_fill = BLUE_DARK if master else NODE_FILL
        box_stroke = BLUE if master else BORDER
        label_col = TEXT_ON_DARK if master else INK
        sa_col = BLUE_LIGHT if master else BLUE
        pgn_col = "#9fc3d6" if master else INK_FAINT
        box = f'<rect x="{x}" y="{top_y}" width="{bw}" height="{bh}" rx="6" fill="{box_fill}" stroke="{box_stroke}" stroke-width="1.3"/>'
        for j, p in enumerate(parts):
            yy = top_y + (24 if len(parts)>1 else 26) + j*13
            box += f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="700" font-size="11.5" fill="{label_col}">{p}</text>'
        base_y = top_y + bh - 22
        box += f'<text x="{cx}" y="{base_y}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8.5" fill="{sa_col}">{sa}</text>'
        box += f'<text x="{cx}" y="{base_y+12}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8.5" fill="{pgn_col}">{pgn}</text>'
        s += box
        s += f'<circle cx="{cx}" cy="{bus_y}" r="3" fill="{BLUE}"/>'

    s += f'<text x="{(bus_x1+bus_x2)/2}" y="{bus_y+34}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9.5" fill="{INK_DIM}">barramento linear · 250 kbps · topologia CAN 2.0B / J1939 · transceptor MCP2515</text>'
    return s

def can_network_wrapper():
    from helpers import diagram
    return diagram(can_network(), "TOPOLOGIA DA REDE CAN J1939 · 5 NÓS", viewbox="0 0 1150 220", height=200)


# ------------------------------------------------------------------ #
# 3. Computer-vision pipeline
# ------------------------------------------------------------------ #
def vision_pipeline():
    s = DEFS
    steps = [
        ("1. Captura", "Frame bruto (BGR)"),
        ("2. Perspectiva", "Bird's Eye View"),
        ("3. Pré-proc.", "Cinza + blur"),
        ("4. Binarização", "Threshold adapt."),
        ("5. Faixas", "Histograma"),
        ("6. Erro (px)", "Centro vs. pista"),
    ]
    n = len(steps)
    bw, bh = 132, 74
    gap = 22
    total = n*bw + (n-1)*gap
    x0 = (1000-total)/2
    y = 60
    for i, (t, sub) in enumerate(steps):
        x = x0 + i*(bw+gap)
        kind = "accent" if i == n-1 else "node"
        s += _box(x, y, bw, bh, t, sub, kind=kind, fs=12.5, fs_sub=9)
        if i < n-1:
            s += _arrow(x+bw, y+bh/2, x+bw+gap, y+bh/2)
    s += f'<text x="500" y="{y+bh+40}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9.5" fill="{INK_DIM}">saída: ângulo de correção calculado por PID → enviado ao Arduino Mega via PySerial (115.200 bps)</text>'
    return s

def vision_pipeline_wrapper():
    from helpers import diagram
    return diagram(vision_pipeline(), "PIPELINE DE VISÃO COMPUTACIONAL · PYTHON / OPENCV", viewbox="0 0 1000 200", height=180)


# ------------------------------------------------------------------ #
# 4. PID control loop
# ------------------------------------------------------------------ #
def pid_loop():
    s = DEFS
    y = 70
    bh = 66
    # setpoint
    s += _box(40, y, 130, bh, "Setpoint", "Centro da pista = 0", kind="ghost", fs=12.5, fs_sub=9)
    # sum junction
    sx, sy = 225, y+bh/2
    s += f'<circle cx="{sx}" cy="{sy}" r="20" fill="{NODE_FILL}" stroke="{BLUE}" stroke-width="1.4"/>'
    s += f'<text x="{sx}" y="{sy+6}" text-anchor="middle" font-size="18" fill="{INK}" font-family="JetBrains Mono, monospace">Σ</text>'
    s += _arrow(40+130, sy, sx-20, sy)
    # PID controller
    pid_x, pid_w = 280, 140
    s += _box(pid_x, y, pid_w, bh, "Controlador PID", "P + I + D", kind="accent", fs=13, fs_sub=9.5)
    s += _arrow(sx+20, sy, pid_x, sy)
    # Plant
    plant_x, plant_w = 500, 140
    s += _box(plant_x, y, plant_w, bh, "Veículo (planta)", "Servo → direção", kind="node", fs=13, fs_sub=9.5)
    s += _arrow(pid_x+pid_w, sy, plant_x, sy, "Ângulo servo")
    # sensor feedback
    vision_x, vision_w = 730, 150
    s += _box(vision_x, y, vision_w, bh, "Visão computacional", "Câmera + OpenCV", kind="node", fs=12, fs_sub=9)
    s += _arrow(plant_x+plant_w, sy, vision_x, sy, "Posição real")
    # feedback line back down and to sum
    vcx = vision_x + vision_w/2
    fy = y+bh+55
    s += f'<line x1="{vcx}" y1="{y+bh}" x2="{vcx}" y2="{fy}" stroke="{INK_FAINT}" stroke-width="1.4"/>'
    s += f'<line x1="{vcx}" y1="{fy}" x2="{sx}" y2="{fy}" stroke="{INK_FAINT}" stroke-width="1.4"/>'
    s += f'<line x1="{sx}" y1="{fy}" x2="{sx}" y2="{sy+20}" stroke="{INK_FAINT}" stroke-width="1.4" marker-end="url(#arrowSilver)"/>'
    s += f'<text x="{(vcx+sx)/2}" y="{fy+16}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{INK_FAINT}">realimentação (erro em pixels)</text>'
    s += f'<text x="{sx}" y="{sy-30}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9" fill="{INK_DIM}">erro e(t)</text>'
    return s

def pid_loop_wrapper():
    from helpers import diagram
    return diagram(pid_loop(), "MALHA DE CONTROLE PID · DIREÇÃO AUTÔNOMA", viewbox="0 0 900 230", height=190)


# ------------------------------------------------------------------ #
# 5. Rack & pinion dimensioned drawing
# ------------------------------------------------------------------ #
def rack_pinion():
    s = DEFS
    # pinion (circle w/ teeth notches, simplified) left
    cx, cy, r = 150, 130, 62
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{NODE_FILL}" stroke="{BLUE}" stroke-width="1.6"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{INK_DIM}" stroke-width="1.3"/>'
    import math
    for i in range(15):
        a = i * (360/15) * (3.14159/180)
        x1 = cx + (r) * math.cos(a); y1 = cy + (r) * math.sin(a)
        x2 = cx + (r+7) * math.cos(a); y2 = cy + (r+7) * math.sin(a)
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BLUE}" stroke-width="2"/>'
    s += f'<text x="{cx}" y="{cy+r+34}" text-anchor="middle" font-family="Barlow Semi Condensed" font-weight="700" font-size="13" fill="{INK}">PINHÃO PIN-001</text>'
    s += f'<text x="{cx}" y="{cy+r+50}" text-anchor="middle" font-family="JetBrains Mono" font-size="9" fill="{INK_DIM}">M=3 · z=15 · ⌀51 mm · SAE 1045</text>'
    # dimension line diameter
    s += f'<line x1="{cx-r}" y1="{cy-r-14}" x2="{cx+r}" y2="{cy-r-14}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<line x1="{cx-r}" y1="{cy-r-20}" x2="{cx-r}" y2="{cy-r-8}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<line x1="{cx+r}" y1="{cy-r-20}" x2="{cx+r}" y2="{cy-r-8}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<text x="{cx}" y="{cy-r-20}" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="{INK_FAINT}">⌀ 51 mm</text>'

    # rack (horizontal bar with teeth) right, meshing
    rx, ry, rw, rh = 330, cy-16, 560, 32
    s += f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="{NODE_FILL}" stroke="{BLUE}" stroke-width="1.6"/>'
    nteeth = 26
    tw = rw/nteeth
    for i in range(nteeth):
        tx = rx + i*tw
        s += f'<line x1="{tx:.1f}" y1="{ry+rh}" x2="{tx:.1f}" y2="{ry+rh+9}" stroke="{BLUE}" stroke-width="1.6"/>'
    s += f'<text x="{rx+rw/2}" y="{ry+rh+34}" text-anchor="middle" font-family="Barlow Semi Condensed" font-weight="700" font-size="13" fill="{INK}">CREMALHEIRA CRM-001</text>'
    s += f'<text x="{rx+rw/2}" y="{ry+rh+50}" text-anchor="middle" font-family="JetBrains Mono" font-size="9" fill="{INK_DIM}">M=3 · 185 × 60 × 20 mm · SAE 1045</text>'
    # dimension length
    s += f'<line x1="{rx}" y1="{ry-14}" x2="{rx+rw}" y2="{ry-14}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<line x1="{rx}" y1="{ry-20}" x2="{rx}" y2="{ry-8}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<line x1="{rx+rw}" y1="{ry-20}" x2="{rx+rw}" y2="{ry-8}" stroke="{INK_FAINT}" stroke-width="1"/>'
    s += f'<text x="{rx+rw/2}" y="{ry-20}" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="{INK_FAINT}">185 mm</text>'
    # mesh contact marker
    s += f'<circle cx="{cx+r}" cy="{cy}" r="4" fill="none" stroke="{BLUE}" stroke-width="1.4"/>'
    return s

def rack_pinion_wrapper():
    from helpers import diagram
    return diagram(rack_pinion(), "DESENHO TÉCNICO · CONJUNTO PINHÃO E CREMALHEIRA", viewbox="0 0 940 230", height=210)


# ------------------------------------------------------------------ #
# 6. PERT / CPM gantt-style network (22 activities, 4 lanes)
# ------------------------------------------------------------------ #
ACTIVITIES = [
    ("A1", "Definição de requisitos e arquitetura", "Controle/Software", 5, []),
    ("A2", "Sistema de visão computacional", "Controle/Software", 10, ["A1"]),
    ("A3", "Algoritmo PID de direção", "Controle/Software", 5, ["A2"]),
    ("A4", "Comunicação Serial/CAN", "Controle/Software", 6, ["A1"]),
    ("A5", "Programação ATmega328P", "Controle/Software", 8, ["A4"]),
    ("A6", "Testes individuais (motores, servo)", "Controle/Software", 4, ["A5"]),
    ("A7", "Integração hardware + visão", "Controle/Software", 5, ["A3", "A6"]),
    ("A8", "Testes integrados + ajuste PID", "Controle/Software", 4, ["A7"]),
    ("B1", "Modelagem 3D – CRM-001", "Digital Twins", 3, ["A1"]),
    ("B2", "Modelagem 3D – PIN-001", "Digital Twins", 3, ["A1"]),
    ("B3", "Modelagem 3D – CRW-001", "Digital Twins", 3, ["A1"]),
    ("B4", "Modelagem 3D – ESV-001 e Eixo", "Digital Twins", 3, ["A1"]),
    ("B5", "Revisão e aprovação dos modelos", "Digital Twins", 2, ["B1", "B2", "B3", "B4"]),
    ("C1", "Usinagem – ESV-001", "Manufatura", 5, ["B4"]),
    ("C2", "Usinagem – CRW-001", "Manufatura", 6, ["B3"]),
    ("C3", "Usinagem – PIN-001", "Manufatura", 7, ["B2"]),
    ("C4", "Usinagem – CRM-001", "Manufatura", 4, ["B1"]),
    ("C5", "Usinagem – EIX-001", "Manufatura", 3, ["B4"]),
    ("C6", "Inspeção dimensional", "Manufatura", 3, ["C1", "C2", "C3", "C4", "C5"]),
    ("D1", "Montagem mecânica + integração elétrica", "Integração", 4, ["A7", "C6"]),
    ("D2", "Testes na pista – navegação autônoma", "Integração", 3, ["D1", "A8"]),
    ("D3", "Documentação e entrega", "Integração", 2, ["D2"]),
]
CRITICAL = {"A1", "A2", "A3", "A7", "D1", "D2", "D3"}
LANES = ["Controle/Software", "Digital Twins", "Manufatura", "Integração"]
LANE_COLOR = {"Controle/Software": "#3684ad", "Digital Twins": "#5a9e82", "Manufatura": "#b3873f", "Integração": "#b8524f"}

def _compute_schedule():
    dur = {a[0]: a[3] for a in ACTIVITIES}
    preds = {a[0]: a[4] for a in ACTIVITIES}
    es = {}
    def calc(code):
        if code in es:
            return es[code]
        if not preds[code]:
            es[code] = 0
        else:
            es[code] = max(calc(p) + dur[p] for p in preds[code])
        return es[code]
    for a in ACTIVITIES:
        calc(a[0])
    ef = {c: es[c] + dur[c] for c in es}
    return es, ef

def pert_gantt():
    es, ef = _compute_schedule()
    max_day = max(ef.values())
    s = DEFS
    left = 190
    top = 26
    row_h = 17.2
    chart_w = 780
    day_w = chart_w / max_day

    # lane bands
    lane_rows = {l: [a for a in ACTIVITIES if a[2] == l] for l in LANES}
    y = top
    lane_bounds = []
    for lane in LANES:
        rows = lane_rows[lane]
        band_h = row_h * len(rows)
        lane_bounds.append((lane, y, band_h))
        y += band_h + 6

    total_h = y

    # background per lane + label
    for lane, ly, lh in lane_bounds:
        col = LANE_COLOR[lane]
        s += f'<rect x="0" y="{ly}" width="{left+chart_w+10}" height="{lh}" fill="{col}" opacity="0.07"/>'
        s += f'<rect x="0" y="{ly}" width="4" height="{lh}" fill="{col}"/>'
        s += f'<text x="10" y="{ly+13}" font-family="Barlow Semi Condensed" font-weight="700" font-size="10.5" fill="{col}">{lane.upper()}</text>'

    # day grid
    step = 5
    dday = 0
    while dday <= max_day:
        gx = left + dday*day_w
        s += f'<line x1="{gx:.1f}" y1="{top-6}" x2="{gx:.1f}" y2="{total_h}" stroke="{LINE}" stroke-width="1"/>'
        s += f'<text x="{gx:.1f}" y="{top-10}" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="{INK_FAINT}">{dday}</text>'
        dday += step

    # rows
    y = top
    positions = {}
    for lane in LANES:
        for code, name, _, dur, preds in lane_rows[lane]:
            ry = y
            x1 = left + es[code]*day_w
            bw = dur*day_w
            crit = code in CRITICAL
            fill = BLUE_DARK if crit else NODE_FILL
            stroke = BLUE if crit else BORDER
            s += f'<rect x="{x1:.1f}" y="{ry+2.4:.1f}" width="{max(bw,4):.1f}" height="{row_h-4.8:.1f}" rx="2.4" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            tcol = TEXT_ON_DARK if crit else INK
            s += f'<text x="{left-8}" y="{ry+row_h-5.2:.1f}" text-anchor="end" font-family="JetBrains Mono" font-weight="600" font-size="8.6" fill="{tcol if crit else INK}">{code}</text>'
            s += f'<text x="6" y="{ry+row_h-5.2:.1f}" font-family="Inter" font-size="7.6" fill="{INK_FAINT}">{name[:34]}</text>' if False else ""
            label_txt = f"{dur}d"
            if bw > 22:
                s += f'<text x="{x1+bw/2:.1f}" y="{ry+row_h-5.2:.1f}" text-anchor="middle" font-family="JetBrains Mono" font-size="7.8" fill="{tcol}">{label_txt}</text>'
            positions[code] = (x1, x1+bw, ry+row_h/2)
            y += row_h
        y += 6

    # critical path connectors
    crit_order = ["A1", "A2", "A3", "A7", "D1", "D2", "D3"]
    for a, b in zip(crit_order, crit_order[1:]):
        if a in positions and b in positions:
            _, xa2, ya = positions[a]
            xb1, _, yb = positions[b]
            s += f'<path d="M{xa2:.1f},{ya:.1f} C{xa2+18:.1f},{ya:.1f} {xb1-18:.1f},{yb:.1f} {xb1:.1f},{yb:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="3,2" marker-end="url(#arrow)"/>'

    return s, total_h + 14

def pert_gantt_wrapper():
    from helpers import diagram
    svg, h = pert_gantt()
    vb_h = int(h)
    return diagram(svg, "REDE PERT/CPM · CRONOGRAMA POR ATIVIDADE (LINHA TRACEJADA = CAMINHO CRÍTICO)", viewbox=f"0 0 1000 {vb_h}", height=min(vb_h*0.72, 330))
