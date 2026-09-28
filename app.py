from __future__ import annotations

import base64
from pathlib import Path
from typing import Final

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Cyclissime | Vélos & performances",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DATA_PATHS: Final = (
    Path(__file__).parent / "attached_assets" / "Financials_cleaned_softr_1789982864958.csv",
    Path(__file__).parent
    / ".local"
    / "conversation-workspace"
    / "files"
    / "attached_assets"
    / "Financials_cleaned_softr_1789982864958.csv",
)

LOGO_PATH: Final = Path(__file__).parent / "attached_assets" / "Logo_Cyclissime_noir_1790582106987.png"

ALL_COUNTRIES_LABEL: Final = "Tous les pays"

# Plotly attend des noms de pays en anglais (locationmode="country names")
COUNTRY_TRANSLATIONS: Final = {
    "Allemagne": "Germany",
    "Mexique": "Mexico",
    "États-Unis": "United States",
    "Etats-Unis": "United States",
    "Espagne": "Spain",
    "Italie": "Italy",
    "Royaume-Uni": "United Kingdom",
    "Suisse": "Switzerland",
    "Belgique": "Belgium",
}

SEGMENT_COLORS: Final = {"Ville": "#4c8ea1", "Sport": "#e56b45", "Famille": "#6b8e62"}

