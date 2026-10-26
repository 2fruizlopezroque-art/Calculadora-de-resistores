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
    page_title="OhmMinimal",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# ESTILOS MINIMALISTAS (NEGRO / MORADO SUTIL)
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Fondo negro absoluto y limpio */
.stApp {
    background-color: #050507;
    color: #e2e8f0;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, p, label, div, span {
    font-family: 'Inter', sans-serif;
}

/* Header Minimalista */
.minimal-header {
    text-align: left;
    border-bottom: 1px solid #141419;
    padding-bottom: 20px;
    margin-bottom: 30px;
}

.minimal-title {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin: 0;
}

.minimal-subtitle {
    font-size: 13px;
    color: #71717a;
    margin-top: 4px;
}

/* Contenedor de Inputs Estilizados */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #0b0b0f !important;
    border: 1px solid #1f1f2e !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
}

div[data-baseweb="input"] input {
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace;
}

/* Botón Minimalista con toque morado sutil */
.stButton > button {
    background-color: #12121c;
    color: #c4b5fd;
    border: 1px solid #3b287a;
    height: 44px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    width: 100%;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #1a152d;
    color: #ffffff;
    border-color: #7c3aed;
}

/* Sección de Resultados */
.section-title {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #71717a;
    margin: 40px 0 20px 0;
    font-weight: 600;
}

