
import math
from bisect import bisect_left
from html import escape

import streamlit as st

# ============================================================
# SERIES COMERCIALES
# 10% -> E12
# 1%  -> E96
# ============================================================

E12 = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]

E96 = [
    100, 102, 105, 107, 110, 113, 115, 118, 121, 124,
    127, 130, 133, 137, 140, 143, 147, 150, 154, 158,
    162, 165, 169, 174, 178, 182, 187, 191, 196, 200,
    205, 210, 215, 221, 226, 232, 237, 243, 249, 255,
    261, 267, 274, 280, 287, 294, 301, 309, 316, 324,
    332, 340, 348, 357, 365, 374, 383, 392, 402, 412,
    422, 432, 442, 453, 464, 475, 487, 499, 511, 523,
    536, 549, 562, 576, 590, 604, 619, 634, 649, 665,
    681, 698, 715, 732, 750, 768, 787, 806, 825, 845,
    866, 887, 909, 931, 953, 976
]

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================

st.set_page_config(
    page_title="Calculadora de Resistencias",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS - DISEÑO
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Roboto+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255, 214, 0, .08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(0, 180, 255, .08), transparent 25%),
        #f6f7fb;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Título */
.title-box {
    text-align: center;
    margin-bottom: 5px;
}

.title {
    display: inline-block;
    font-size: 35px;
    font-weight: 800;
    letter-spacing: 5px;
    line-height: 1;
}

.title span {
    display: inline-block;
    color: white;
    padding: 2px 7px;
    margin: 1px;
    border-radius: 1px;
}

