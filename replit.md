# Cyclissime

Application Streamlit de présentation de vélos et d'analyse des ventes Cyclissime à partir d'un fichier CSV.

## Run & Operate

- `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true` — lancer l'application
- Le workflow `Cyclissime Streamlit` démarre l'application sur le port 5000.
- Le fichier source des données est `attached_assets/Financials_cleaned_softr_1789982864958.csv`.

## Stack

- Python 3.11
- Streamlit, pandas et Plotly
- Données tabulaires calculées à la volée avec cache Streamlit

## Where things live

- `app.py` — page Cyclissime, chargement des données, filtres, cartes produits et graphiques.
- `attached_assets/` — données commerciales fournies.
- `requirements.txt` — dépendances Python de l'application.

## Architecture decisions

- Les indicateurs sont recalculés depuis le CSV filtré, sans valeurs commerciales codées en dur.
- La sélection dans la barre latérale pilote à la fois les métriques, les graphiques et le tableau.
- Les images produit sont des visuels distants afin de garder le dépôt léger.

## Product

Cyclissime présente six modèles de vélos, puis permet d'explorer les ventes par segment, marché, modèle et année. La page affiche le chiffre d'affaires, les unités vendues, le bénéfice, la vente moyenne, la répartition par segment, l'évolution temporelle et le classement des modèles.

## User preferences

L'interface demandée est en français, moderne et responsive.

## Gotchas

- Le lancement non interactif doit conserver `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`; sans ce paramètre Streamlit peut attendre l'e-mail d'accueil et ne pas ouvrir le port.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