/* Footer Minimal */
.minimal-footer {
    border-top: 1px solid #141419;
    color: #52525b;
    text-align: center;
    font-size: 11px;
    padding-top: 24px;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# UTILIDADES Y MATEMÁTICAS
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
# MOTOR DE BÚSQUEDA
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

    # Una resistencia
    idx = cercano(valores, objetivo)
    if idx is not None:
        for i in range(max(0, idx - 2), min(n, idx + 3)):
            r = valores[i]
            guardar(r, (r,), "Simple", fmt(r))

    # Dos en serie
    for i, a in enumerate(valores):
        if a >= objetivo:
            break
        idx = cercano(valores, objetivo - a, i)
        if idx is not None:
            for j in range(max(i, idx - 1), min(n, idx + 2)):
                b = valores[j]
                guardar(a + b, (a, b), "Serie", formula_serie((a, b)))

    # Dos en paralelo
    for ga, a in conductancias:
        restante = objetivo_g - ga
        if restante <= 0:
            continue
        idx = cercano(gs, restante)
        if idx is not None:
            for j in range(max(0, idx - 1), min(len(gs), idx + 2)):
                gb, b = conductancias[j]
                guardar(1 / (ga + gb), (a, b), "Paralelo", formula_paralelo((a, b)))

    # Tres en serie
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
                    guardar(a + b + c, (a, b, c), "Serie", formula_serie((a, b, c)))

    # Tres en paralelo
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
                    guardar(1 / (ga + gb + gc), (a, b, c), "Paralelo", formula_paralelo((a, b, c)))

    # Mixto 1: R1 + (R2 || R3)
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
                    guardar(a + 1 / (gb + gc), (a, b, c), "Mixto", f"{fmt(a)} + ({fmt(b)} || {fmt(c)})")

    # Mixto 2: R1 || (R2 + R3)
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
                    guardar(equiv, (a, b, c), "Mixto", f"{fmt(a)} || ({fmt(b)} + {fmt(c)})")

    return sorted(
        resultados.values(),
        key=lambda x: x["error"]
    )[:3]


# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================

st.markdown("""
<div class="minimal-header">
    <div class="minimal-title">OhmMatcher</div>
    <div class="minimal-subtitle">Calculadora analítica de arreglos de resistencias</div>
</div>
""", unsafe_allow_html=True)

# Controles de entrada compactos
col1, col2, col3 = st.columns([1, 1, 1.2])

with col1:
    objetivo = st.number_input(
        "Valor deseado (Ω)",
        min_value=0.001,
        value=430.0,
        step=1.0
    )

with col2:
    tolerancia = st.selectbox(
        "Tolerancia",
        [10, 1],
        format_func=lambda x: f"Serie E{12 if x==10 else 96} ({x}%)"
    )

with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    buscar = st.button("Buscar combinaciones", use_container_width=True)


# ==========================================
# RESULTADOS
# ==========================================

if "resultados" not in st.session_state:
    st.session_state.resultados = None

if buscar:
    with st.spinner("Procesando combinaciones..."):
        st.session_state.resultados = buscar_combinaciones(objetivo, tolerancia)
        st.session_state.objetivo = objetivo
        st.session_state.tolerancia = tolerancia

if st.session_state.resultados is not None:
    resultados = st.session_state.resultados
    serie_nombre = "E12" if st.session_state.tolerancia == 10 else "E96"

    st.markdown(f'<div class="section-title">Mejores alternativas óptimas (Serie {serie_nombre})</div>', unsafe_allow_html=True)

    if not resultados:
        st.warning("No se encontraron combinaciones.")
    else:
        for i, resultado in enumerate(resultados):
            etiqueta_badge = '<div class="badge-optimo">ÓPTIMO</div>' if i == 0 else f'<div class="badge-num">0{i+1}</div>'
            resistencias_html = "".join(
                dibujar_resistencia(r)
                for r in resultado["resistencias"]
            )

            tarjeta = f"""
            <div class="result-card">
                <div class="card-header-row">
                    <div class="meta-info">
                        {etiqueta_badge}
                        <span class="type-label">{resultado['tipo']}</span>
                    </div>
                    <div class="error-badge">Error: {resultado['error']:.3f}%</div>
                </div>

                <div class="formula-display">{resultado['formula']}</div>

                <div class="bottom-split">
                    <div class="resistors-container">{resistencias_html}</div>
                    <div class="equivalent-value">{fmt(resultado['valor'])}</div>
                </div>
            </div>
            """

            components.html(
                f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
                    * {{ box-sizing: border-box; }}
                    body {{
                        margin: 0;
                        padding: 4px 0;
                        font-family: 'Inter', sans-serif;
                        background: transparent;
                        color: #f1f5f9;
                    }}

                    .result-card {{
                        background: #09090e;
                        border: 1px solid #1c1c2b;
                        border-radius: 12px;
                        padding: 16px 20px;
                        width: 100%;
                        position: relative;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                        transition: border-color 0.2s ease;
                    }}

                    .result-card:hover {{
                        border-color: #5b21b6;
                    }}

                    .card-header-row {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 10px;
                    }}

                    .meta-info {{
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }}

                    .badge-optimo {{
                        background: #2e1065;
                        color: #c4b5fd;
                        border: 1px solid #7c3aed;
                        font-size: 10px;
                        font-weight: 700;
                        padding: 2px 8px;
                        border-radius: 4px;
                        letter-spacing: 0.5px;
                    }}

                    .badge-num {{
                        background: #14141f;
                        color: #71717a;
                        font-size: 10px;
                        font-weight: 700;
                        padding: 2px 8px;
                        border-radius: 4px;
                    }}

                    .type-label {{
                        font-size: 11px;
                        font-weight: 600;
                        color: #71717a;
                        text-transform: uppercase;
                        letter-spacing: 0.8px;
                    }}

                    .error-badge {{
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 11px;
                        color: #34d399;
                        background: rgba(52, 211, 153, 0.08);
                        padding: 3px 8px;
                        border-radius: 4px;
                        border: 1px solid rgba(52, 211, 153, 0.15);
                    }}

                    .formula-display {{
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 15px;
                        font-weight: 600;
                        color: #ffffff;
                        margin-bottom: 16px;
                    }}

                    .bottom-split {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        border-top: 1px solid #14141f;
                        padding-top: 12px;
                    }}

                    .resistors-container {{
                        display: flex;
                        gap: 10px;
                        flex-wrap: wrap;
                    }}

                    .resistor-card {{
                        background: #050508;
                        border: 1px solid #181824;
                        border-radius: 6px;
                        padding: 4px 8px;
                        width: 95px;
                        text-align: center;
                    }}

                    .wire {{
                        height: 28px;
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
                        background: #272738;
                    }}

                    .resistor-body {{
                        position: relative;
                        z-index: 1;
                        width: 58px;
                        height: 18px;
                        border: 1px solid #3f3f50;
                        border-radius: 3px;
                        background: #13131b;
                        display: flex;
                        justify-content: space-evenly;
                        overflow: hidden;
                    }}

                    .band {{
                        width: 4px;
                        height: 100%;
                        flex-shrink: 0;
                    }}

                    .res-value {{
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 10px;
                        color: #a1a1aa;
                        margin-top: 2px;
                    }}

                    .equivalent-value {{
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 20px;
                        font-weight: 700;
                        color: #ffffff;
                        text-align: right;
                    }}

                    @media (max-width: 600px) {{
                        .bottom-split {{ flex-direction: column; align-items: flex-start; gap: 10px; }}
                        .equivalent-value {{ text-align: left; }}
                    }}
                </style>
                </head>
                <body>{tarjeta}</body>
                </html>
                """,
                height=185,
                scrolling=False
            )

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="minimal-footer">
    Calculadora de Resistencias
</div>
""", unsafe_allow_html=True)
