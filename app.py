import math
import streamlit as st
import streamlit.components.v1 as components
from bisect import bisect_left

# ==========================================
# SERIES COMERCIALES
# ==========================================

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
       3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

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
# CONFIGURACIÓN DE STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Calculadora de resistencias",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# ESTILOS DE LA INTERFAZ
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f3f5fa, #e9edf5);
    color: #252840;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label, div, span {
    font-family: 'DM Sans', sans-serif;
}

.title {
    text-align: center;
    font-size: clamp(19px, 3vw, 36px);
    font-weight: 900;
    margin-bottom: 8px;
    line-height: 1.5;
}

.letter {
    display: inline-block;
    color: white;
    padding: 3px 5px;
    margin: 1px;
    border-radius: 4px;
}

.subtitle {
    text-align: center;
    color: #68718a;
    margin-bottom: 30px;
    font-size: 15px;
}

.stButton > button {
    background: linear-gradient(135deg, #635bdb, #4942b8);
    color: white;
    border: none;
    height: 49px;
    border-radius: 12px;
    font-weight: 800;
    width: 100%;
    box-shadow: 0 5px 14px rgba(80, 72, 190, 0.22);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5149c6, #38319f);
    color: white;
    transform: translateY(-2px);
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px;
    border-color: #c9cfdf;
}

.results-title {
    text-align: center;
    color: #4942b8;
    font-size: 16px;
    font-weight: 800;
    margin: 30px 0 20px;
}

.info-box {
    background: white;
    border: 1px solid #dfe4ef;
    border-radius: 15px;
    padding: 22px;
    margin-top: 28px;
    color: #59647b;
    line-height: 1.7;
    box-shadow: 0 4px 16px rgba(36, 48, 90, .04);
}

.info-box h3 {
    color: #4942b8;
    margin-top: 0;
}

.footer {
    color: #8a91a5;
    text-align: center;
    font-size: 12px;
    padding-top: 24px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FORMATO DE RESISTENCIAS
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
# BÚSQUEDA DE COMBINACIONES
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
            guardar(r, (r,), "Una resistencia", fmt(r))

    # Dos resistencias en serie
    for i, a in enumerate(valores):
        if a >= objetivo:
            break
        idx = cercano(valores, objetivo - a, i)
        if idx is not None:
            for j in range(max(i, idx - 1), min(n, idx + 2)):
                b = valores[j]
                guardar(a + b, (a, b), "Serie", formula_serie((a, b)))

    # Dos resistencias en paralelo
    for ga, a in conductancias:
        restante = objetivo_g - ga
        if restante <= 0:
            continue
        idx = cercano(gs, restante)
        if idx is not None:
            for j in range(max(0, idx - 1), min(len(gs), idx + 2)):
                gb, b = conductancias[j]
                guardar(1 / (ga + gb), (a, b), "Paralelo", formula_paralelo((a, b)))

    # Tres resistencias en serie
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

    # Tres resistencias en paralelo
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

    # Una en serie con dos en paralelo: R1 + (R2 || R3)
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
                    guardar(a + 1 / (gb + gc), (a, b, c), "Serie-paralelo", f"{fmt(a)} + ({fmt(b)} || {fmt(c)})")

    # Una en paralelo con dos en serie: R1 || (R2 + R3)
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
                    guardar(equiv, (a, b, c), "Serie-paralelo", f"{fmt(a)} || ({fmt(b)} + {fmt(c)})")

    return sorted(
        resultados.values(),
        key=lambda x: x["error"]
    )[:3]


# ==========================================
# TÍTULO
# ==========================================

titulo = "CALCULADORA DE RESISTENCIAS"
colores_titulo = [
    "#635bdb", "#4942b8", "#318fbb", "#319688",
    "#746be8", "#3c6fba", "#4b56a8"
]
letras = ""

for i, letra in enumerate(titulo):
    if letra == " ":
        letras += "&nbsp;"
    else:
        color = colores_titulo[i % len(colores_titulo)]
        letras += f'<span class="letter" style="background:{color}">{letra}</span>'

st.markdown(
    f'<div class="title">{letras}</div>'
    '<div class="subtitle">⚡ Herramienta de análisis de circuitos · Encuentra tu combinación ideal</div>',
    unsafe_allow_html=True
)

# ==========================================
# DATOS DE ENTRADA
# ==========================================

c1, c2, c3 = st.columns([1, 1, 1.35])

with c1:
    objetivo = st.number_input(
        "VALOR DESEADO (Ω)",
        min_value=0.001,
        value=430.0,
        step=1.0
    )

with c2:
    tolerancia = st.selectbox(
        "TOLERANCIA DESEADA",
        [10, 1],
        format_func=lambda x: f"{x}%"
    )

with c3:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    buscar = st.button("⚡ Buscar combinaciones", use_container_width=True)


# ==========================================
# RESULTADOS
# ==========================================

if "resultados" not in st.session_state:
    st.session_state.resultados = None

if buscar:
    with st.spinner("Buscando las mejores combinaciones..."):
        st.session_state.resultados = buscar_combinaciones(objetivo, tolerancia)
        st.session_state.objetivo = objetivo
        st.session_state.tolerancia = tolerancia

if st.session_state.resultados is not None:
    resultados = st.session_state.resultados
    serie_nombre = "E12" if st.session_state.tolerancia == 10 else "E96"

    st.markdown(
        f'<div class="results-title">✦ TOP 3 DE LAS MEJORES COMBINACIONES · SERIE {serie_nombre}</div>',
        unsafe_allow_html=True
    )

    if not resultados:
        st.warning("No se encontraron combinaciones.")
    else:
        clases_posibles = ["first", "second", "third"]
        for i, resultado in enumerate(resultados):
            clase = clases_posibles[i] if i < len(clases_posibles) else "third"
            etiqueta = '<div class="best-badge">MEJOR OPCIÓN</div>' if i == 0 else ""

            resistencias_html = "".join(
                dibujar_resistencia(r)
                for r in resultado["resistencias"]
            )

            tarjeta = f"""
            <div class="result {clase}">
                <div class="rank">#{i + 1}</div>
                <div class="result-main">
                    {etiqueta}
                    <div class="result-type">{resultado['tipo']}</div>
                    <div class="formula">{resultado['formula']}</div>
                    <div class="resistor-row">{resistencias_html}</div>
                </div>
                <div class="value-side">
                    <div class="eq">{fmt(resultado['valor'])}</div>
                    <div class="err">Error: {resultado['error']:.4f}%</div>
                </div>
            </div>
            """

            components.html(
                f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    * {{ box-sizing: border-box; }}
                    body {{
                        margin: 0;
                        padding: 3px 0;
                        font-family: 'DM Sans', Arial, sans-serif;
                        background: transparent;
                        color: #252840;
                    }}
                    .result {{
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        padding: 14px;
                        border-radius: 15px;
                        border: 2px solid;
                        min-height: 150px;
                        width: 100%;
                    }}
                    .first {{ background: #eeecff; border-color: #756be8; }}
                    .second {{ background: #e3f4f1; border-color: #59a99c; }}
                    .third {{ background: #fff0e4; border-color: #e7a16b; }}
                    .rank {{
                        min-width: 42px;
                        height: 42px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                    }}
                    .first .rank {{ background: #635bdb; }}
                    .second .rank {{ background: #319688; }}
                    .third .rank {{ background: #d58243; }}
                    .result-main {{ flex: 1; min-width: 0; }}
                    .result-type {{
                        color: #68718a;
                        font-size: 11px;
                        font-weight: bold;
                        text-transform: uppercase;
                        letter-spacing: .7px;
                        margin-bottom: 5px;
                    }}
                    .formula {{
                        font-family: 'Space Mono', monospace;
                        font-size: 14px;
                        font-weight: bold;
                        overflow-wrap: anywhere;
                        color: #252840;
                    }}
                    .best-badge {{
                        display: inline-block;
                        background: #635bdb;
                        color: white;
                        border-radius: 5px;
                        padding: 4px 8px;
                        font-size: 10px;
                        font-weight: bold;
                        margin-bottom: 5px;
                    }}
                    .resistor-row {{
                        display: flex;
                        flex-wrap: wrap;
                        gap: 8px;
                        margin-top: 10px;
                    }}
                    .resistor-card {{
                        width: 105px;
                        background: white;
                        border: 1px solid #e0e5ef;
                        border-radius: 8px;
                        padding: 6px;
                        text-align: center;
                    }}
                    .wire {{
                        height: 35px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                    }}
                    .wire:before {{
                        content: "";
                        position: absolute;
                        width: 100%;
                        height: 3px;
                        background: #a0a5af;
                    }}
                    .resistor-body {{
                        position: relative;
                        z-index: 1;
                        width: 70px;
                        height: 24px;
                        border: 1px solid #b5a47f;
                        border-radius: 5px;
                        background: #ead7ae;
                        display: flex;
                        justify-content: space-evenly;
                        overflow: hidden;
                    }}
                    .band {{
                        width: 6px;
                        height: 100%;
                        flex-shrink: 0;
                    }}
                    .res-value {{
                        font-family: 'Space Mono', monospace;
                        font-size: 12px;
                        font-weight: bold;
                        margin-top: 4px;
                    }}
                    .value-side {{
                        min-width: 115px;
                        text-align: right;
                        font-family: 'Space Mono', monospace;
                    }}
                    .eq {{
                        font-size: 17px;
                        font-weight: bold;
                        overflow-wrap: anywhere;
                        color: #252840;
                    }}
                    .err {{
                        display: inline-block;
                        background: #188d65;
                        color: white;
                        border-radius: 6px;
                        padding: 5px 7px;
                        font-size: 11px;
                        font-weight: bold;
                        margin-top: 6px;
                    }}
                    @media (max-width: 600px) {{
                        .result {{ flex-wrap: wrap; }}
                        .value-side {{ width: 100%; text-align: left; }}
                    }}
                </style>
                </head>
                <body>{tarjeta}</body>
                </html>
                """,
                height=205,
                scrolling=False
            )


# ==========================================
# INFORMACIÓN
# ==========================================

st.markdown("""
<div class="info-box">
    <h3>⚙ ¿Cómo funciona?</h3>
    Introduce el valor de resistencia deseado y selecciona una tolerancia.
    El programa utiliza la serie comercial E12 para 10% y E96 para 1%.
    <br><br>
    Busca combinaciones de una, dos y tres resistencias conectadas en
    serie, paralelo y las dos configuraciones mixtas serie-paralelo.
    Después ordena los resultados por su error porcentual y muestra
    las tres opciones encontradas más cercanas al valor solicitado.
    <br><br>
    <b>Fórmulas utilizadas</b><br>
    Serie: R = R₁ + R₂ + R₃<br>
    Paralelo: 1/R = 1/R₁ + 1/R₂ + 1/R₃
</div>
<div class="footer">
    CALCULADORA DE RESISTENCIAS · PYTHON + STREAMLIT
</div>
""", unsafe_allow_html=True)
