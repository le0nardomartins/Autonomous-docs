# -*- coding: utf-8 -*-
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
from helpers import (page, title, h2, lead, table, callout, icard, bare, pending, imgrow,
                      diagram, idx_card, sidebar, NAV, DOC_CODE)
import svg_diagrams as sd

PAGES_HTML = []
PNO = {}  # will fill page numbers as we append

def add(html):
    PAGES_HTML.append(html)

# ================================================================== #
# PAGE 1 · COVER
# ================================================================== #
cover = f'''<div class="cover">
  <div class="left">
    <img class="logo" src="images/apex_logo.png">
    <div class="kicker">Manual de Operação e Desenvolvimento</div>
    <h1>Apex Team</h1>
    <div class="rule"></div>
    <div class="subtitle">Veículo autônomo em escala &middot; Desafio Mercedes-Benz 2026</div>
    <div class="team">
      <span class="role">Apex Team &middot; Engenharia Mecatrônica 4º Ano &middot; FIAP</span>
      Danilo Augusto &nbsp;RM 97810<br>
      Gabriel Rocha &nbsp;RM 552552<br>
      Gabriel Tadashi &nbsp;RM 551722<br>
      Guilherme Renovato &nbsp;RM 551712<br>
      Leonardo Martins &nbsp;RM 99537
    </div>
    <div class="meta">
      <b>FIAP</b> · Faculdade de Informática e Administração Paulista<br>
      Desafio Mercedes-Benz 2026 &middot; Campus Aclimação &middot; São Paulo – SP
    </div>
  </div>
  <div class="right"><img src="images/cover_car_new.png"></div>
  <div class="foot"><span>{DOC_CODE}</span></div>
</div>'''
add(cover)

# ================================================================== #
# PAGE 2 · SUMÁRIO
# ================================================================== #
sumario_body = title("Sumário") + lead(
    "Este manual de operação e desenvolvimento descreve todas as funções e componentes do veículo "
    "autônomo Tony Tunado, desenvolvido como resposta ao desafio proposto pela Mercedes-Benz ao 4º ano "
    "de Engenharia Mecatrônica da FIAP em 2026."
)

# index grid filled after page numbers are known · placeholder token replaced later
sumario_body += '<div class="idx-grid">%%IDXGRID%%</div>'
add(page("sumario", "Sumário", 2, sumario_body))

# ================================================================== #
# PAGE 4 · PARTIDA RÁPIDA (intro)
# ================================================================== #
p4 = title("Início", sub="Bem-vindo ao Tony Tunado")
p4 += lead(
    "O Tony Tunado é um veículo autônomo em escala desenvolvido pela Apex Team · time de alunos do 4º ano "
    "de Engenharia Mecatrônica da FIAP · como resposta ao desafio proposto pela Mercedes-Benz em 2026. "
    "O projeto integra visão computacional, inteligência artificial, controle embarcado, manufatura CNC e "
    "impressão 3D."
)
p4 += h2("O veículo é capaz de:")
p4 += '''<ul class="checklist">
  <li>Seguir autonomamente uma pista delimitada por faixas laterais brancas</li>
  <li>Detectar e interpretar placas de sinalização viária (modelo YOLO)</li>
  <li>Identificar pedestres e obstáculos via 4 sensores ultrassônicos HC-SR04</li>
  <li>Realizar missões de entrega autônoma ponto a ponto</li>
  <li>Comunicar subsistemas via protocolo CAN J1939 · padrão automotivo SAE</li>
</ul>'''
p4 += callout("info", "O código-fonte do sistema de visão computacional roda em Python no notebook e se "
    "comunica com o Arduino Mega via serial USB a 115.200 bps. Os firmwares dos ATmegas são desenvolvidos "
    "em C++ via CAN 2.0B / J1939 a 250 kbps.")
add(page("partida", "Início", 3, p4))

# ================================================================== #
# PAGE 5 · PARTIDA RÁPIDA (guia + dicas)
# ================================================================== #
p5 = title("Arquitetura Geral", sub="Resumo das principais funcionalidades do Tony Tunado para orientação rápida do operador.")
p5 += diagram(sd.architecture(), "ARQUITETURA GERAL DO SISTEMA", viewbox="0 0 1000 276")
p5 += table(
    ["Etapa", "Descrição", "Componente"],
    [
        ["1. Captura", "Câmera fisheye 160° captura a pista em tempo real", "Câmera USB"],
        ["2. Processamento", "OpenCV: bird's eye view, binarização, detecção de faixas", "Notebook / Python"],
        ["3. Cálculo do erro", "Desvio do centro da pista calculado pelo algoritmo", "PID – Python"],
        ["4. Transmissão", "Ângulo de correção via Serial 115.200 bps", "PySerial"],
        ["5. CAN J1939", "Mega repassa comandos ao barramento a 250 kbps", "Arduino Mega"],
        ["6. Atuação", "Servo corrige direção; RS550 ajusta velocidade", "ATmegas + BTS7960"],
        ["7. Monitoramento", "HC-SR04 detectam obstáculos; Hall mede velocidade", "ATmegas dedicados"],
    ], compact=True, col_widths=["16%","56%","28%"]
)
p5 += h2("Dicas antes de ligar")
p5 += '''<ul class="checklist">
  <li>Certifique-se de que a bateria LiFePO4 está carregada (BMS-40A-4S deve estar em estado normal)</li>
  <li>Conecte o notebook ao Arduino Mega via USB antes de ligar a bateria principal</li>
  <li>Posicione o veículo dentro da pista antes de iniciar o script Python</li>
  <li>Verifique se todos os 6 ATmega328P estão respondendo no barramento CAN antes da largada</li>
</ul>'''
add(page("partida", "Início", 4, p5))

# ================================================================== #
# PAGE 6 · PROCESSAMENTO (Notebook + Arduino Mega)
# ================================================================== #
p6 = title("Hardware", accent="Processamento")
p6 += h2("Notebook")
p6 += lead("O notebook é a central de processamento do sistema de visão computacional. Executa todo o "
    "código Python, processa os frames da câmera em tempo real e envia os dados ao Arduino Mega via Serial USB.")
