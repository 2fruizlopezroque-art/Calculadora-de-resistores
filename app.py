import streamlit.components.v1 as components
import math
import streamlit as st
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
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Calculadora de resistencias",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# DISEÑO CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500;700&display=swap');

.stApp {
    background: linear-gradient(120deg, #faf8ef, #eef6ff);
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    font-family: Arial, sans-serif;
}
.title {
    text-align: center;
    font-size: clamp(19px, 3vw, 36px);
    font-weight: 900;
    margin-bottom: 8px;
}
.letter {
    display: inline-block;
    color: white;
    padding: 3px 5px;
    margin: 1px;
}
.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 30px;
}
.stButton > button {
    background: #ff1010;
    color: white;
    border: none;
    height: 49px;
    border-radius: 12px;
    font-weight: bold;
    width: 100%;
}
.stButton > button:hover {
    background: #d90000;
    color: white;
}
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px;
}
.results-title {
    text-align: center;
    color: #168b49;
    font-size: 16px;
    font-weight: bold;
    margin: 30px 0 20px;
}
.result {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 18px;
    border-radius: 14px;
    border: 2px solid;
    margin-bottom: 12px;
    min-height: 145px;
}
.first {
    background: #fff0b6;
    border-color: #f2a000;
}
.second {
    background: #d9e4f2;
    border-color: #9ba9bc;
}
.third {
    background: #f2e8de;
    border-color: #b95000;
}
.rank {
    min-width: 43px;
    height: 43px;
    border-radius: 50%;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 17px;
}
.first .rank { background: #d99500; }
.second .rank { background: #6f7d91; }
.third .rank { background: #98430a; }
.result-main {
    flex: 1;
    min-width: 0;
}
.result-type {
    color: #566173;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
}
.formula {
    font-family: 'Roboto Mono', monospace;
    font-size: 15px;
    font-weight: bold;
    color: #171923;
    overflow-wrap: anywhere;
    margin-top: 5px;
}
.best-badge {
    display: inline-block;
    background: #d99500;
    color: white;
    border-radius: 4px;
    padding: 4px 9px;
    font-size: 10px;
    font-weight: bold;
    margin-bottom: 6px;
}
.resistor-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
}
.resistor-card {
    width: 112px;
    background: white;
    border-radius: 9px;
    padding: 7px 5px;
    text-align: center;
    box-shadow: 0 2px 5px #00000012;
}
.wire {
    position: relative;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.wire:before {
    content: "";
    position: absolute;
    width: 100%;
    height: 3px;
    background: #a0a5af;
    left: 0;
    top: 16px;
}
.resistor-body {
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
}
.band {
    height: 100%;
    width: 6px;
}
.res-value {
    font-family: 'Roboto Mono', monospace;
    font-size: 12px;
    font-weight: bold;
    margin-top: 4px;
}
.value-side {
    min-width: 130px;
    text-align: right;
    font-family: 'Roboto Mono', monospace;
}
.eq {
    font-size: 18px;
    font-weight: bold;
    color: #171923;
}
.err {
    display: inline-block;
    background: #188d48;
    color: white;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: bold;
    margin-top: 6px;
}
.info {
    background: white;
    border: 1px solid #e1e5ec;
    border-radius: 12px;
    padding: 20px;
    margin-top: 25px;
    color: #566173;
    line-height: 1.7;
}
@media (max-width: 700px) {
    .result { flex-wrap: wrap; }
    .value-side { text-align: left; width: 100%; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCIONES PARA RESISTENCIAS
# ==========================================

def fmt(r):
    if r >= 1_000_000:
        return f"{r / 1_000_000:.4g} MΩ"
    if r >= 1000:
        return f"{r / 1000:.4g} kΩ"
    if r >= 1:
        return f"{r:.4g} Ω"
    return f"{r:.4g} Ω"


def generar_valores(serie):
    valores = set()
    for exponente in range(-3, 9):
        for base in serie:
            valores.add(round(base * 10**exponente, 10))
    return sorted(valores)


def cercano(valores, objetivo, minimo=0):
    """Busca el valor comercial más próximo al objetivo."""
    if objetivo <= 0:
        return None

    pos = bisect_left(valores, objetivo, lo=minimo)
    candidatos = []

    if pos < len(valores):
        candidatos.append(pos)
    if pos > minimo:
        candidatos.append(pos - 1)

    if not candidatos:
        return None

    return min(candidatos, key=lambda i: abs(valores[i] - objetivo))


def bandas_color(valor):
    """Calcula bandas aproximadas para representar el valor."""
    colores = [
        "#111111", "#854b26", "#e53935", "#f57c00",
        "#f1c40f", "#27ae60", "#2878c8", "#7b3fa1",
        "#777777", "#ffffff"
    ]

    if valor <= 0:
        return ["#111111", "#111111", "#854b26", "#bfa46b"]

    exponente = math.floor(math.log10(valor)) - 1
    cifras = round(valor / (10**exponente))

    if cifras >= 100:
        cifras //= 10
        exponente += 1

    d1 = max(0, min(9, cifras // 10))
    d2 = max(0, min(9, cifras % 10))

    if exponente < 0:
        mult = "#bfa46b"
    elif exponente <= 9:
        mult = colores[exponente]
    else:
        mult = "#ffffff"

    # Banda de tolerancia dorada para 5%, plateada para 10%.
    return [colores[d1], colores[d2], mult, "#bfa46b"]


def dibujar_resistencia(valor):
    bandas = "".join(
        f'<span class="band" style="background:{color}"></span>'
        for color in bandas_color(valor)
    )
    return (
        '<div class="resistor-card">'
        '<div class="wire"><div class="resistor-body">'
        + bandas +
        '</div></div><div class="res-value">'
        + fmt(valor) +
        '</div></div>'
    )


# ==========================================
# BUSCAR LAS MEJORES COMBINACIONES
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

    def formula_serie(rs):
        return " + ".join(fmt(r) for r in rs)

    def formula_paralelo(rs):
        return " || ".join(fmt(r) for r in rs)

    def cercano_g(objetivo_g_local, minimo=0):
        return cercano(gs, objetivo_g_local, minimo)

    n = len(valores)

    # Una resistencia
    for a in valores:
        guardar(a, (a,), "Una resistencia", fmt(a))

    # Dos resistencias en serie
    for i, a in enumerate(valores):
        b_index = cercano(valores, objetivo - a, i)
        if b_index is not None:
            b = valores[b_index]
            guardar(a + b, (a, b), "Serie", formula_serie((a, b)))

    # Dos resistencias en paralelo
    for ga, a in conductancias:
        idx = cercano_g(objetivo_g - ga)
        if idx is not None:
            gb, b = conductancias[idx]
            guardar(1 / (ga + gb), (a, b), "Paralelo",
                    formula_paralelo((a, b)))

    # Tres resistencias en serie
    for i, a in enumerate(valores):
        for j in range(i, n):
            b = valores[j]
            idx = cercano(valores, objetivo - a - b, j)
            if idx is not None:
                c = valores[idx]
                guardar(a + b + c, (a, b, c), "Serie",
                        formula_serie((a, b, c)))

    # Tres resistencias en paralelo
    for i, (ga, a) in enumerate(conductancias):
        for gb, b in conductancias:
            idx = cercano_g(objetivo_g - ga - gb)
            if idx is not None:
                gc, c = conductancias[idx]
                guardar(1 / (ga + gb + gc), (a, b, c), "Paralelo",
                        formula_paralelo((a, b, c)))

    # Una en serie con dos en paralelo: a + (b || c)
    for a in valores:
        restante = objetivo - a
        if restante <= 0:
            continue

        g_restante = 1 / restante
        for gb, b in conductancias:
            idx = cercano_g(g_restante - gb)
            if idx is not None:
                gc, c = conductancias[idx]
                paralelo = 1 / (gb + gc)
                guardar(a + paralelo, (a, b, c), "Serie-paralelo",
                        f"{fmt(a)} + ({fmt(b)} || {fmt(c)})")

    # Una en paralelo con dos en serie: a || (b + c)
    for ga, a in conductancias:
        g_restante = objetivo_g - ga
        if g_restante <= 0:
            continue

        rama = 1 / g_restante
        for j, b in enumerate(valores):
            idx = cercano(valores, rama - b, j)
            if idx is not None:
                c = valores[idx]
                equivalente = 1 / (ga + 1 / (b + c))
                guardar(equivalente, (a, b, c), "Serie-paralelo",
                        f"{fmt(a)} || ({fmt(b)} + {fmt(c)})")

    ordenados = sorted(resultados.values(), key=lambda x: x["error"])
    return ordenados[:3]


# ==========================================
# INTERFAZ
# ==========================================

titulo = "CALCULADORA DE RESISTENCIAS"
colores_titulo = [
    "#e74c3c", "#e67e22", "#f1c40f", "#27ae60",
    "#16a085", "#3498db", "#2980b9"
]

letras = ""
for i, letra in enumerate(titulo):
    if letra == " ":
        letras += "&nbsp;"
    else:
        color = colores_titulo[i % len(colores_titulo)]
        letras += (
            f'<span class="letter" style="background:{color}">'
            f'{letra}</span>'
        )

st.markdown(
    f'<div class="title">{letras}</div>'
    '<div class="subtitle">⚡ Encuentra la combinación más cercana '
    'con resistencias comerciales :D</div>',
    unsafe_allow_html=True
)

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
        "TOLERANCIA DESEADA (%)",
        [10, 1],
        format_func=lambda x: f"{x}%"
    )

with c3:
    st.markdown("<div style='height:27px'></div>",
                unsafe_allow_html=True)
    buscar = st.button("🔎 Buscar combinaciones",
                       use_container_width=True)

if "resultados" not in st.session_state:
    st.session_state.resultados = None

if buscar:
    with st.spinner("Buscando las mejores combinaciones..."):
        st.session_state.resultados = buscar_combinaciones(
            objetivo, tolerancia
        )
        st.session_state.objetivo = objetivo
        st.session_state.tolerancia = tolerancia

if st.session_state.resultados is not None:
    resultados = st.session_state.resultados
    serie_nombre = (
        "E12" if st.session_state.tolerancia == 10 else "E96"
    )

    st.markdown(
        f'<div class="results-title">✅ TOP 3 DE LAS MEJORES '
        f'COMBINACIONES · SERIE {serie_nombre}</div>',
        unsafe_allow_html=True
    )

    if not resultados:
        st.warning("No se encontraron combinaciones.")
    else:
        for i, resultado in enumerate(resultados):
            clase = ["first", "second", "third"][i]
            etiqueta = (
                '<div class="best-badge">MEJOR OPCIÓN</div>'
                if i == 0 else ""
            )

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
                        font-family: Arial, sans-serif;
                        background: transparent;
                    }}
                    .result {{
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        padding: 14px;
                        border-radius: 14px;
                        border: 2px solid;
                        min-height: 150px;
                        width: 100%;
                    }}
                    .first {{
                        background: #fff0b6;
                        border-color: #f2a000;
                    }}
                    .second {{
                        background: #d9e4f2;
                        border-color: #9ba9bc;
                    }}
                    .third {{
                        background: #f2e8de;
                        border-color: #b95000;
                    }}
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
                    .first .rank {{ background: #d99500; }}
                    .second .rank {{ background: #6f7d91; }}
                    .third .rank {{ background: #98430a; }}
                    .result-main {{
                        flex: 1;
                        min-width: 0;
                    }}
                    .result-type {{
                        color: #566173;
                        font-size: 11px;
                        font-weight: bold;
                        text-transform: uppercase;
                        margin-bottom: 5px;
                    }}
                    .formula {{
                        font-family: monospace;
                        font-size: 14px;
                        font-weight: bold;
                        overflow-wrap: anywhere;
                    }}
                    .best-badge {{
                        display: inline-block;
                        background: #d99500;
                        color: white;
                        border-radius: 4px;
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
                        font-family: monospace;
                        font-size: 12px;
                        font-weight: bold;
                        margin-top: 4px;
                    }}
                    .value-side {{
                        min-width: 115px;
                        text-align: right;
                        font-family: monospace;
                    }}
                    .eq {{
                        font-size: 17px;
                        font-weight: bold;
                        overflow-wrap: anywhere;
                    }}
                    .err {{
                        display: inline-block;
                        background: #188d48;
                        color: white;
                        border-radius: 6px;
                        padding: 5px 7px;
                        font-size: 11px;
                        font-weight: bold;
                        margin-top: 6px;
                    }}
                    @media (max-width: 600px) {{
                        .result {{ flex-wrap: wrap; }}
                        .value-side {{
                            width: 100%;
                            text-align: left;
                        }}
                    }}
                </style>
                </head>
                <body>
                    {tarjeta}
                </body>
                </html>
                """,
                height=205,
                scrolling=False
            )

st.markdown("""
<div class="info">
    <h3>¿Cómo funciona?</h3>
    El programa recibe una resistencia deseada y una tolerancia comercial.
    Para 10% usa la serie E12; para 1% usa E96.
    <br><br>
    Prueba combinaciones de una, dos y tres resistencias conectadas en
    serie, en paralelo y en configuraciones mixtas serie-paralelo.
    Después ordena los resultados por el error porcentual y muestra
    las tres combinaciones más cercanas al valor solicitado.
    <br><br>
    <b>Fórmulas utilizadas:</b><br>
    Serie: R = R₁ + R₂ + R₃<br>
    Paralelo: 1/R = 1/R₁ + 1/R₂ + 1/R₃
</div>
""", unsafe_allow_html=True)
