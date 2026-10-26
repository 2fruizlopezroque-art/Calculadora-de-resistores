import math
import streamlit as st
import streamlit.components.v1 as components
from bisect import bisect_left

# ==========================================
# SERIES COMERCIALES (E12 & E96)
# ==========================================

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

E96 = [
    1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18,
    1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43,
    1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74,
    1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10,
    2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55,
    2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09,
    3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74,
    3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53,
    4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
    5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65,
    6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06,
    8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76
]

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================

st.set_page_config(
    page_title="SYNTH-OHM // Resistor Matrix",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# ESTILOS CYBERPUNK / DARK SCI-FI
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=JetBrains+Mono:wght@400;600;800&display=swap');

/* Fondo general y reset */
.stApp {
    background-color: #080b10;
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(0, 243, 255, 0.08) 0%, transparent 60%),
        linear-gradient(rgba(0, 243, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 243, 255, 0.03) 1px, transparent 1px);
    background-size: 100% 100%, 30px 30px, 30px 30px;
    color: #c0caf5;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label, div, span {
    font-family: 'JetBrains Mono', monospace;
}

/* Encabezado Neón */
.cyber-header {
    text-align: center;
    padding: 15px 0 25px 0;
}

.cyber-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(24px, 4vw, 42px);
    font-weight: 900;
    letter-spacing: 4px;
    color: #00f3ff;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.6), 0 0 25px rgba(0, 243, 255, 0.3);
    margin: 0;
}

.cyber-subtitle {
    font-size: 13px;
    color: #a9b1d6;
    letter-spacing: 2px;
    margin-top: 8px;
    text-transform: uppercase;
}

.cyber-badge-top {
    display: inline-block;
    background: rgba(0, 243, 255, 0.1);
    border: 1px solid #00f3ff;
    color: #00f3ff;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 10px;
}

/* Inputs y Selects */
div[data-baseweb="input"] > div {
    background-color: #0d131f !important;
    border: 1px solid #1f2d45 !important;
    border-radius: 6px !important;
    color: #00f3ff !important;
}