p6 += '''<ul class="checklist">
  <li>Linguagem: Python 3 | Bibliotecas: OpenCV, PySerial, NumPy</li>
  <li>Conexão com Mega: UART USB 115.200 bps, protocolo 8N1</li>
  <li>Função: frames da câmera &rarr; calcula ângulo PID &rarr; envia ao Mega</li>
</ul>'''
p6 += h2("Arduino Mega 2560")
p6 += imgrow([bare("images/arduino_mega.png", h=190)], cols=3)
p6 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Microcontrolador", "ATmega2560"],
        ["Frequência de clock", "16 MHz"],
        ["Memória Flash", "256 kB (8 kB bootloader)"],
        ["EEPROM", "4 kB"],
        ["SRAM", "8 kB"],
        ["Pinos digitais I/O", "54 (15 com PWM)"],
        ["Entradas analógicas", "16"],
        ["UARTs hardware", "4"],
        ["Tensão de operação", "5 V"],
        ["Tensão de entrada recomendada", "7–12 V"],
        ["Interface SPI", "Sim (MCP2515 – CAN)"],
        ["SKU", "A000067"],
    ], compact=True, col_widths=["40%","60%"]
)
add(page("processamento", "Processamento", 5, p6))

# ================================================================== #
# PAGE 7 · PROCESSAMENTO (ATmega328P modules)
# ================================================================== #
p7 = title("Periféricos", accent="6 Módulos ATmega328P")
p7 += lead("Cada função crítica do veículo é isolada em um módulo dedicado baseado em ATmega328P, todos "
    "conectados ao Arduino Mega pelo barramento CAN 2.0B / J1939. Isso garante que uma falha de firmware em "
    "um módulo não derrube o sistema inteiro.")
p7 += diagram(sd.atmega_modules(), "6 MÓDULOS ATMEGA328P · MAPA DE FUNÇÕES E ENDEREÇOS", viewbox="0 0 966 240")
p7 += table(
    ["Módulo", "Função", "Source Address"],
    [
        ["PCB Motores Traseiros", "Controle de tração traseira – BTS7960", "0x10"],
        ["PCB Motores Dianteiros", "Controle de tração dianteira – BTS7960", "0x11"],
        ["PCB Sinalização", "LEDs RGB e lanternas", "0x20"],
        ["PCB Encoders", "Leitura Hall + velocidade por roda", "0x30"],
        ["PCB Ultrassônicos", "Leitura dos 4 HC-SR04", "0x40"],
        ["PCB BMS", "Monitoramento da bateria", "0x50"],
    ], compact=True, col_widths=["30%","52%","18%"]
)
add(page("processamento", "Processamento", 6, p7))

# ================================================================== #
# PAGE 8 · PROPULSÃO (Motor RS550)
# ================================================================== #
p8 = title("Hardware", accent="Propulsão")
p8 += h2("Motores RS550")
p8 += imgrow([
    bare("images/motor_rs550.png", h=150),
    pending("Motor montado na roda", "Foto do RS550 já instalado no cubo de roda · a equipe vai enviar em breve", tall=False),
], cols=2)
p8 += table(
    ["Parâmetro", "Valor"],
    [
        ["Modelo", "RS550"],
        ["Tipo", "Motor DC com escovas"],
        ["Rotação nominal", "~30.000 RPM (sem carga)"],
        ["Tensão nominal", "12 V DC"],
        ["Configuração", "4WD – um motor por roda"],
        ["Controle", "PWM via driver BTS7960"],
    ], compact=True, col_widths=["40%","60%"]
)
p8 += h2("Driver BTS7960 · Controlador de Alta Corrente")
p8 += lead("Cada motor RS550 é acionado por uma meia-ponte BTS7960 dedicada, controlada em PWM pelo "
    "ATmega328P correspondente. O driver integra proteção contra sobrecorrente, sobretemperatura e curto-circuito.")
add(page("propulsao", "Propulsão", 7, p8))

# ================================================================== #
# PAGE 9 · PROPULSÃO (Driver BTS7960)
# ================================================================== #
p9 = title("Driver BTS7960", accent="Especificações")
p9 += imgrow([bare("images/bts7960.png", h=190)], cols=3)
p9 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Tipo", "Meia ponte (Half-bridge) – NovalithIC"],
        ["Resistência de condução", "16 mΩ a 25 °C"],
        ["Frequência PWM máxima", "Até 25 kHz (roda livre ativa)"],
        ["Corrente limite típica", "43 A"],
        ["Proteção", "Sobrecorrente, sobretemperatura, sobretensão, subtensão"],
        ["Diagnóstico", "Flag de estado + sensoriamento de corrente"],
        ["Controle EMI", "Interruptor alto canal-P (sem bomba de carga)"],
    ], compact=True, col_widths=["40%","60%"]
)
p9 += callout("info", "Um driver BTS7960 é usado por eixo (dianteiro e traseiro), cada um comandado por um "
    "ATmega328P dedicado · ver mapa de módulos na seção Processamento.")
add(page("propulsao", "Propulsão", 8, p9))

# ================================================================== #
# PAGE 10 · DIREÇÃO (Servo)
# ================================================================== #
p10 = title("Hardware", accent="Direção")
p10 += h2("Servo DS51150-12V")
p10 += imgrow([
    bare("images/servo_ds51150.png", h=150),
    pending("Servo montado no veículo", "Foto do servo instalado no conjunto de direção · a equipe vai enviar em breve", tall=False),
], cols=2)
p10 += table(
    ["Parâmetro", "10 V", "12 V", "12,6 V", "Unidade"],
    [
        ["Corrente em repouso", "4", "5", "6", "mA"],
        ["Velocidade sem carga", "0,24", "0,21", "0,19", "seg/60°"],
        ["Torque de bloqueio", "150", "165", "173", "kg&middot;cm"],
        ["Corrente de bloqueio", "7,4", "8,0", "8,3", "A"],
    ], compact=True, numeric_cols={1,2,3}, col_widths=["34%","16%","16%","16%","18%"]
)
p10 += table(
    ["Parâmetro Geral", "Especificação"],
    [
        ["Dimensões", "65 x 30 x 48 mm"],
        ["Peso", "175 g"],
        ["Redução", "357:1"],
        ["Proteção", "IP67"],
        ["Tensão operacional", "9–12,6 V"],
        ["Sinal de controle", "PWM 500–2.500 µs / 50–330 Hz"],
        ["Ângulo de operação", "180 ou 270 graus"],
    ], compact=True, col_widths=["40%","60%"]
)
add(page("direcao", "Direção", 9, p10))

# ================================================================== #
# PAGE 11 · DIREÇÃO (Pinhão / Cremalheira)
# ================================================================== #
p11 = title("Pinhão PIN-001", accent="e Cremalheira CRM-001")
p11 += diagram(sd.rack_pinion(), "DESENHO TÉCNICO · CONJUNTO PINHÃO E CREMALHEIRA", viewbox="0 0 940 230")
p11 += table(
    ["Parâmetro", "Pinhão PIN-001", "Cremalheira CRM-001"],
    [
        ["Material", "Aço SAE 1045", "Aço SAE 1045"],
        ["Módulo", "M = 3", "M = 3"],
        ["Número de dentes", "z = 15", "–"],
        ["Dimensões", "Diâm. 51 mm x alt. 60 mm", "185 x 60 x 20 mm"],
        ["Furo central", "Diâm. 12,3 mm", "–"],
        ["Rugosidade", "Ra ≤ 3,2 µm", "Ra ≤ 3,2 µm"],
        ["Corrida radial", "≤ 0,05 mm", "–"],
        ["Norma", "NBR 6158 (IT8)", "NBR 6158 (IT8)"],
    ], compact=True, col_widths=["34%","33%","33%"]
)
add(page("direcao", "Direção", 10, p11))

