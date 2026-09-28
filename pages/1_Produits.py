from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from app import PRODUCTS, euro, inject_styles, integer, load_data


inject_styles()

st.markdown(
    """
    <style>
    .products-intro {
        color: var(--muted);
        font-size: 1.08rem;
        line-height: 1.65;
        max-width: 650px;
    }

    .product-page-card {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 18px;
        overflow: hidden;
        margin-bottom: 1.4rem;
        /* Laisse de la place sous l'en-tête fixe de Streamlit lors du défilement */
        scroll-margin-top: 90px;
        transition: box-shadow 400ms ease;
    }

    /* Mise en évidence temporaire de la carte ciblée */
    .product-page-card.is-target {
        box-shadow: 0 0 0 3px var(--orange), 0 18px 45px rgba(34, 55, 48, 0.16);
    }

    .product-page-image {
        aspect-ratio: 1.8 / 1;
        display: block;
        object-fit: cover;
        width: 100%;
    }

    .product-page-content {
        padding: 1.25rem 1.35rem 1.45rem;
    }

    .product-page-tag {
        color: var(--orange);
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .product-page-title {
        color: var(--ink);
        font-family: "Space Grotesk", sans-serif;
        font-size: 1.7rem;
        letter-spacing: -0.05em;
        margin: 0.35rem 0 0.55rem;
    }

    .product-page-description {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
        min-height: 72px;
    }

    .product-page-facts {
        border-top: 1px solid var(--line);
        display: grid;
        gap: 0.85rem;
        grid-template-columns: repeat(2, 1fr);
        margin-top: 1.1rem;
        padding-top: 1rem;
    }

    .product-page-fact span {
        color: var(--muted);
        display: block;
        font-size: 0.68rem;
        letter-spacing: 0.08em;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
    }

    .product-page-fact strong {
        color: var(--ink);
        font-family: "Space Grotesk", sans-serif;
        font-size: 1rem;
    }

    @media (max-width: 800px) {
        .product-page-description {
            min-height: 0;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_target_product() -> str | None:
    """Lit ?produit=... dans l'URL et le valide contre la liste des modèles."""
    raw = st.query_params.get("produit", "")
    target = str(raw).strip().lower()
    valid = {product.lower() for product in PRODUCTS}
    return target if target in valid else None


def scroll_to_product(anchor: str) -> None:
    """Attend que la carte soit rendue dans la page, puis défile jusqu'à elle."""
    components.html(
        f"""
        <script>
        (function () {{
            const target = {json.dumps(anchor)};
            const doc = window.parent.document;
            let tries = 0;

            const findCard = () =>
                doc.getElementById(target) ||
                Array.from(doc.querySelectorAll(".product-page-card")).find((card) => {{
                    const title = card.querySelector(".product-page-title");
                    return title && title.textContent.trim().toLowerCase() === target;
                }});

            const timer = setInterval(() => {{
                const card = findCard();
                if (card) {{
                    clearInterval(timer);
                    card.scrollIntoView({{ behavior: "smooth", block: "start" }});
                    card.classList.add("is-target");
                    setTimeout(() => card.classList.remove("is-target"), 2500);
                }} else if (++tries > 60) {{
                    clearInterval(timer);  // abandon après ~6 s
                }}
            }}, 100);
        }})();
        </script>
        """,
        height=0,
    )


df = load_data()
target_product = get_target_product()

st.markdown('<div class="eyebrow">La gamme Cyclissime</div>', unsafe_allow_html=True)
st.title("Les produits")
st.markdown(
    '<p class="products-intro">Découvrez les six modèles Cyclissime, leur personnalité et les performances enregistrées dans les ventes.</p>',
    unsafe_allow_html=True,
)
st.markdown("<div style='height: 1.4rem'></div>", unsafe_allow_html=True)


for start in range(0, len(PRODUCTS), 2):
    product_columns = st.columns(2, gap="large")
    for column, product in zip(product_columns, list(PRODUCTS)[start : start + 2]):
        product_data = df[df["Product"] == product]
        details = PRODUCTS[product]
        total_units = product_data["Units Sold"].sum()
        total_sales = product_data["Sales"].sum()
        average_price = total_sales / total_units if total_units else 0
        leading_segment = (
            product_data.groupby("Segment")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
            if not product_data.empty
            else "—"
        )
        leading_market = (
            product_data.groupby("City")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
            if not product_data.empty
            else "—"
        )

        with column:
            st.markdown(
                f"""
                <article class="product-page-card" id="{product.lower()}">
                    <img class="product-page-image" src="{details["image"]}" alt="Vélo {product}">
                    <div class="product-page-content">
                        <div class="product-page-tag">{details["tag"]}</div>
                        <div class="product-page-title">{product}</div>
                        <div class="product-page-description">{details["description"]}</div>
                        <div class="product-page-facts">
                            <div class="product-page-fact">
                                <span>Unités vendues</span>
                                <strong>{integer(total_units)}</strong>
                            </div>
                            <div class="product-page-fact">
                                <span>Chiffre d’affaires</span>
                                <strong>{euro(total_sales)}</strong>
                            </div>
                            <div class="product-page-fact">
                                <span>Prix moyen vendu</span>
                                <strong>{euro(average_price, 2)}</strong>
                            </div>
                            <div class="product-page-fact">
                                <span>Segment principal</span>
                                <strong>{leading_segment}</strong>
                            </div>
                        </div>
                        <div class="product-page-fact" style="margin-top: 0.9rem;">
                            <span>Marché principal</span>
                            <strong>{leading_market}</strong>
                        </div>
                    </div>
                </article>
                """,
                unsafe_allow_html=True,
            )


# Placé en fin de page : les cartes sont déjà envoyées au navigateur quand le script démarre.
if target_product:
    scroll_to_product(target_product)