.title span:nth-child(4n+1) { background:#e74c3c; }
.title span:nth-child(4n+2) { background:#f39c12; }
.title span:nth-child(4n+3) { background:#f1c40f; color:#fff; }
.title span:nth-child(4n+4) { background:#27ae60; }

.subtitle {
    color:#657080;
    font-size:15px;
    margin-top:8px;
}

.subtitle b {
    color:#e74c3c;
}

/* Inputs */
label {
    color:#536071 !important;
    font-weight:700 !important;
}

div[data-baseweb="input"] {
    border-radius:11px !important;
    border:1.5px solid #252936 !important;
    background:white !important;
}

div[data-baseweb="select"] > div {
    border-radius:11px !important;
    border:1.5px solid #252936 !important;
    background:white !important;
}

.stButton > button {
    width:100%;
    height:52px;
    border-radius:12px;
    border:0;
    background:linear-gradient(90deg,#ff1010,#ff2020);
    color:white;
    font-size:17px;
    font-weight:800;
    box-shadow:0 6px 16px rgba(255,0,0,.18);
}

.stButton > button:hover {
    background:linear-gradient(90deg,#e60000,#ff1717);
    transform:translateY(-1px);
}

/* Separador */
.results-header {
    text-align:center;
    margin:26px 0 20px;
    font-size:17px;
    color:#159447;
    font-weight:800;
}

/* Tarjetas de resultados */
.result-card {
    border-radius:16px;
    padding:18px 18px 17px;
    margin:12px 0;
    border:2px solid #d5d9e1;
    box-shadow:0 3px 10px rgba(0,0,0,.06);
}

.result-card.best {
    background:#fff1b8;
    border-color:#f0a000;
}

.result-card.second {
    background:#dce7f5;
    border-color:#9ba8bb;
}

.result-card.third {
    background:#f2e9df;
    border-color:#c55a00;
}

.rank {
    width:42px;
    height:42px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
    font-weight:800;
    color:white;
    margin-right:12px;
}

.best .rank { background:#d99500; }
.second .rank { background:#6f7d91; }
.third .rank { background:#9c4207; }

.type-label {
    font-family:'Roboto Mono', monospace;
    font-size:12px;
    font-weight:700;
    color:#596273;
    text-transform:uppercase;
    letter-spacing:.5px;
}

.formula {
    font-family:'Roboto Mono', monospace;
    font-size:18px;
    font-weight:700;
    color:#101318;
    margin-top:3px;
}

.badge {
    display:inline-block;
    color:white;
    padding:4px 10px;
    border-radius:5px;
    font-size:11px;
    font-weight:800;
    margin-bottom:5px;
}

.best .badge { background:#d99500; }

.value-box {
    text-align:right;
    font-family:'Roboto Mono', monospace;
}

.eq-value {
    font-size:20px;
    font-weight:800;
    color:#111;
}

.error {
    display:inline-block;
    background:#159447;
    color:white;
    padding:5px 10px;
    border-radius:6px;
    font-size:13px;
    font-weight:800;
    margin-top:5px;
}

.outside {
    background:#d9534f;
}

.resistor-card {
    background:white;
    border-radius:10px;
    padding:8px 10px 7px;
    min-width:118px;
    text-align:center;
    box-shadow:0 2px 5px rgba(0,0,0,.07);
}

.resistor-value {
    font-family:'Roboto Mono', monospace;
    font-size:14px;
    font-weight:700;
    margin-top:3px;
}

.resistors-row {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin-top:14px;
}

/* Información */
.info-box {
    background:white;
    border:1px solid #e0e4eb;
    border-radius:14px;
    padding:18px 22px;
    margin-top:24px;
}

.info-title {
    font-size:19px;
    font-weight:800;
    color:#283142;
}

.info-text {
    color:#626d7d;
    font-size:14px;
    line-height:1.6;
}

.footer {
    text-align:center;
    color:#9aa1ad;
    margin-top:25px;
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES DE APOYO
# ============================================================

def format_resistance(value):
    """Convierte ohms a una representación cómoda."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.3g} MΩ"
    if value >= 1_000:
        return f"{value / 1_000:.3g} kΩ"
    if value >= 1:
        return f"{value:.3g} Ω"
    if value >= 0.001:
        return f"{value * 1000:.3g} mΩ"
    return f"{value:.3g} Ω"


def commercial_values(series):
    """
    Genera los valores comerciales de la serie elegida.
    Se cubre un rango amplio para que el cálculo funcione
    tanto con resistencias pequeñas como grandes.
    """
    values = set()

    if series == E12:
        # 1.0, 1.2, ... 8.2 x 10^n
        for exponent in range(-3, 9):
            for base in series:
                values.add((base / 10) * (10 ** exponent))
    else:
        # 1.00, 1.02, ... 9.76 x 10^n
        for exponent in range(-3, 9):
            for base in series:
                values.add((base / 100) * (10 ** exponent))

    return sorted(values)


def resistor_svg(value, tolerance):
    """
    Dibuja una resistencia con SVG y bandas de colores.
    No depende de imágenes externas.
    """
    colors = {
        0: "#111111",
        1: "#8B4513",
        2: "#E53935",
        3: "#F57C00",
        4: "#F1C40F",
        5: "#2EAD63",
        6: "#2878C8",
        7: "#7B3FA1",
        8: "#777777",
        9: "#F4F4F4",
        -1: "#D4AF37",   # dorado
        -2: "#BFC3C7"    # plateado
    }

    # Determinar dos cifras significativas y multiplicador.
    if value <= 0:
        value = 1

    exponent = math.floor(math.log10(value)) - 1
    digits = int(round(value / (10 ** exponent)))

    if digits >= 100:
        digits //= 10
        exponent += 1

    d1 = digits // 10
    d2 = digits % 10

    if exponent < -2:
        multiplier_color = colors[-2]
    elif exponent == -1:
        multiplier_color = colors[-1]
    elif exponent <= 9:
        multiplier_color = colors[exponent]
    else:
        multiplier_color = colors[9]

    tolerance_color = "#8B4513" if tolerance == 1 else "#BFC3C7"

    svg = f"""
    <svg width="108" height="45" viewBox="0 0 108 45"
         xmlns="http://www.w3.org/2000/svg">
        <line x1="3" y1="22" x2="25" y2="22"
              stroke="#9aa1ad" stroke-width="3"/>
        <line x1="83" y1="22" x2="105" y2="22"
              stroke="#9aa1ad" stroke-width="3"/>

        <rect x="25" y="10" width="58" height="24" rx="5"
              fill="#ead7ae" stroke="#b6a47d" stroke-width="1"/>

        <rect x="35" y="10" width="7" height="24" fill="{colors[d1]}"/>
        <rect x="48" y="10" width="7" height="24" fill="{colors[d2]}"/>
        <rect x="61" y="10" width="7" height="24" fill="{multiplier_color}"/>
        <rect x="75" y="10" width="5" height="24" fill="{tolerance_color}"/>
    </svg>
    """

    return svg


def resistor_card(value, tolerance):
    return f"""
    <div class="resistor-card">
        {resistor_svg(value, tolerance)}
        <div class="resistor-value">{escape(format_resistance(value))}</div>
    </div>
    """


def add_result(results, equivalent, target, topology, resistors, formula):
    """Guarda un resultado evitando duplicados."""
    if equivalent <= 0:
        return

    error = abs(equivalent - target) / target * 100

    # Ordenar resistencias para identificar combinaciones repetidas.
    key = (
        topology,
        tuple(round(r, 12) for r in sorted(resistors))
    )

    if key not in results or error < results[key]["error"]:
        results[key] = {
            "error": error,
            "equivalent": equivalent,
            "topology": topology,
            "resistors": tuple(sorted(resistors)),
            "formula": formula
        }


def nearby_indices(sorted_values, target, minimum_index=0, amount=3):
    """
    Devuelve algunos valores cercanos al objetivo.
    Esto evita tener que recorrer millones de combinaciones
    sin perder las mejores soluciones.
    """
    if target <= 0:
        return []

    pos = bisect_left(sorted_values, target, lo=minimum_index)

    start = max(minimum_index, pos - amount)
    end = min(len(sorted_values), pos + amount + 1)

    return range(start, end)


def find_best_combinations(target, tolerance):
    """
    Busca las mejores combinaciones usando:
      - 1 resistencia
      - 2 resistencias: serie y paralelo
      - 3 resistencias:
          * las 3 en serie
          * las 3 en paralelo
          * 1 en serie con 2 en paralelo
          * 1 en paralelo con 2 en serie
    """

    series = E12 if tolerance == 10 else E96
    values = commercial_values(series)

    # Conductancias ordenadas.
    conductance_pairs = sorted((1 / r, r) for r in values)
    conductances = [x[0] for x in conductance_pairs]

    results = {}

    # --------------------------------------------------------
    # 1 RESISTENCIA
    # --------------------------------------------------------
    for i in nearby_indices(values, target):
        r = values[i]
        add_result(
            results,
            r,
            target,
            "Una resistencia",
            (r,),
            f"{format_resistance(r)}"
        )

    # --------------------------------------------------------
    # 2 RESISTENCIAS EN SERIE
    # --------------------------------------------------------
    for i, a in enumerate(values):
        remaining = target - a

        if remaining <= 0:
            break

        for j in nearby_indices(values, remaining, i):
            b = values[j]

            add_result(
                results,
                a + b,
                target,
                "Serie",
                (a, b),
                f"{format_resistance(a)} + {format_resistance(b)}"
            )

    # --------------------------------------------------------
    # 2 RESISTENCIAS EN PARALELO
    # --------------------------------------------------------
    target_g = 1 / target

    for ga, a in conductance_pairs:
        remaining_g = target_g - ga

        if remaining_g <= 0:
            continue

        for j in nearby_indices(conductances, remaining_g):
            gb, b = conductance_pairs[j]
            equivalent = 1 / (ga + gb)

            add_result(
                results,
                equivalent,
                target,
                "Paralelo",
                (a, b),
                f"{format_resistance(a)} || {format_resistance(b)}"
            )

    # --------------------------------------------------------
    # 3 RESISTENCIAS EN SERIE
    # --------------------------------------------------------
    for i, a in enumerate(values):
        remaining = target - a

        if remaining <= 0:
            break

        for j in nearby_indices(values, remaining, i):
            b = values[j]
            remaining2 = remaining - b

            if remaining2 <= 0:
                continue

            for k in nearby_indices(values, remaining2, j):
                c = values[k]

                add_result(
                    results,
                    a + b + c,
                    target,
                    "Serie",
                    (a, b, c),
                    f"{format_resistance(a)} + "
                    f"{format_resistance(b)} + "
                    f"{format_resistance(c)}"
                )

    # --------------------------------------------------------
    # 3 RESISTENCIAS EN PARALELO
    # --------------------------------------------------------
    for ga, a in conductance_pairs:
        remaining_g = target_g - ga

        if remaining_g <= 0:
            continue

        for j in nearby_indices(conductances, remaining_g):
            gb, b = conductance_pairs[j]
            remaining_g2 = remaining_g - gb

            if remaining_g2 <= 0:
                continue

            for k in nearby_indices(conductances, remaining_g2):
                gc, c = conductance_pairs[k]
                equivalent = 1 / (ga + gb + gc)

                add_result(
                    results,
                    equivalent,
                    target,
                    "Paralelo",
                    (a, b, c),
                    f"{format_resistance(a)} || "
                    f"{format_resistance(b)} || "
                    f"{format_resistance(c)}"
                )

    # --------------------------------------------------------
    # 3 RESISTENCIAS:
    # R1 + (R2 || R3)
    # --------------------------------------------------------
    for a in values:
        branch_target = target - a

        if branch_target <= 0:
            continue

        branch_g = 1 / branch_target

        for j in nearby_indices(conductances, branch_g):
            gb, b = conductance_pairs[j]
            remaining_g = branch_g - gb

            if remaining_g <= 0:
                continue

            for k in nearby_indices(conductances, remaining_g):
                gc, c = conductance_pairs[k]

                parallel = 1 / (gb + gc)
                equivalent = a + parallel

                add_result(
                    results,
                    equivalent,
                    target,
                    "Serie-Paralelo",
                    (a, b, c),
                    f"{format_resistance(a)} + "
                    f"({format_resistance(b)} || "
                    f"{format_resistance(c)})"
                )

    # --------------------------------------------------------
    # 3 RESISTENCIAS:
    # R1 || (R2 + R3)
    # --------------------------------------------------------
    for a in values:
        ga = 1 / a
        remaining_g = target_g - ga

        if remaining_g <= 0:
            continue

        branch_target = 1 / remaining_g

        for j in nearby_indices(values, branch_target):
            b = values[j]
            remaining_r = branch_target - b

            if remaining_r <= 0:
                continue

            for k in nearby_indices(values, remaining_r):
                c = values[k]

                series_branch = b + c
                equivalent = 1 / (ga + 1 / series_branch)

                add_result(
                    results,
                    equivalent,
                    target,
                    "Serie-Paralelo",
                    (a, b, c),
                    f"{format_resistance(a)} || "
                    f"({format_resistance(b)} + "
                    f"{format_resistance(c)})"
                )

    # Ordenar por error y quedarse con las 3 mejores.
    ordered = sorted(
        results.values(),
        key=lambda item: item["error"]
    )

    return ordered[:3], len(values)


# ============================================================
# ENCABEZADO
# ============================================================

title = "CALCULADORA DE RESISTENCIAS"

letters = []
for i, letter in enumerate(title):
    if letter == " ":
        letters.append("&nbsp;")
    else:
        letters.append(f"<span>{escape(letter)}</span>")

st.markdown(
    f"""
    <div class="title-box">
        <div class="title">{''.join(letters)}</div>
        <div class="subtitle">
            <b>▮</b> Encuentra la combinación más cercana con resistencias comerciales :D
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# CONTROLES
# ============================================================

col1, col2, col3 = st.columns([1, 1, 1.45])

with col1:
    target = st.number_input(
        "VALOR DESEADO (Ω)",
        min_value=0.001,
        value=430.0,
        step=1.0,
        format="%.3f"
    )

with col2:
    tolerance = st.selectbox(
        "TOLERANCIA DESEADA (%)",
        [10, 1],
        index=0,
        format_func=lambda x: f"{x}%"
    )

with col3:
    st.markdown("<div style='height:27px'></div>", unsafe_allow_html=True)
    calculate = st.button("🔎  Buscar combinaciones", use_container_width=True)

# ============================================================
# RESULTADOS
# ============================================================

# Calcular también al entrar por primera vez.
if calculate or "results" not in st.session_state:
    with st.spinner("Analizando combinaciones..."):
        best_results, amount_values = find_best_combinations(
            target,
            tolerance
        )

    st.session_state["results"] = best_results
    st.session_state["amount_values"] = amount_values
    st.session_state["last_target"] = target
    st.session_state["last_tolerance"] = tolerance

best_results = st.session_state["results"]

series_name = "E12" if tolerance == 10 else "E96"

st.markdown(
    f"""
    <div class="results-header">
        ✅ TOP 3 DE LAS MEJORES COMBINACIONES · SERIE {series_name}
    </div>
    """,
    unsafe_allow_html=True
)

if not best_results:
    st.error("No se encontraron combinaciones.")
else:
    for index, result in enumerate(best_results):
        if index == 0:
            card_class = "best"
            badge = '<span class="badge">MEJOR OPCIÓN</span>'
        elif index == 1:
            card_class = "second"
            badge = ""
        else:
            card_class = "third"
            badge = ""

        error_class = "" if result["error"] <= tolerance else "outside"

        resistor_cards = "".join(
            resistor_card(r, tolerance)
            for r in result["resistors"]
        )

        st.markdown(
            f"""
            <div class="result-card {card_class}">
                <div style="display:flex; align-items:flex-start;">

                    <div class="rank">#{index + 1}</div>

                    <div style="flex:1;">
                        {badge}
                        <div class="type-label">
                            {escape(result["topology"])}
                        </div>
                        <div class="formula">
                            {escape(result["formula"])}
                        </div>

                        <div class="resistors-row">
                            {resistor_cards}
                        </div>
                    </div>

                    <div class="value-box">
                        <div class="eq-value">
                            {format_resistance(result["equivalent"])}
                        </div>
                        <div class="error {error_class}">
                            Error: {result["error"]:.4f}%
                        </div>
                    </div>

                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# EXPLICACIÓN DEL PROGRAMA
# ============================================================

st.markdown(
    """
    <div class="info-box">
        <div class="info-title">¿Cómo funciona?</div>
        <div class="info-text">
            El programa recibe un valor de resistencia y una tolerancia de
            <b>10% o 1%</b>. Después busca la combinación comercial más
            cercana utilizando hasta <b>3 resistencias</b>.
            <br><br>
            Se consideran las conexiones posibles:
            <b>serie</b>, <b>paralelo</b> y las dos configuraciones
            <b>serie-paralelo</b> con tres resistencias.
            <br><br>
            Para 10% se utilizan valores de la serie comercial
            <b>E12</b>. Para 1% se utilizan valores de la serie
            <b>E96</b>. Los resultados se ordenan de acuerdo con su
            error respecto al valor solicitado.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
        Calculadora de resistencias comerciales · Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