# ================================================================== #
# PAGE 12 · SENSORES (HC-SR04)
# ================================================================== #
p12 = title("Hardware", accent="Sensores")
p12 += h2("Sensor Ultrassônico HC-SR04")
p12 += imgrow([bare("images/sensor_hcsr04.png", h=190)], cols=3)
p12 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Modelo", "HC-SR04"],
        ["Tensão", "DC 5 V &middot; Corrente: 15 mA"],
        ["Frequência", "40 kHz"],
        ["Alcance", "2 cm – 4 m &middot; Ângulo: 15 graus"],
        ["Trigger", "Pulso TTL 10 µs"],
        ["Fórmula de distância", "µs / 58 = cm &middot; ciclo mín.: 60 ms"],
        ["Quantidade", "4 unidades (frente, trás, esquerda, direita)"],
    ], compact=True, col_widths=["36%","64%"]
)
p12 += callout("info", "Os quatro sensores HC-SR04 são lidos pelo módulo PCB Ultrassônicos (SA 0x40), que "
    "publica as quatro distâncias no barramento CAN via PGN 0xFF30 a cada ciclo de varredura.")
add(page("sensores", "Sensores", 11, p12))

# ================================================================== #
# PAGE 13 · SENSORES (Hall + Câmera)
# ================================================================== #
p13 = title("Hall KY-035", accent="e Câmera Fisheye")
p13 += h2("Sensor de Efeito Hall KY-035 · Encoder de Roda")
p13 += imgrow([
    bare("images/sensor_ky035.png", h=150),
    pending("Ímã de neodímio no eixo", "Foto do ímã fixado no eixo do motor · a equipe vai enviar em breve"),
], cols=2)
p13 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Modelo", "HR0031 / KY-035 &middot; Sensor: 44E"],
        ["Tensão", "3–6 V DC &middot; Corrente: 4–8 mA"],
        ["Sinal de saída", "Digital ON/OFF – coletor aberto"],
        ["Tempo de resposta", "2 µs"],
        ["Corrente de saída máx.", "25 mA"],
        ["Quantidade", "4 unidades (uma por roda)"],
        ["Função", "Conta pulsos dos ímãs de neodímio no eixo do motor"],
    ], compact=True, col_widths=["36%","64%"]
)
p13 += h2("Câmera USB Fisheye")
p13 += imgrow([
    bare("images/camera_fisheye.png", h=150),
    pending("Câmera montada no veículo", "Foto da câmera instalada no chassi · a equipe vai enviar em breve"),
], cols=2)
add(page("sensores", "Sensores", 12, p13))

# ================================================================== #
# PAGE 14 · ENERGIA (Bateria + BMS)
# ================================================================== #
p14 = title("Hardware", accent="Sistema de Energia")
p14 += h2("Bateria LiFePO4")
p14 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Tecnologia", "LiFePO4 (Lítio Ferro Fosfato)"],
        ["Tensão nominal", "12 V"],
        ["Capacidade", "60 Ah"],
        ["Gerenciamento", "BMS-40A-4S integrado"],
    ], compact=True, col_widths=["36%","64%"]
)
p14 += h2("BMS-40A-4S · Gerenciamento de Bateria")
p14 += imgrow([bare("images/bms_module.png", h=190)], cols=3)
p14 += table(
    ["Parâmetro", "Mín.", "Nominal", "Máx.", "Unidade"],
    [
        ["Tensão de carregamento", "–", "16,8", "18,1", "V"],
        ["Corrente contínua de descarga", "–", "40", "40", "A"],
        ["Proteção sobrecarga/célula", "4,2", "4,25", "4,3", "V"],
        ["Proteção descarga/célula", "2,4", "2,5", "2,6", "V"],
        ["Corrente de balanceamento", "95", "100", "105", "mA"],
        ["Proteção sobrecorrente (-E)", "70", "80", "90", "A"],
        ["Temperatura de operação", "-40", "25", "85", "°C"],
    ], compact=True, numeric_cols={1,2,3}, col_widths=["34%","16%","16%","16%","18%"]
)
add(page("energia", "Energia", 13, p14))

# ================================================================== #
# PAGE 15 · ENERGIA (Relé)
# ================================================================== #
p15 = title("Relé Auxiliar Reversor", accent="DNI 0116")
p15 += lead("O relé reversor universal comanda a inversão de polaridade dos motores traseiros, permitindo a "
    "marcha à ré do veículo sob comando do módulo PCB Motores Traseiros.")
p15 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Modelo", "DNI 0116 – Relé reversor universal"],
        ["Tensão", "12 V DC &middot; Corrente: 40/30 A"],
        ["Terminal 30", "Positivo direto da bateria (12 V)"],
        ["Terminal 85/86", "Lado negativo / positivo da bobina"],
        ["Terminal 87 / 87a", "Contato NA / NF"],
    ], compact=True, col_widths=["36%","64%"]
)
p15 += callout("info", "O relé é acionado eletronicamente pelo módulo de tração traseira · nunca opere a "
    "reversão manualmente com o veículo em movimento.")
add(page("energia", "Energia", 14, p15))

# ================================================================== #
# PAGE 16 · COMUNICAÇÃO (CAN diagram + Serial)
# ================================================================== #
p16 = title("Comunicação")
p16 += diagram(sd.can_network(), "TOPOLOGIA DA REDE CAN J1939 · 7 NÓS", viewbox="0 0 1150 220")
p16 += h2("Serial USB · Notebook e Arduino Mega")
p16 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Protocolo", "UART (Serial USB)"],
        ["Baud rate", "115.200 bps"],
        ["Formato", "8N1 (8 bits, sem paridade, 1 stop bit)"],
        ["Usos", "Ângulo PID; logs; comandos de teste"],
        ["Biblioteca Python", "PySerial"],
    ], compact=True, col_widths=["36%","64%"]
)
add(page("comunicacao", "Comunicação", 15, p16))