PRODUCTS: Final = {
    "Amarilla": {
        "tag": "ÉDITION SIGNATURE",
        "description": "Un vélo polyvalent et lumineux, pensé pour les trajets qui ne suivent jamais la même route.",
        "image": "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=1200&q=85",
        "accent": "#e6a23c",
    },
    "Carretera": {
        "tag": "PERFORMANCE",
        "description": "Une ligne vive et une transmission précise pour gagner en rythme sans perdre en confort.",
        "image": "https://images.unsplash.com/photo-1502744688674-c619d1586c9e?auto=format&fit=crop&w=1200&q=85",
        "accent": "#e05c3c",
    },
    "Montana": {
        "tag": "EXPLORATION",
        "description": "Stable, endurant et prêt à quitter l’asphalte pour les chemins qui s’ouvrent devant vous.",
        "image": "https://images.unsplash.com/photo-1541625602330-2277a4c46182?auto=format&fit=crop&w=1200&q=85",
        "accent": "#6b8e62",
    },
    "Paseo": {
        "tag": "QUOTIDIEN",
        "description": "Une posture naturelle et une allure élégante pour rendre chaque déplacement plus agréable.",
        "image": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=1200&q=85",
        "accent": "#4c8ea1",
    },
    "Velo": {
        "tag": "ESSENTIEL",
        "description": "L’équilibre juste entre agilité, simplicité et plaisir de rouler tous les jours.",
        "image": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=85",
        "accent": "#5c7188",
    },
    "VTT": {
        "tag": "HORS-PISTE",
        "description": "Des pneus qui accrochent, un cadre rassurant et l’envie de repousser la prochaine montée.",
        "image": "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?auto=format&fit=crop&w=1200&q=85",
        "accent": "#866c57",
    },
}


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #18211f;
            --muted: #6f7b76;
            --cream: #f6f4ef;
            --paper: #fffdf8;
            --sage: #56796b;
            --orange: #e56b45;
            --line: rgba(24, 33, 31, 0.11);
        }

        .stApp {
            background: var(--cream);
            color: var(--ink);
        }

        [data-testid="stHeader"] {
            background: rgba(246, 244, 239, 0.88);
        }

        [data-testid="stSidebar"] {
            background: #e9eee7;
            border-right: 1px solid rgba(24, 33, 31, 0.08);
        }

        [data-testid="stSidebar"] * {
            font-family: "DM Sans", sans-serif;
        }

        .block-container {
            max-width: 1440px;
            padding: 2.25rem 4.5rem 5rem;
        }

        h1, h2, h3, h4, p, li, span, label, button, input {
            font-family: "DM Sans", sans-serif;
        }

        h1, h2, h3 {
            font-family: "Space Grotesk", sans-serif;
            color: var(--ink);
            letter-spacing: -0.045em;
        }

        h1 {
            font-size: clamp(2.8rem, 5.2vw, 6.4rem);
            line-height: 0.95;
        }

        h2 {
            font-size: clamp(2rem, 3.4vw, 4rem);
            line-height: 1.02;
        }

        .brand-mark {
            align-items: center;
            display: flex;
            gap: 0.7rem;
            margin-bottom: 4.3rem;
        }

        .logo-banner {
            align-items: center;
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 22px;
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            justify-content: center;
            margin-bottom: 3.5rem;
            min-height: 126px;
            overflow: hidden;
            padding: 1rem 2.5rem;
        }

        .logo-banner img {
            display: block;
            max-width: 100%;
            object-fit: contain;
            width: 450px;
        }

        .logo-tagline {
            color: var(--ink);
            font-family: "DM Sans", sans-serif;
            font-size: 1rem;
            letter-spacing: 0;
            max-width: 100%;
            text-align: left;
            width: 450px;
        }

        .brand-dot {
            background: var(--orange);
            border-radius: 50%;
            display: inline-block;
            height: 13px;
            position: relative;
            width: 13px;
        }

        .brand-dot:after {
            border: 1px solid var(--orange);
            border-radius: 50%;
            content: "";
            height: 23px;
            left: -6px;
            position: absolute;
            top: -6px;
            width: 23px;
        }

        .brand-name {
            color: var(--ink);
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.12rem;
            font-weight: 700;
            letter-spacing: -0.03em;
        }

        .top-link {
            color: var(--muted);
            font-size: 0.83rem;
            letter-spacing: 0.06em;
            text-decoration: none;
            text-transform: uppercase;
        }

        .top-link:hover {
            color: var(--orange);
        }

        .eyebrow {
            color: var(--orange);
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1.15rem;
            line-height: 1.65;
            max-width: 560px;
        }

        .hero-note {
            border-left: 2px solid var(--orange);
            color: var(--muted);
            font-size: 0.87rem;
            line-height: 1.45;
            margin-top: 2rem;
            padding-left: 1rem;
        }

        .hero-image {
            background: #cad6cb;
            border-radius: 24px;
            min-height: 450px;
            overflow: hidden;
            position: relative;
        }

        .hero-image img {
            height: 100%;
            object-fit: cover;
            width: 100%;
        }

        .hero-sticker {
            background: var(--orange);
            border-radius: 50%;
            bottom: 30px;
            color: white;
            font-size: 0.68rem;
            font-weight: 700;
            height: 106px;
            letter-spacing: 0.08em;
            line-height: 1.25;
            padding-top: 34px;
            position: absolute;
            right: 28px;
            text-align: center;
            text-transform: uppercase;
            transform: rotate(8deg);
            width: 106px;
        }

        .section-space {
            height: 9rem;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.55;
            max-width: 410px;
        }

        /* Lien englobant chaque carte modèle (toutes tailles d'écran) */
        .model-card-link,
        .model-card-link:hover,
        .model-card-link:visited {
            color: inherit;
            display: block;
            text-decoration: none;
        }

        .model-card {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 18px;
            overflow: hidden;
            transition: box-shadow 180ms ease, transform 180ms ease;
        }

        .model-card:hover {
            box-shadow: 0 14px 40px rgba(34, 55, 48, 0.13);
            transform: translateY(-4px);
        }

        .model-image {
            aspect-ratio: 1.25 / 1;
            display: block;
            object-fit: cover;
            width: 100%;
        }

        .model-content {
            padding: 1.2rem 1.3rem 1.45rem;
        }

        .model-tag {
            color: var(--orange);
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.13em;
        }

        .model-title {
            color: var(--ink);
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.35rem;
            font-weight: 600;
            letter-spacing: -0.04em;
            margin: 0.5rem 0;
        }

        .model-description {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.55;
            min-height: 66px;
        }

        .model-stat {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.77rem;
            margin-top: 1.1rem;
            padding-top: 0.9rem;
        }

        .model-stat strong {
            color: var(--ink);
            font-size: 0.95rem;
        }

        .metric-card {
            background: var(--paper);
            border: 1px solid var(--line);
            border-radius: 16px;
            min-height: 142px;
            padding: 1.3rem 1.4rem;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--ink);
            font-family: "Space Grotesk", sans-serif;
            font-size: clamp(1.9rem, 3.2vw, 3rem);
            font-weight: 600;
            letter-spacing: -0.06em;
            margin-top: 0.5rem;
        }

        .metric-caption {
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 0.35rem;
        }

        .insight-box {
            background: #dce8dc;
            border-radius: 18px;
            color: var(--ink);
            padding: 1.35rem 1.5rem;
        }

        .insight-box strong {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.1rem;
        }

        .insight-box p {
            color: #4d6257;
            font-size: 0.88rem;
            line-height: 1.55;
        }

        .footer-note {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 4rem;
            padding-top: 1.2rem;
        }

        @media (max-width: 800px) {
            .block-container {
                padding: 1.5rem 1.15rem 3.5rem;
            }

            .brand-mark {
                margin-bottom: 2.2rem;
            }

            .logo-banner {
                margin-bottom: 2.2rem;
                min-height: 90px;
                padding: 0.8rem 1.2rem;
            }

            .logo-banner img {
                width: 320px;
            }

            .logo-tagline {
                font-size: 0.82rem;
                width: 320px;
            }

            .hero-image {
                margin-top: 1.2rem;
                min-height: 300px;
            }

            .section-space {
                height: 5rem;
            }

        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Données et formatage
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner="Chargement des données commerciales…")
def load_data() -> pd.DataFrame:
    data_path = next((path for path in DATA_PATHS if path.exists()), None)
    if data_path is None:
        raise FileNotFoundError("Le fichier de données Cyclissime est introuvable.")

    df = pd.read_csv(data_path)
    df.columns = [column.strip() for column in df.columns]

    text_columns = ["Segment", "City", "Product", "Discount Band", "Month Name"]
    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    numeric_columns = [
        "Units Sold",
        "Manufacturing Price",
        "Sale Price",
        "Gross Sales",
        "Discounts",
        "Sales",
        "COGS",
        "Profit",
        "Month Number",
        "Year",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def euro(value: float, decimals: int = 0) -> str:
    formatted = f"{value:,.{decimals}f}".replace(",", " ").replace(".", ",")
    return f"{formatted} €"


def integer(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


# ---------------------------------------------------------------------------
# Composants HTML
# ---------------------------------------------------------------------------

def render_metric(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_product_card(product: str, product_data: pd.DataFrame) -> None:
    details = PRODUCTS[product]
    units = product_data["Units Sold"].sum()
    anchor = product.lower()
    st.markdown(
        f"""
        <a class="model-card-link" href="/Produits?produit={anchor}" target="_self">
            <article class="model-card">
                <img class="model-image" src="{details["image"]}" alt="Vélo {product}">
                <div class="model-content">
                    <div class="model-tag">{details["tag"]}</div>
                    <div class="model-title">{product}</div>
                    <div class="model-description">{details["description"]}</div>
                    <div class="model-stat"><strong>{integer(units)}</strong> unités vendues dans la sélection</div>
                </div>
            </article>
        </a>
        """,
        unsafe_allow_html=True,
    )


def render_logo_banner() -> None:
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Le logo Cyclissime est introuvable : {LOGO_PATH}")

    encoded_logo = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div class="logo-banner">
            <img src="data:image/png;base64,{encoded_logo}" alt="Logo Cyclissime">
            <div class="logo-tagline">*Le vélo, simplement</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Graphiques
# ---------------------------------------------------------------------------

def chart_with_country_filter(filtered: pd.DataFrame, base_title: str, key: str) -> pd.DataFrame:
    """Affiche un titre + une liste de pays, et renvoie les données filtrées.

    Le titre est placé au-dessus de la liste grâce à un emplacement réservé,
    puis complété avec le pays choisi ("<titre> - France").
    """
    title_slot = st.empty()

    selected_country = st.selectbox(
        "Pays",
        options=[ALL_COUNTRIES_LABEL, *sorted(filtered["City"].unique())],
        key=key,
        label_visibility="collapsed",
    )

    if selected_country == ALL_COUNTRIES_LABEL:
        title_slot.markdown(f"#### {base_title}")
        return filtered

    title_slot.markdown(f"#### {base_title} - {selected_country}")
    return filtered[filtered["City"] == selected_country]


def render_segment_chart(filtered: pd.DataFrame) -> None:
    """Anneau de répartition des ventes par segment, avec filtre pays local."""
    segment_data = chart_with_country_filter(filtered, "Répartition par segment", key="segment_country")

    segment_summary = (
        segment_data.groupby("Segment", as_index=False)
        .agg(Ventes=("Sales", "sum"), Unités=("Units Sold", "sum"))
        .sort_values("Ventes", ascending=False)
    )

    if segment_summary.empty:
        st.info("Aucune donnée pour cette sélection.")
        return

    fig = px.pie(
        segment_summary,
        names="Segment",
        values="Ventes",
        hole=0.66,
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        marker={"line": {"color": "#f6f4ef", "width": 3}},
        hovertemplate="%{label}<br>%{value:,.0f} €<extra></extra>",
    )
    fig.update_layout(
        height=350,
        margin={"t": 25, "r": 25, "b": 15, "l": 15},
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#18211f"},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_monthly_chart(filtered: pd.DataFrame) -> None:
    """Courbe d'évolution des ventes dans le temps, avec filtre pays local."""
    monthly_data = chart_with_country_filter(filtered, "Évolution des ventes", key="monthly_country")

    monthly = (
        monthly_data.groupby("Date", as_index=False)
        .agg(Ventes=("Sales", "sum"))
        .sort_values("Date")
    )

    if monthly.empty:
        st.info("Aucune donnée pour cette sélection.")
        return

    total_sales = monthly["Ventes"].sum()

    fig = px.area(monthly, x="Date", y="Ventes")
    fig.update_traces(
        line={"color": "#e56b45", "width": 3},
        fillcolor="rgba(229, 107, 69, 0.15)",
        hovertemplate="%{x|%b %Y}<br>%{y:,.0f} €<extra></extra>",
    )
    # Total des ventes affiché en haut à gauche du graphique
    fig.add_annotation(
        text=f"<b>Total : {euro(total_sales)}</b>",
        xref="paper",
        yref="paper",
        x=0.01,
        y=1.0,
        xanchor="left",
        yanchor="bottom",
        showarrow=False,
        font={"family": "Space Grotesk", "size": 16, "color": "#18211f"},
        bgcolor="#fffdf8",
        bordercolor="rgba(24, 33, 31, 0.11)",
        borderwidth=1,
        borderpad=6,
    )
    fig.update_layout(
        height=350,
        margin={"t": 55, "r": 15, "b": 15, "l": 15},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "DM Sans", "color": "#18211f"},
        xaxis={"showgrid": False, "title": None},
        yaxis={"showgrid": True, "gridcolor": "rgba(24,33,31,0.08)", "title": None},
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# Sections de la page
# ---------------------------------------------------------------------------

def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """Affiche les filtres et renvoie le DataFrame filtré."""
    with st.sidebar:
        st.markdown("### Explorer les ventes")
        st.caption("Les indicateurs se recalculent avec votre sélection.")

        segments = sorted(df["Segment"].unique())
        cities = sorted(df["City"].unique())
        products = sorted(df["Product"].unique())
        years = sorted(df["Year"].astype(int).unique())

        selected_segments = st.multiselect("Segments", options=segments, default=segments)
        selected_cities = st.multiselect("Marchés", options=cities, default=cities)
        selected_products = st.multiselect("Modèles", options=products, default=products)
        selected_years = st.multiselect("Années", options=years, default=years)

        st.divider()
        st.caption(f"Source : {integer(len(df))} lignes de ventes")
        st.caption("Données actualisées depuis le fichier CSV fourni.")

    return df[
        df["Segment"].isin(selected_segments)
        & df["City"].isin(selected_cities)
        & df["Product"].isin(selected_products)
        & df["Year"].astype(int).isin(selected_years)
    ].copy()


def render_header() -> None:
    render_logo_banner()
    st.markdown(
        """
        <div class="brand-mark">
            <a class="top-link" href="#collection">Collection</a>
            <a class="top-link" href="#performances">Performances</a>
            <a class="top-link" href="/Produits" target="_self">Produits</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    hero_left, hero_right = st.columns([1.05, 0.95], gap="large")
    with hero_left:
        st.markdown('<div class="eyebrow">Rouler autrement depuis 1987</div>', unsafe_allow_html=True)
        st.title("Le vélo qui vous emmène plus loin.")
        st.markdown(
            '<p class="hero-copy">Cyclissime imagine des vélos simples à aimer, précis à piloter et assez robustes pour suivre tous vos détours.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-note">Une collection construite pour les rues, les sentiers et tous les kilomètres entre les deux.</div>',
            unsafe_allow_html=True,
        )
    with hero_right:
        st.markdown(
            """
            <div class="hero-image">
                <img src="https://images.unsplash.com/photo-1505705694340-019e1e335916?auto=format&fit=crop&w=1400&q=90" alt="Cycliste sur une route">
                <div class="hero-sticker">Fait pour<br>bouger</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_collection(filtered: pd.DataFrame) -> None:
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    st.markdown('<div id="collection"></div>', unsafe_allow_html=True)

    collection_title, collection_copy = st.columns([1, 1], gap="large")
    with collection_title:
        st.markdown('<div class="eyebrow">La collection</div>', unsafe_allow_html=True)
        st.header("Six façons de prendre la route.")
    with collection_copy:
        st.markdown(
            '<p class="section-kicker">Du premier trajet en ville à la sortie qui finit au sommet, chaque modèle a une personnalité claire et une raison d’être.</p>',
            unsafe_allow_html=True,
        )

    showcase_products = list(PRODUCTS)
    for start in range(0, len(showcase_products), 3):
        card_columns = st.columns(3, gap="medium")
        for column, product in zip(card_columns, showcase_products[start : start + 3]):
            with column:
                render_product_card(product, filtered[filtered["Product"] == product])
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)


def render_performances(filtered: pd.DataFrame) -> None:
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    st.markdown('<div id="performances"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Les performances</div>', unsafe_allow_html=True)
    st.header("Les chiffres donnent le rythme.")
    st.markdown(
        '<p class="section-kicker">Une lecture simple de la performance commerciale Cyclissime, calculée sur la sélection active.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 1.4rem'></div>", unsafe_allow_html=True)

    # Indicateurs clés
    total_sales = filtered["Sales"].sum()
    total_units = filtered["Units Sold"].sum()
    total_profit = filtered["Profit"].sum()
    average_basket = total_sales / total_units if total_units else 0

    metrics = st.columns(4, gap="medium")
    with metrics[0]:
        render_metric("Chiffre d’affaires", euro(total_sales), "ventes nettes")
    with metrics[1]:
        render_metric("Vélos vendus", integer(total_units), "unités cumulées")
    with metrics[2]:
        render_metric("Bénéfice", euro(total_profit), "marge après coûts")
    with metrics[3]:
        render_metric("Vente moyenne", euro(average_basket, 2), "par vélo vendu")

    # Graphiques
    st.markdown("<div style='height: 1.6rem'></div>", unsafe_allow_html=True)
    chart_left, chart_right = st.columns([1, 1.25], gap="large")
    with chart_left:
        render_segment_chart(filtered)
    with chart_right:
        render_monthly_chart(filtered)

    # Tableau des modèles + encadré
    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    top_models = (
        filtered.groupby("Product", as_index=False)
        .agg(
            Unités=("Units Sold", "sum"),
            Ventes=("Sales", "sum"),
            Bénéfice=("Profit", "sum"),
        )
        .sort_values("Unités", ascending=False)
    )

    table_left, table_right = st.columns([1.3, 0.7], gap="large")
    with table_left:
        st.markdown("#### Modèles les plus vendus")
        st.dataframe(
            top_models,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Product": st.column_config.TextColumn("Modèle"),
                "Unités": st.column_config.NumberColumn("Unités", format="%d"),
                "Ventes": st.column_config.NumberColumn("Ventes", format="%.0f €"),
                "Bénéfice": st.column_config.NumberColumn("Bénéfice", format="%.0f €"),
            },
        )
    with table_right:
        if top_models.empty:
            leader_name, leader_units = "—", "0"
        else:
            leader = top_models.iloc[0]
            leader_name = str(leader["Product"])
            leader_units = integer(float(leader["Unités"]))

        st.markdown(
            f"""
            <div class="insight-box">
                <strong>Le modèle qui mène la danse</strong>
                <p><b>{leader_name}</b> est en tête de cette sélection avec <b>{leader_units} unités</b> vendues.</p>
                <p>Utilisez les filtres à gauche pour comparer les performances par marché, segment ou année.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def create_boxplot(df: pd.DataFrame):
    """Boîte à moustaches du profit par pays, avec ou sans rabais."""
    data = df.assign(
        Rabais=df["Discounts"].gt(0).map({True: "Avec rabais", False: "Sans rabais"})
    )

    fig = px.box(
        data,
        x="City",
        y="Profit",
        color="Rabais",
        category_orders={
            "City": sorted(data["City"].unique()),
            "Rabais": ["Sans rabais", "Avec rabais"],
        },
        color_discrete_map={"Sans rabais": "#56796b", "Avec rabais": "#e56b45"},
        labels={"City": "Pays", "Profit": "Profit (€)", "Rabais": ""},
        title="Comparaison du profit par pays selon la présence d'un rabais",
    )
    fig.update_layout(
        font_family="Montserrat",
        height=450,
        margin={"t": 70, "r": 15, "b": 15, "l": 15},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.0, "xanchor": "right", "x": 1.0},
        yaxis={"showgrid": True, "gridcolor": "rgba(24,33,31,0.08)"},
    )
    return fig


def render_profit_comparison(filtered: pd.DataFrame) -> None:
    st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)
    if filtered.empty:
        st.info("Aucune donnée pour cette sélection.")
        return
    st.plotly_chart(create_boxplot(filtered), use_container_width=True, config={"displayModeBar": False})


def create_map(df: pd.DataFrame):
    """Carte animée du profit par pays, mois par mois."""
    monthly = (
        df.dropna(subset=["Date"])
        .groupby(["City", "Date"], as_index=False)
        .agg(Profit=("Profit", "sum"))
        .sort_values("Date")
    )
    monthly["Country"] = monthly["City"].replace(COUNTRY_TRANSLATIONS)
    monthly["Mois"] = monthly["Date"].dt.strftime("%Y-%m")
    # La taille d'une bulle ne peut pas être négative : on borne à 0 pour l'affichage,
    # le profit réel reste visible au survol.
    monthly["Taille"] = monthly["Profit"].clip(lower=0)

    fig = px.scatter_geo(
        monthly,
        locations="Country",
        locationmode="country names",
        hover_name="City",
        hover_data={"Profit": ":,.0f", "Country": False, "Taille": False, "Mois": False},
        size="Taille",
        size_max=45,
        color="City",
        animation_frame="Mois",
        projection="natural earth",
        labels={"City": "Pays"},
        title="Carte animée de l'évolution du profit par pays au fil du temps",
    )
    fig.update_geos(
        showcountries=True,
        countrycolor="rgba(24, 33, 31, 0.25)",
        showland=True,
        landcolor="#e9eee7",
        showocean=True,
        oceancolor="#f6f4ef",
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        font_family="Montserrat",
        height=560,
        margin={"t": 70, "r": 10, "b": 10, "l": 10},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_profit_map(filtered: pd.DataFrame) -> None:
    st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)
    if filtered.empty:
        st.info("Aucune donnée pour cette sélection.")
        return
    st.plotly_chart(create_map(filtered), use_container_width=True, config={"displayModeBar": False})


def render_footer() -> None:
    st.markdown(
        '<div class="footer-note">Cyclissime · Une sélection de vélos pensée pour garder le mouvement simple.</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main() -> None:
    inject_styles()
    df = load_data()

    filtered = render_sidebar(df)

    render_header()
    render_hero()
    render_collection(filtered)
    render_performances(filtered)
    render_profit_comparison(filtered)
    render_profit_map(filtered)
    render_footer()


if __name__ == "__main__":
    main()