div[data-baseweb="input"] input {
    color: #00f3ff !important;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}

div[data-baseweb="select"] > div {
    background-color: #0d131f !important;
    border: 1px solid #1f2d45 !important;
    border-radius: 6px !important;
    color: #00f3ff !important;
}

/* Botón cibernético */
.stButton > button {
    background: linear-gradient(135deg, #00f3ff, #7000ff);
    color: #000;
    border: none;
    height: 48px;
    border-radius: 6px;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 14px;
    letter-spacing: 2px;
    width: 100%;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
    transition: all 0.3s ease;
    text-transform: uppercase;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00f3ff, #ff007f);
    color: #fff;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.8);
    transform: translateY(-2px);
}

/* Título de resultados */
.results-header {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    color: #ff007f;
    font-size: 16px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 35px 0 15px;
    text-shadow: 0 0 10px rgba(255, 0, 127, 0.5);
}

/* Caja de info */
.info-box-cyber {
    background: #0d131f;
    border: 1px solid #1f2d45;
    border-left: 4px solid #00f3ff;
    border-radius: 8px;
    padding: 20px;
    margin-top: 30px;
    color: #a9b1d6;
    font-size: 13px;
    line-height: 1.8;
}

.info-box-cyber h3 {
    font-family: 'Orbitron', sans-serif;
    color: #00f3ff;
    margin-top: 0;
    font-size: 16px;
    letter-spacing: 1px;
}

.footer-cyber {
    text-align: center;
    color: #414868;
    font-size: 11px;
    letter-spacing: 2px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FORMATO DE VALORES Y COLORES DE BANDAS
# ==========================================

def fmt(r):
    if r >= 1_000_000:
        return f"{r / 1_000_000:.4g} MΩ"
    if r >= 1000:
        return f"{r / 1000:.4g} kΩ"
    return f"{r:.4g} Ω"


def generar_valores(serie):
    valores = set()
    for exponente in range(-3, 9):
        for base in serie:
            valores.add(round(base * 10**exponente, 10))
    return sorted(valores)


def bandas_color(valor):
    colores = [
        "#171717", "#854b26", "#e53935", "#f57c00",
        "#f1c40f", "#27ae60", "#2878c8", "#7b3fa1",
        "#777777", "#ffffff"
    ]
    if valor <= 0:
        return ["#171717", "#171717", "#171717", "#bfa46b"]

    exponente = math.floor(math.log10(valor)) - 1
    cifras = round(valor / (10 ** exponente))

    if cifras >= 100:
        cifras //= 10
        exponente += 1

    d1 = max(0, min(9, cifras // 10))
    d2 = max(0, min(9, cifras % 10))

    if exponente < 0:
        multiplicador = "#bfc3c7"
    elif exponente <= 9:
        multiplicador = colores[exponente]
    else:
        multiplicador = "#ffffff"

    return [
        colores[d1], colores[d2],
        multiplicador, "#bfa46b"
    ]


def dibujar_resistencia(valor):
    bandas = "".join(
        f'<span class="band" style="background:{color}"></span>'
        for color in bandas_color(valor)
    )
    return f"""
    <div class="resistor-card">
        <div class="wire">
            <div class="resistor-body">{bandas}</div>
        </div>
        <div class="res-value">{fmt(valor)}</div>
    </div>
    """


# ==========================================
# MOTOR DE BÚSQUEDA DE COMBINACIONES
# ==========================================

def buscar_combinaciones(objetivo, tolerancia):
    serie = E12 if tolerancia == 10 else E96
    valores = generar_valores(serie)

    conductancias = sorted((1 / r, r) for r in valores)
    gs = [g for g, r in conductancias]
    objetivo_g = 1 / objetivo

    resultados = {}

    def guardar(equiv, resistencias, tipo, formula):
        if equiv <= 0 or not math.isfinite(equiv):
            return

        error = abs(equiv - objetivo) / objetivo * 100
        resistencias = tuple(sorted(resistencias))
        clave = (tipo, resistencias)

        if clave not in resultados or error < resultados[clave]["error"]:
            resultados[clave] = {
                "valor": equiv,
                "resistencias": resistencias,
                "tipo": tipo,
                "formula": formula,
                "error": error
            }

    def cercano(lista, objetivo_local, minimo=0):
        if objetivo_local <= 0 or minimo >= len(lista):
            return None

        pos = bisect_left(lista, objetivo_local, lo=minimo)
        candidatos = []

        if pos < len(lista):
            candidatos.append(pos)
        if pos - 1 >= minimo:
            candidatos.append(pos - 1)

        if not candidatos:
            return None

        return min(
            candidatos,
            key=lambda i: abs(lista[i] - objetivo_local)
        )

    def formula_serie(rs):
        return " + ".join(fmt(r) for r in rs)

    def formula_paralelo(rs):
        return " || ".join(fmt(r) for r in rs)

    n = len(valores)

    # 1. Una resistencia
    idx = cercano(valores, objetivo)
    if idx is not None:
        for i in range(max(0, idx - 2), min(n, idx + 3)):
            r = valores[i]
            guardar(r, (r,), "INDIVIDUAL", fmt(r))

    # 2. Dos resistencias en serie
    for i, a in enumerate(valores):
        if a >= objetivo:
            break
        idx = cercano(valores, objetivo - a, i)
        if idx is not None:
            for j in range(max(i, idx - 1), min(n, idx + 2)):
                b = valores[j]
                guardar(a + b, (a, b), "SERIE DUAL", formula_serie((a, b)))

    # 3. Dos resistencias en paralelo
    for ga, a in conductancias:
        restante = objetivo_g - ga
        if restante <= 0:
            continue
        idx = cercano(gs, restante)
        if idx is not None:
            for j in range(max(0, idx - 1), min(len(gs), idx + 2)):
                gb, b = conductancias[j]
                guardar(1 / (ga + gb), (a, b), "PARALELO DUAL", formula_paralelo((a, b)))

    # 4. Tres resistencias en serie
    for i, a in enumerate(valores):
        if a >= objetivo:
            break
        for j in range(i, n):
            b = valores[j]
            restante = objetivo - a - b
            if restante <= 0:
                break
            idx = cercano(valores, restante, j)
            if idx is not None:
                for k in range(max(j, idx - 1), min(n, idx + 2)):
                    c = valores[k]
                    guardar(a + b + c, (a, b, c), "SERIE TRIPLE", formula_serie((a, b, c)))

    # 5. Tres resistencias en paralelo
    for i, (ga, a) in enumerate(conductancias):
        restante1 = objetivo_g - ga
        if restante1 <= 0:
            continue
        for j in range(i, len(conductancias)):
            gb, b = conductancias[j]
            restante2 = restante1 - gb
            if restante2 <= 0:
                continue
            idx = cercano(gs, restante2, j)
            if idx is not None:
                for k in range(max(j, idx - 1), min(len(gs), idx + 2)):
                    gc, c = conductancias[k]
                    guardar(1 / (ga + gb + gc), (a, b, c), "PARALELO TRIPLE", formula_paralelo((a, b, c)))

    # 6. Serie-paralelo: R1 + (R2 || R3)
    for a in valores:
        rama = objetivo - a
        if rama <= 0:
            break
        rama_g = 1 / rama
        for gb, b in conductancias:
            restante = rama_g - gb
            if restante <= 0:
                continue
            idx = cercano(gs, restante)
            if idx is not None:
                for k in range(max(0, idx - 1), min(len(gs), idx + 2)):
                    gc, c = conductancias[k]
                    guardar(a + 1 / (gb + gc), (a, b, c), "MIXTO [SERIE + PARALELO]", f"{fmt(a)} + ({fmt(b)} || {fmt(c)})")

    # 7. Serie-paralelo: R1 || (R2 + R3)
    for ga, a in conductancias:
        restante_g = objetivo_g - ga
        if restante_g <= 0:
            continue
        rama = 1 / restante_g
        for j, b in enumerate(valores):
            restante_r = rama - b
            if restante_r <= 0:
                continue
            idx = cercano(valores, restante_r, j)
            if idx is not None:
                for k in range(max(j, idx - 1), min(n, idx + 2)):
                    c = valores[k]
                    equiv = 1 / (ga + 1 / (b + c))
                    guardar(equiv, (a, b, c), "MIXTO [PARALELO + SERIE]", f"{fmt(a)} || ({fmt(b)} + {fmt(c)})")

    return sorted(
        resultados.values(),
        key=lambda x: x["error"]
    )[:3]


# ==========================================
# INTERFAZ / HEADER
# ==========================================

st.markdown("""
<div class="cyber-header">
    <div class="cyber-badge-top">SYSTEM v2.0 // CIRCUIT SYNTHESIZER</div>
    <div class="cyber-title">SYNTH-OHM // MATRIX</div>
    <div class="cyber-subtitle">Cálculo y optimización de arreglos resistivos comerciales</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# CONTROLES DE ENTRADA
# ==========================================

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    objetivo = st.number_input(
        "RESISTENCIA OBJETIVO (Ω)",
        min_value=0.001,
        value=430.0,
        step=1.0
    )

with c2:
    tolerancia = st.selectbox(
        "SERIE DE TOLERANCIA",
        [10, 1],
        format_func=lambda x: f"Serie E{12 if x==10 else 96} ({x}%)"
    )

with c3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    buscar = st.button("⚡ PROCESAR COMBINACIONES", use_container_width=True)


# ==========================================
# RENDERIZADO DE RESULTADOS
# ==========================================

if "resultados" not in st.session_state:
    st.session_state.resultados = None

if buscar:
    with st.spinner("ANALIZANDO MATRIZ COMERCIAL..."):
        st.session_state.resultados = buscar_combinaciones(objetivo, tolerancia)
        st.session_state.objetivo = objetivo
        st.session_state.tolerancia = tolerancia

if st.session_state.resultados is not None:
    resultados = st.session_state.resultados
    serie_nombre = "E12" if st.session_state.tolerancia == 10 else "E96"

    st.markdown(
        f'<div class="results-header">// TOP 3 COMBINACIONES ÓPTIMAS — SERIE {serie_nombre} //</div>',
        unsafe_allow_html=True
    )

    if not resultados:
        st.warning("No se encontraron combinaciones en la matriz.")
    else:
        clases_posibles = ["rank-1", "rank-2", "rank-3"]
        for i, resultado in enumerate(resultados):
            clase = clases_posibles[i] if i < len(clases_posibles) else "rank-3"
            etiqueta = '<div class="best-badge">OPCIÓN ÓPTIMA</div>' if i == 0 else ""

            resistencias_html = "".join(
                dibujar_resistencia(r)
                for r in resultado["resistencias"]
            )

            tarjeta = f"""
            <div class="card {clase}">
                <div class="rank-badge">0{i + 1}</div>

                <div class="card-main">
                    {etiqueta}
                    <div class="type-tag">{resultado['tipo']}</div>
                    <div class="formula">{resultado['formula']}</div>
                    <div class="resistor-row">{resistencias_html}</div>
                </div>

                <div class="card-stats">
                    <div class="eq-val">{fmt(resultado['valor'])}</div>
                    <div class="err-tag">ERR: {resultado['error']:.4f}%</div>
                </div>
            </div>
            """

            components.html(
                f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=JetBrains+Mono:wght@500;800&display=swap');
                    
                    * {{ box-sizing: border-box; }}
                    body {{
                        margin: 0;
                        padding: 4px;
                        font-family: 'JetBrains Mono', monospace;
                        background: transparent;
                        color: #c0caf5;
                    }}

                    .card {{
                        display: flex;
                        align-items: center;
                        gap: 15px;
                        padding: 16px;
                        border-radius: 8px;
                        background: #0d131f;
                        border: 1px solid #1f2d45;
                        width: 100%;
                        position: relative;
                        overflow: hidden;
                    }}

                    /* Estilos para cada posición */
                    .rank-1 {{
                        border-color: #00f3ff;
                        box-shadow: 0 0 15px rgba(0, 243, 255, 0.15);
                    }}
                    .rank-1::before {{
                        content: "";
                        position: absolute;
                        top: 0; left: 0; width: 4px; height: 100%;
                        background: #00f3ff;
                        box-shadow: 0 0 8px #00f3ff;
                    }}

                    .rank-2 {{
                        border-color: #7000ff;
                        box-shadow: 0 0 15px rgba(112, 0, 255, 0.15);
                    }}
                    .rank-2::before {{
                        content: "";
                        position: absolute;
                        top: 0; left: 0; width: 4px; height: 100%;
                        background: #7000ff;
                    }}

                    .rank-3 {{
                        border-color: #ff007f;
                        box-shadow: 0 0 15px rgba(255, 0, 127, 0.15);
                    }}
                    .rank-3::before {{
                        content: "";
                        position: absolute;
                        top: 0; left: 0; width: 4px; height: 100%;
                        background: #ff007f;
                    }}

                    .rank-badge {{
                        font-family: 'Orbitron', sans-serif;
                        font-size: 20px;
                        font-weight: 900;
                        min-width: 45px;
                        height: 45px;
                        border-radius: 6px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        background: #141c2e;
                        color: #7a88cf;
                        border: 1px solid #283754;
                    }}

                    .rank-1 .rank-badge {{ color: #00f3ff; border-color: #00f3ff; text-shadow: 0 0 8px #00f3ff; }}
                    .rank-2 .rank-badge {{ color: #a960ff; border-color: #7000ff; }}
                    .rank-3 .rank-badge {{ color: #ff007f; border-color: #ff007f; }}

                    .card-main {{
                        flex: 1;
                        min-width: 0;
                    }}

                    .type-tag {{
                        color: #565f89;
                        font-size: 10px;
                        font-weight: 800;
                        letter-spacing: 1.5px;
                        margin-bottom: 4px;
                    }}

                    .formula {{
                        font-size: 14px;
                        font-weight: 800;
                        color: #00f3ff;
                        overflow-wrap: anywhere;
                    }}

                    .best-badge {{
                        display: inline-block;
                        background: #00f3ff;
                        color: #000;
                        border-radius: 3px;
                        padding: 2px 6px;
                        font-size: 9px;
                        font-weight: 900;
                        letter-spacing: 1px;
                        margin-bottom: 4px;
                        font-family: 'Orbitron', sans-serif;
                    }}

                    .resistor-row {{
                        display: flex;
                        flex-wrap: wrap;
                        gap: 10px;
                        margin-top: 10px;
                    }}

                    .resistor-card {{
                        width: 100px;
                        background: #080b10;
                        border: 1px solid #1a2438;
                        border-radius: 6px;
                        padding: 5px;
                        text-align: center;
                    }}

                    .wire {{
                        height: 30px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                    }}

                    .wire:before {{
                        content: "";
                        position: absolute;
                        width: 100%;
                        height: 2px;
                        background: #3b4261;
                    }}

                    .resistor-body {{
                        position: relative;
                        z-index: 1;
                        width: 65px;
                        height: 20px;
                        border: 1px solid #414868;
                        border-radius: 4px;
                        background: #1a1b26;
                        display: flex;
                        justify-content: space-evenly;
                        overflow: hidden;
                    }}

                    .band {{
                        width: 5px;
                        height: 100%;
                        flex-shrink: 0;
                    }}

                    .res-value {{
                        font-size: 11px;
                        font-weight: 800;
                        color: #c0caf5;
                        margin-top: 4px;
                    }}

                    .card-stats {{
                        min-width: 120px;
                        text-align: right;
                    }}

                    .eq-val {{
                        font-family: 'Orbitron', sans-serif;
                        font-size: 18px;
                        font-weight: 900;
                        color: #ffffff;
                    }}

                    .err-tag {{
                        display: inline-block;
                        background: rgba(0, 243, 255, 0.1);
                        border: 1px solid #00f3ff;
                        color: #00f3ff;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-size: 10px;
                        font-weight: 800;
                        margin-top: 6px;
                    }}

                    @media (max-width: 600px) {{
                        .card {{ flex-wrap: wrap; }}
                        .card-stats {{ width: 100%; text-align: left; }}
                    }}
                </style>
                </head>
                <body>{tarjeta}</body>
                </html>
                """,
                height=195,
                scrolling=False
            )


# ==========================================
# PANEL INFORMATIVO
# ==========================================

st.markdown("""
<div class="info-box-cyber">
    <h3>// DOCUMENTACIÓN DEL SISTEMA</h3>
    El motor analiza combinaciones de 1, 2 y 3 resistencias utilizando las series estandarizadas <b>E12 (10%)</b> y <b>E96 (1%)</b>.
    <br><br>
    <b>Arquitecturas soportadas:</b> Serie pura, Paralelo puro, Serie-Paralelo mixta [R1 + (R2 || R3)] y Paralelo-Serie mixta [R1 || (R2 + R3)].
</div>

<div class="footer-cyber">
    SYNTH-OHM MATRIX // HARDWARE DESIGN ENGINE
</div>
""", unsafe_allow_html=True)