# ================================================================== #
# PAGE 17 · COMUNICAÇÃO (CAN table + PGNs)
# ================================================================== #
p17 = title("CAN 2.0B / J1939", accent="Arduino Mega e ATmegas")
p17 += table(
    ["Parâmetro", "Especificação"],
    [
        ["Protocolo base / aplicação", "CAN 2.0B / J1939 (SAE)"],
        ["Velocidade", "250 kbps"],
        ["Transceptor", "MCP2515 via SPI &middot; cristal 8 MHz"],
        ["Topologia", "Barramento linear &middot; terminação 120 Ω"],
        ["Nós na rede", "7 (1 Mega mestre + 6 ATmegas)"],
    ], compact=True, col_widths=["36%","64%"]
)
p17 += h2("PGNs e Source Addresses")
p17 += table(
    ["Nó / Módulo", "Source Address", "PGN", "Descrição"],
    [
        ["Arduino Mega (Mestre)", "0x01", "0xFEF1", "Comando de tração aos motores"],
        ["PCB Motores Traseiros", "0x10", "0xFF00", "Telemetria: RPM, corrente, status"],
        ["PCB Motores Dianteiros", "0x11", "0xFF00", "Telemetria: RPM, corrente, status"],
        ["PCB Sinalização", "0x20", "0xFF10", "Estado LEDs e lanternas"],
        ["PCB Encoders", "0x30", "0xFF20", "Velocidade por roda (Hall)"],
        ["PCB Ultrassônicos", "0x40", "0xFF30", "Distâncias 4x HC-SR04"],
        ["PCB BMS", "0x50", "0xFF40", "Tensão, corrente e temperatura"],
    ], compact=True, col_widths=["26%","16%","14%","44%"]
)
add(page("comunicacao", "Comunicação", 16, p17))

# ================================================================== #
# PAGE 17 · SOFTWARE (Visão computacional)
# ================================================================== #
p18 = title("Software")
p18 += h2("Visão Computacional · Python + OpenCV")
p18 += lead(
    "O algoritmo de navegação roda inteiramente em Python no notebook, processando cada frame da câmera "
    "USB em um pipeline de 8 etapas antes de decidir o ângulo de direção."
)
p18 += diagram(sd.vision_pipeline(), "PIPELINE DE VISÃO COMPUTACIONAL", viewbox="0 0 1000 200")
p18 += table(
    ["Etapa", "Técnica", "Saída"],
    [
        ["1. Captura", "OpenCV VideoCapture (câmera USB)", "Frame bruto (BGR)"],
        ["2. Perspectiva", "4 pontos de controle + getPerspectiveTransform", "ROI 320×240 em vista aérea"],
        ["3. Pré-processamento", "Conversão para escala de cinza", "Imagem em tons de cinza"],
        ["4. Binarização", "Threshold fixo, ajustável no painel de controle", "Imagem binária (P&amp;B)"],
        ["5. Faixas", "Sliding window: 3 janelas horizontais, pixels brancos/coluna", "Posição esq./dir. por janela"],
        ["6. Erro", "Média das janelas válidas vs. centro da imagem", "Erro lateral em pixels"],
        ["7. Controle", "PID reta ou curva, conforme o erro (dual-PID)", "Ângulo de correção (±90°)"],
        ["8. Transmissão", "JSON via Serial 115.200 bps, a cada 200 ms", "servo/velocidade ao Arduino Mega"],
    ], compact=True, col_widths=["16%","54%","30%"]
)
p18 += h2("Painel de Ajuste em Tempo Real")
p18 += lead(
    "Todos os parâmetros abaixo são ajustáveis ao vivo, por sliders no painel de controle ou pelo "
    "dashboard web, e podem ser persistidos em config/config.json."
)
p18 += table(
    ["Parâmetro", "Exemplo salvo", "Efeito"],
    [
        ["ROI &middot; Linha superior/inferior", "525 / 385 px", "Largura do topo e da base do trapézio de perspectiva"],
        ["ROI &middot; Altura sup./inf.", "192 / 286 px", "Posição vertical do topo/base do trapézio na imagem"],
        ["Limiar de binarização", "217", "Nível de cinza acima do qual um pixel vira 'faixa'"],
        ["Erro de transição", "12 px", "Limite para trocar entre PID de reta e de curva"],
    ], compact=True, col_widths=["30%","20%","50%"]
)
add(page("software", "Software", 17, p18))

# ================================================================== #
# PAGE 18 · SOFTWARE (Detecção de faixas · sliding window)
# ================================================================== #
p18b = title("Software", accent="Sliding Window")
p18b += lead(
    "Dentro da ROI já convertida em vista aérea e binarizada, o algoritmo localiza as duas faixas da "
    "pista sem nenhuma rede neural &mdash; apenas contagem de pixels brancos por coluna."
)
p18b += h2("Busca por Janelas Deslizantes")
p18b += table(
    ["Passo", "O que acontece"],
    [
        ["1", "A ROI (320&times;240) é dividida em 3 janelas horizontais de mesma altura"],
        ["2", "Em cada janela, conta-se o número de pixels brancos em cada coluna"],
        ["3", "A coluna com mais pixels na metade esquerda vira a 'faixa esquerda'; idem à direita"],
        ["4", "A faixa só é considerada válida se o total de pixels superar 10% da altura da janela"],
        ["5", "As posições válidas das 3 janelas são combinadas por média, definindo a posição final"],
    ], compact=True, col_widths=["8%","92%"]
)
p18b += h2("4 Estados da Pista")
p18b += table(
    ["Estado", "Condição", "Cálculo do centro"],
    [
        ["both", "As duas faixas válidas", "Média entre esquerda e direita"],
        ["left", "Só a faixa esquerda válida", "Esquerda + metade do track_size (estimado)"],
        ["right", "Só a faixa direita válida", "Direita − metade do track_size (estimado)"],
        ["none", "Nenhuma faixa válida", "Mantém o último erro conhecido"],
    ], compact=True, col_widths=["14%","40%","46%"]
)
p18b += callout("info", "track_size guarda a última largura de pista medida (distância entre as duas faixas) "
    "sempre que ambas são detectadas ao mesmo tempo. Quando só uma faixa aparece, essa memória é usada "
    "para estimar onde a outra deveria estar, em vez de simplesmente perder a referência.")
p18b += callout("info", "O erro final é a diferença, em pixels, entre o centro calculado da pista e o centro "
    "da imagem. Um círculo verde marca o centro da pista e um vermelho o ponto de referência &mdash; ambos "
    "exibidos ao vivo na aba de câmeras do painel de controle.")
add(page("software", "Software", 18, p18b))

# ================================================================== #
# PAGE 19 · SOFTWARE (Inteligência Artificial · YOLO)
# ================================================================== #
p19 = title("Inteligência Artificial", accent="YOLO")
p19 += lead(
    "Um modelo YOLOv11 (model/Modelo_3.pt) roda em uma thread própria, independente da visão principal "
    "&mdash; assim, a inferência (mais lenta) nunca atrasa o laço que dirige o carro."
)
p19 += table(
    ["Evento", "Critério de validação", "Ação"],
    [
        ["Placa PARE", "Confiança ≥ 80% · área ≥ 1.500 px² · diagonal mínima", "Velocidade 0 por 3–5 s, depois cooldown de 3–5 s"],
        ["Semáforo vermelho", "Maior confiança entre os semáforos no frame", "Velocidade 0 até detectar verde"],
        ["Semáforo amarelo", "Idem, cor classificada pelo recorte da caixa", "Reduz para % configurável da velocidade base"],
        ["Semáforo verde / nenhum", "Sem detecção válida por 2 s &rarr; estado 'nenhum'", "Velocidade normal configurada"],
    ], compact=True, col_widths=["20%","44%","36%"]
)
p19 += callout("info", "A cor do semáforo é decidida sem uma rede neural dedicada: o recorte da caixa detectada "
    "pelo YOLO é convertido para tons de cinza e dividido em 3 faixas horizontais (topo/meio/base) &mdash; a "
    "faixa com maior brilho médio indica a lâmpada acesa, seguindo o mesmo layout físico do semáforo "
    "(vermelho/amarelo/verde).")
p19 += h2("Ciclo de Inferência")
p19 += table(
    ["Parâmetro", "Valor padrão", "Descrição"],
    [
        ["Intervalo de detecção", "A cada 5 frames", "Frequência de execução do YOLO (ajustável)"],
        ["Confiança mínima (STOP)", "80%", "Abaixo disso a caixa detectada é ignorada"],
        ["Área mínima (STOP)", "1.500 px²", "Evita ativar STOP com placas pequenas/distantes"],
        ["Tempo de parada / cooldown", "3–5 s / 3–5 s", "Duração do freio e intervalo mínimo antes do próximo PARE"],
        ["Timeout do semáforo", "2 s", "Sem detecção válida por esse tempo &rarr; estado 'nenhum'"],
    ], compact=True, col_widths=["28%","20%","52%"]
)
p19 += callout("info", "A thread de sinais lê apenas o frame mais recente compartilhado (protegido por um "
    "lock) e atualiza duas variáveis de estado que o laço principal apenas consulta a cada iteração. Não "
    "existe fila: se a IA ainda está processando, o carro segue com o último estado conhecido, sem travar.")
add(page("software", "Software", 19, p19))

# ================================================================== #
# PAGE 20 · SOFTWARE (Controle Dual-PID e protocolo)
# ================================================================== #
p19b = title("Controle", accent="Dual-PID")
p19b += lead(
    "O erro lateral (em pixels) alimenta dois controladores PID independentes &mdash; ajustados "
    "separadamente para trechos retos e curvas &mdash; escolhidos automaticamente a cada ciclo."
)
p19b += diagram(sd.pid_loop(), "MALHA DE CONTROLE PID · DIREÇÃO AUTÔNOMA", viewbox="0 0 900 230")
p19b += h2("Fórmula e Comutação Reta/Curva")
p19b += table(
    ["Termo", "Fórmula", "Papel"],
    [
        ["Proporcional (P)", "Kp &times; erro", "Resposta imediata ao desvio atual"],
        ["Integral (I)", "Ki &times; &Sigma;(erro &times; dt)", "Corrige desvio acumulado/persistente"],
        ["Derivativo (D)", "Kd &times; (erro − erro_anterior) / dt", "Amortece mudanças bruscas"],
        ["Saída", "P + I + D, limitada a ±90°", "Ângulo de correção somado a 90° e enviado ao servo"],
    ], compact=True, col_widths=["18%","36%","46%"]
)
p19b += callout("info", "Reta vs. curva: quando o erro está dentro do limiar 'Erro de transição' (12 px no "
    "exemplo salvo), o PID de reta assume, com ganhos mais suaves. Fora desse limiar, o PID de curva "
    "assume, com ganhos mais agressivos para reagir mais rápido.")
p19b += h2("Envio ao Arduino Mega")
p19b += table(
    ["Campo", "Tipo", "Significado"],
    [
        ["servo", "int, 0–180", "90 = centro; ângulo do PID somado a 90"],
        ["speed", "float", "Velocidade efetiva (m/s); 0 quando parado, em STOP ou vermelho"],
        ["stop", "bool", "True força parada imediata"],
        ["tl", "int, -1 a 2", "Estado do semáforo: nenhum/vermelho/amarelo/verde"],
        ["lights", "int, 0/1", "Iluminação do veículo"],
    ], compact=True, col_widths=["16%","20%","64%"]
)
p19b += lead("O pacote é serializado em JSON e enviado a cada 'Intervalo de comando' (200 ms por padrão) "
    "via Serial a 115.200 bps.")
add(page("software", "Software", 20, p19b))

# ================================================================== #
# PAGE 21 · SOFTWARE (Painel de controle e dashboard)
# ================================================================== #
p19c = title("Software", accent="Painel de Controle")
p19c += lead(
    "Duas interfaces permitem operar e depurar o veículo em tempo real: um painel desktop com visão ao "
    "vivo, e um dashboard web para acesso remoto pelo celular."
)
p19c += h2("Painel Desktop")
p19c += table(
    ["Aba", "Conteúdo"],
    [
        ["Câmeras ao vivo", "3 vistas simultâneas: câmera da pista, vista aérea com faixas, e detecções de sinais &mdash; até 30 FPS, sem fila, sempre o frame mais recente"],
        ["Pista e Direção", "Sliders de ROI, limiar de binarização, erro de transição e os 6 ganhos do PID (reta/curva)"],
        ["Carro e Sinais", "Velocidade alvo, % de velocidade no amarelo, ângulo máximo, intervalo de comando e limiares de confiança/tamanho para PARE e semáforo"],
        ["Informações do Carro", "Telemetria ao vivo: erro da faixa, modo PID ativo, velocidade recebida/aplicada, bateria, distância dos 3 ultrassônicos e status de cada módulo"],
        ["Conexão e Registros", "Porta COM e índice de câmera, reconexão a quente, e um log colorido (info/ok/aviso/erro/RX/TX) com horário"],
    ], compact=True, col_widths=["22%","78%"]
)
p19c += callout("info", "A visualização de câmera nunca compete com o controle do carro: roda em sua própria "
    "janela de atualização (33 ms) e exibe só a imagem mais recente &mdash; frames não consumidos a tempo "
    "são descartados, sem acumular atraso na direção.")
p19c += h2("Dashboard Web (porta 5000)")
p19c += table(
    ["Rota", "Método", "Função"],
    [
        ["/api/config", "GET / POST", "Lê ou atualiza os parâmetros (ROI, PID, velocidade, confiança dos sinais)"],
        ["/api/dashboard", "GET", "Telemetria simplificada para o Digital Twin (rpm estimado, luz ligada)"],
        ["/api/reset", "POST", "Restaura os parâmetros salvos em config/config.json"],
        ["/panel", "GET", "Painel HTML simplificado com sliders, otimizado para celular"],
    ], compact=True, col_widths=["20%","18%","62%"]
)
p19c += callout("info", "O dashboard é liberado no Firewall do Windows automaticamente na primeira execução, "
    "e pode ser aberto no celular lendo um QR Code gerado direto no painel desktop.")
add(page("software", "Software", 21, p19c))

# ================================================================== #
# PAGE 22 · SOFTWARE (Firmware embarcado)
# ================================================================== #
p19d = title("Software", accent="Firmware Embarcado")
p19d += lead(
    "O Arduino Mega recebe os comandos vindos do notebook e traduz para acionamento físico dos motores "
    "e do servo, além de uma camada extra de segurança independente contra obstáculos."
)
p19d += h2("Controle dos 4 Motores (Ponte H)")
p19d += table(
    ["Recurso", "Comportamento"],
    [
        ["HBridgeController", "Uma instância por roda (4 no total), cada uma com seus pinos RPWM/LPWM"],
        ["move(vel)", "Define a velocidade alvo (-255 a 255); o sinal define frente ou ré"],
        ["Aceleração progressiva", "Opcional: incrementa o PWM em passos (padrão 5) a cada 10 ms até o alvo, evitando arrancadas bruscas"],
        ["stop()", "Zera a velocidade e desliga o PWM imediatamente, sem rampa"],
    ], compact=True, col_widths=["26%","74%"]
)
p19d += h2("Servo com Rampa Suave")
p19d += lead(
    "Assim como os motores, o ângulo do servo não salta direto para o valor recebido: o firmware o "
    "desloca em passos de 1° a cada 1 ms até alcançar o alvo, resultando em uma direção mecanicamente "
    "mais suave."
)
p19d += h2("Camada de Segurança Independente")
p19d += lead(
    "Um segundo microcontrolador (Arduino UNO) lê 3 sensores ultrassônicos de forma não bloqueante e "
    "envia apenas 'PARE' ou 'PROSSIGA' ao Mega por uma serial dedicada (Serial1)."
)
p19d += table(
    ["Sensor", "Alcance máx.", "Distância de segurança"],
    [
        ["Frontal", "200 cm", "≤ 40 cm aciona PARE"],
        ["Lateral esquerdo", "100 cm", "≤ 25 cm aciona PARE"],
        ["Lateral direito", "100 cm", "≤ 25 cm aciona PARE"],
    ], compact=True, col_widths=["30%","30%","40%"]
)
p19d += callout("aviso", "O Mega só muda de estado (PARE &#8644; PROSSIGA) depois de receber a mesma "
    "mensagem 10 vezes seguidas do UNO &mdash; um filtro anti-ruído que evita frenagens falsas por leituras "
    "isoladas ruins do sensor. Essa parada por obstáculo é independente do STOP enviado pelo notebook: "
    "qualquer uma das duas pode parar o veículo.")
add(page("software", "Software", 22, p19d))

# ================================================================== #
# PAGE 20 · PEÇAS MECÂNICAS (tabela + conjunto)
# ================================================================== #
p20 = title("Peças Mecânicas", accent="e Componentes Fabricados")
p20 += table(
    ["Código", "Nome da Peça", "Processo", "Material", "Observações"],
    [
        ["PIN-001", "Pinhão de Direção", "Tornear + Fresar CNC", "SAE 1045", "M=3, z=15, Diâm. 51x60 mm"],
        ["CRM-001", "Cremalheira de Direção", "Fresamento CNC", "SAE 1045", "185x60x20 mm"],
        ["CRW-001", "Hub de Roda c/ Encoder", "Usinagem CNC", "SAE 1045", "Suporte sensor Hall"],
        ["ESV-001", "Suporte do Servo", "CNC + Impressão 3D", "PLA/Aço", "Fixação DS51150"],
        ["EIX-001", "Eixo de Transmissão", "Tornear CNC", "SAE 1045", "Motores às rodas"],
        ["–", "Case Servo Superior", "Impressão 3D (FDM)", "PLA", "Proteção superior do servo"],
        ["–", "Case Servo Inferior", "Impressão 3D (FDM)", "PLA", "Base de fixação"],
        ["–", "Conector de Direção", "Impressão 3D (FDM)", "PLA", "Acoplamento servo-cremalheira"],
        ["–", "Calota Apex", "Impressão 3D (FDM)", "PLA", "Elemento estético das rodas"],
        ["–", "Lanterna", "Impressão 3D (FDM)", "PLA", "Suporte dos LEDs traseiros"],
    ], compact=True, col_widths=["11%","23%","19%","13%","34%"]
)
p20 += imgrow([
    icard("images/pinhao.png", "Pinhão de Direção", code="PIN-001", h=112),
    icard("images/cremalheira.png", "Cremalheira de Direção", code="CRM-001", h=112),
    icard("images/encoder.png", "Hub de Roda c/ Encoder", code="CRW-001", h=112),
    icard("images/case_servo_cima.png", "Case Servo Superior", h=112),
    icard("images/case_servo_baixo.png", "Case Servo Inferior", h=112),
    icard("images/conector_direcao.png", "Conector de Direção", h=112),
    icard("images/calota.png", "Calota Apex", h=112),
    icard("images/lanterna.png", "Lanterna", h=112),
], cols=4)
add(page("pecas", "Peças Mecânicas", 23, p20))

# ================================================================== #
# PAGE 21 · PEÇAS MECÂNICAS (renders + controle dimensional)
# ================================================================== #
p21 = title("Montagem", accent="e Controle Dimensional")
p21 += imgrow([
    pending("Render 3D · conjunto de direção", "Pinhão + cremalheira + servo · a equipe vai enviar em breve"),
    pending("Montagem mecânica final", "Foto da montagem completa no veículo · a equipe vai enviar em breve"),
], cols=2)
p21 += h2("Controle Dimensional · Pinhão PIN-001 (Operação 060 – 100% das peças)")
p21 += table(
    ["Verificação", "Instrumento", "Critério"],
    [
        ["Diâmetro externo", "Paquímetro digital 0,01 mm", "Diâm. 51 mm"],
        ["Altura total", "Paquímetro digital", "60 mm"],
        ["Furo central", "Calibre passa/não-passa", "Diâm. 12,3 mm"],
        ["Perfil dos dentes", "Gabarito de módulo M=3", "Conforme perfil"],
        ["Corrida radial", "Relógio comparador", "≤ 0,05 mm"],
        ["Rugosidade", "Rugosímetro", "Ra ≤ 3,2 µm"],
    ], compact=True, col_widths=["32%","38%","30%"]
)
add(page("pecas", "Peças Mecânicas", 24, p21))

def rpn_row(etapa, falha, efeito, s_, o_, d_):
    rpn = s_*o_*d_
    marker = "__CRIT__" if rpn >= 100 else ("__ALTO__" if rpn >= 60 else None)
    row = [etapa, falha, efeito, str(s_), str(o_), str(d_), str(rpn)]
    return [marker] + row if marker else row

# ================================================================== #
# PAGE 22 · FMEA (legenda + bloco 1)
# ================================================================== #
p22 = title("FMEA", accent="Análise de Modos e Efeitos de Falha")
p22 += lead("A FMEA cobre três blocos: (1) Manufatura, (2) Eletrônica e Embarcado, (3) Software e IA. "
    "RPN = S x O x D &nbsp;|&nbsp; Escala AIAG 1–10.")
p22 += table(
    ["Faixa RPN", "Prioridade", "Ação"],
    [
        ["RPN ≥ 100", "CRÍTICO", "Ação corretiva imediata obrigatória"],
        ["RPN 60–99", "ALTO", "Ação preventiva antes da demonstração"],
        ["RPN < 60", "MODERADO", "Monitorar na evolução do projeto"],
    ], compact=True, col_widths=["22%","20%","58%"]
)
p22 += h2("Bloco 1 · Manufatura")
p22 += table(
    ["Etapa", "Falha", "Efeito", "S", "O", "D", "RPN"],
    [
        rpn_row("Pinhão – Tornear", "Diâm. fora de tolerância", "Folga no engrenamento", 7,3,2),
        rpn_row("Pinhão – Fresar", "Perfil de dente incorreto", "Vibração e ruído", 8,3,2),
        rpn_row("Cremalheira – Fresar", "Passo linear incorreto", "Imprecisão de direção", 7,2,2),
        rpn_row("Suporte Servo – Furar", "Furo fora de posição", "Servo desalinhado", 6,2,2),
        rpn_row("Inspeção Final", "Corrida radial >0,05 mm", "Vibração no sistema", 7,2,1),
    ], compact=True, numeric_cols={3,4,5,6}, col_widths=["19%","25%","25%","8%","8%","8%","9%"]
)
add(page("fmea", "FMEA", 25, p22))

# ================================================================== #
# PAGE 23 · FMEA (bloco 2 + bloco 3)
# ================================================================== #
p23 = title("Blocos 2 e 3", accent="Eletrônica, Software e IA")
p23 += h2("Bloco 2 · Eletrônica e Embarcado")
p23 += table(
    ["Etapa", "Falha", "Efeito", "S", "O", "D", "RPN"],
    [
        rpn_row("Driver BTS7960", "Sobrecorrente", "Queima do driver", 8,3,3),
        rpn_row("Comunicação CAN", "Perda de mensagem", "Comando não executado", 8,3,2),
        rpn_row("Servo DS51150", "Não responde ao PWM", "Perda de direção", 9,2,2),
        rpn_row("Sensor Hall", "Falha de leitura", "Velocidade incorreta", 6,3,2),
        rpn_row("BMS-40A-4S", "Desconexão por pico", "Perda total de energia", 9,2,2),
        rpn_row("HC-SR04", "Leitura errônea", "Colisão com obstáculo", 7,4,3),
    ], compact=True, numeric_cols={3,4,5,6}, col_widths=["19%","25%","25%","8%","8%","8%","9%"]
)
p23 += h2("Bloco 3 · Software e IA")
p23 += table(
    ["Etapa", "Falha", "Efeito", "S", "O", "D", "RPN"],
    [
        rpn_row("Bird's Eye View", "Homografia errada", "Erro no cálculo da faixa", 7,3,3),
        rpn_row("PID – Direção", "Instabilidade", "Veículo oscilando", 7,4,2),
        rpn_row("YOLO – Detecção", "Falso positivo", "Parada indevida", 7,3,3),
        rpn_row("Serial – Comunicação", "Perda de frame", "Ângulo não recebido", 8,2,2),
        rpn_row("Integração Visão+CAN", "Latência excessiva", "Atraso na correção", 6,3,3),
    ], compact=True, numeric_cols={3,4,5,6}, col_widths=["19%","25%","25%","8%","8%","8%","9%"]
)
add(page("fmea", "FMEA", 26, p23))

# ================================================================== #
# PAGE 24 · PERT/CPM (diagrama)
# ================================================================== #
p24 = title("PERT/CPM", accent="Planejamento do Projeto")
p24 += lead("Planejamento com 22 atividades em 3 frentes paralelas (Controle/Software, Digital Twins, "
    "Manufatura) convergindo na Integração. Caminho crítico: A1 &rarr; A2 &rarr; A3 &rarr; A7 &rarr; D1 &rarr; "
    "D2 &rarr; D3 (~29 dias úteis).")
gantt_svg, gantt_h = sd.pert_gantt()
p24 += diagram(gantt_svg, "REDE PERT/CPM · CRONOGRAMA POR ATIVIDADE (TRACEJADO = CAMINHO CRÍTICO)",
                viewbox=f"0 0 1000 {int(gantt_h)}")
p24 += '''<div class="legend" style="margin-top:8px;">
  <span><span class="dot" style="background:#3684ad;"></span>Controle / Software</span>
  <span><span class="dot" style="background:#5a9e82;"></span>Digital Twins</span>
  <span><span class="dot" style="background:#b3873f;"></span>Manufatura</span>
  <span><span class="dot" style="background:#b8524f;"></span>Integração</span>
</div>'''
add(page("pert", "PERT / CPM", 27, p24, tight=True))

# ================================================================== #
# PAGE 25 · PERT/CPM (tabela completa)
# ================================================================== #
p25 = title("Atividades", accent="e Predecessoras")
pert_rows = [
    ["A1", "Definição de requisitos e arquitetura", "Controle/Software", "5", "–"],
    ["A2", "Sistema de visão computacional", "Controle/Software", "10", "A1"],
    ["A3", "Algoritmo PID de direção", "Controle/Software", "5", "A2"],
    ["A4", "Comunicação Serial/CAN", "Controle/Software", "6", "A1"],
    ["A5", "Programação ATmega328P", "Controle/Software", "8", "A4"],
    ["A6", "Testes individuais (motores, servo)", "Controle/Software", "4", "A5"],
    ["A7", "Integração hardware + visão", "Controle/Software", "5", "A3, A6"],
    ["A8", "Testes integrados + ajuste PID", "Controle/Software", "4", "A7"],
    ["B1", "Modelagem 3D – CRM-001", "Digital Twins", "3", "A1"],
    ["B2", "Modelagem 3D – PIN-001", "Digital Twins", "3", "A1"],
    ["B3", "Modelagem 3D – CRW-001", "Digital Twins", "3", "A1"],
    ["B4", "Modelagem 3D – ESV-001 e Eixo", "Digital Twins", "3", "A1"],
    ["B5", "Revisão e aprovação dos modelos", "Digital Twins", "2", "B1–B4"],
    ["C1", "Usinagem – ESV-001", "Manufatura", "5", "B4"],
    ["C2", "Usinagem – CRW-001", "Manufatura", "6", "B3"],
    ["C3", "Usinagem – PIN-001", "Manufatura", "7", "B2"],
    ["C4", "Usinagem – CRM-001", "Manufatura", "4", "B1"],
    ["C5", "Usinagem – EIX-001", "Manufatura", "3", "B4"],
    ["C6", "Inspeção dimensional", "Manufatura", "3", "C1–C5"],
    ["D1", "Montagem mecânica + integração elétrica", "Integração", "4", "A7, C6"],
    ["D2", "Testes na pista – navegação autônoma", "Integração", "3", "D1, A8"],
    ["D3", "Documentação e entrega", "Integração", "2", "D2"],
]
p25 += table(
    ["Cód.", "Atividade", "Frente", "Dias", "Predecessoras"],
    pert_rows, compact=True, col_widths=["8%","40%","20%","10%","22%"]
)
add(page("pert", "PERT / CPM", 28, p25))

# ================================================================== #
# PAGE 26 · DADOS TÉCNICOS
# ================================================================== #
p26 = title("Dados Técnicos", accent="Consolidados")
p26 += table(
    ["Sistema", "Parâmetro", "Valor"],
    [
        ["Propulsão", "Motores", "4x RS550 ~30.000 RPM | 4WD"],
        ["Propulsão", "Driver", "BTS7960 – 43 A típico, PWM até 25 kHz"],
        ["Direção", "Servo", "DS51150-12V – 150 kg&middot;cm / 12 V / IP67"],
        ["Direção", "Controle", "PWM 500–2.500 µs / 50–330 Hz"],
        ["Direção", "Mecanismo", "Pinhão M=3 z=15 + Cremalheira SAE 1045"],
        ["Energia", "Bateria", "LiFePO4 12 V / 60 Ah"],
        ["Energia", "BMS", "BMS-40A-4S – 40 A contínuo, 4 células, balanceamento 100 mA"],
        ["Energia", "Relé", "DNI 0116 – 40/30 A, 12 V"],
        ["Sensores", "Ultrassônico", "4x HC-SR04 – 2 cm a 4 m, 15 graus"],
        ["Sensores", "Hall / Encoder", "4x KY-035 (44E) + ímã de neodímio"],
        ["Sensores", "Câmera", "USB fisheye 160–180 graus, 2 MP, 30 fps"],
        ["Processamento", "Visão", "Notebook – Python 3 / OpenCV"],
        ["Processamento", "ECU central", "Arduino Mega 2560 – ATmega2560, 16 MHz"],
        ["Processamento", "Periféricos", "6x ATmega328P dedicados"],
        ["Comunicação", "Notebook &rarr; Mega", "UART USB 115.200 bps 8N1"],
        ["Comunicação", "Mega &rarr; ATmegas", "CAN 2.0B / J1939 – 250 kbps / MCP2515"],
        ["Software", "Visão", "Python + OpenCV – bird's eye view + PID"],
        ["Software", "IA", "YOLO – dataset personalizado"],
        ["Software", "Firmware", "C++ / Arduino Framework"],
        ["Mecânica", "Fabricação", "CNC SAE 1045 + Impressão 3D PLA"],
        ["Mecânica", "Norma", "NBR 6158 – IT8 | Ra ≤ 3,2 µm"],
        ["Equipe", "Time", "Apex Team – FIAP Mecatrônica 4º Ano"],
        ["Projeto", "Desafio", "Mercedes-Benz 2026 | São Paulo – SP"],
    ], compact=True, col_widths=["18%","22%","60%"]
)
add(page("dados", "Dados Técnicos", 29, p26))

# ================================================================== #
# PAGE 27 · CONTRACAPA
# ================================================================== #
back = f'''<div class="cover" style="justify-content:center;">
  <div class="left" style="width:100%; align-items:center; text-align:center; padding:0; justify-content:center;">
    <img class="logo" src="images/apex_logo.png" style="margin:0 auto 34px auto;">
    <div class="rule" style="margin:0 auto 26px auto;"></div>
    <div class="subtitle" style="max-width:560px;">Apex Team &middot; Manual de Operação e Desenvolvimento<br>FIAP &middot; Desafio Mercedes-Benz 2026</div>
    <div class="meta" style="text-align:center;">{DOC_CODE}</div>
  </div>
</div>'''
add(back)

print("Built all pages.", len(PAGES_HTML))

# ---- fill sumário index grid now that page numbers are fixed ----
IDX = [
    ("01", "Início", 3, "partida"),
    ("02", "Processamento", 5, "processamento"),
    ("03", "Propulsão", 7, "propulsao"),
    ("04", "Direção", 9, "direcao"),
    ("05", "Sensores", 11, "sensores"),
    ("06", "Energia", 13, "energia"),
    ("07", "Comunicação", 15, "comunicacao"),
    ("08", "Software", 17, "software"),
    ("09", "Peças Mecânicas", 23, "pecas"),
    ("10", "FMEA", 25, "fmea"),
    ("11", "PERT / CPM", 27, "pert"),
    ("12", "Dados Técnicos", 29, "dados"),
]
idx_html = "".join(idx_card(n, label, pno, key) for n, label, pno, key in IDX)
PAGES_HTML[1] = PAGES_HTML[1].replace("%%IDXGRID%%", idx_html)

# ================================================================== #
# FINAL ASSEMBLY
# ================================================================== #
PRINT_BUTTON = '''<button class="print-fab" onclick="window.print()" title="Abre a caixa de impressao do navegador -- escolha \'Salvar como PDF\'.">
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 14h12v7H6v-7z" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  Gerar PDF
</button>'''

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Tony Tunado &middot; Manual de Operação e Desenvolvimento</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{''.join(PAGES_HTML)}
{PRINT_BUTTON}
</body>
</html>'''

with open(BASE_DIR / "manual.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Wrote manual.html -", len(html), "bytes,", len(PAGES_HTML), "pages")
