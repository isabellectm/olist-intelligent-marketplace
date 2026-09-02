"""Gera o notebook da Fase 1."""
import json
from pathlib import Path

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    },
    "cells": [],
}


def md(text: str) -> None:
    src = text if text.endswith("\n") else text + "\n"
    nb["cells"].append({"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)})


def code(text: str) -> None:
    src = text if text.endswith("\n") else text + "\n"
    nb["cells"].append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": src.splitlines(keepends=True),
        }
    )


md(
    "# Fase 1 — Análise exploratória Olist\n\n"
    "Sete blocos, na ordem do escopo. Para gerar gráficos no terminal:\n"
    "`python notebooks/01_analise_exploratoria.py` (rode na raiz do repositório).\n\n"
    "O notebook é gerado por `python scripts/gerar_notebook.py`."
)
md(
    "## Bloco 1 — Dicionário e ligações\n\n"
    "O pedido é o centro. `customer_id` é por compra; `customer_unique_id` é a pessoa."
)
code(
    """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ORDERS_CSV = "olist_orders_dataset.csv"


def find_root() -> Path:
    starts = [Path.cwd().resolve()]
    nb = globals().get("__vsc_ipynb_file__")
    if nb:
        starts.append(Path(nb).resolve().parent)
    seen = set()
    for start in starts:
        for folder in (start, *start.parents):
            if folder in seen:
                continue
            seen.add(folder)
            if (folder / "data" / "raw" / ORDERS_CSV).exists():
                return folder
    raise FileNotFoundError(
        "Não achei data/raw/olist_orders_dataset.csv. "
        "Coloque os CSVs da Olist em data/raw/ (veja data/raw/README.md)."
    )


ROOT = find_root()
DATA = ROOT / "data" / "raw"
print("pasta de trabalho:", Path.cwd())
print("lendo de", DATA)

orders = pd.read_csv(DATA / ORDERS_CSV, parse_dates=[
    "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
    "order_delivered_customer_date", "order_estimated_delivery_date"])
items = pd.read_csv(DATA / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(DATA / "olist_order_reviews_dataset.csv")
customers = pd.read_csv(DATA / "olist_customers_dataset.csv")
products = pd.read_csv(DATA / "olist_products_dataset.csv")
sellers = pd.read_csv(DATA / "olist_sellers_dataset.csv")

for name, df in [("orders", orders), ("items", items), ("payments", payments),
                 ("reviews", reviews), ("customers", customers),
                 ("products", products), ("sellers", sellers)]:
    print(f"{name:12} {len(df):>8,}  {list(df.columns)}")
"""
)
md("## Bloco 2 — Operação do pedido")
code(
    """print(orders.order_purchase_timestamp.min(), "→", orders.order_purchase_timestamp.max())
print(orders.order_status.value_counts())
delivered = orders[orders.order_status == "delivered"].copy()
delivered["atraso_dias"] = (
    delivered.order_delivered_customer_date - delivered.order_estimated_delivery_date
).dt.days
late = delivered.atraso_dias > 0
print(f"Entregues: {len(delivered):,} | % atraso: {late.mean()*100:.2f}%")
print(f"Mediana atraso (atrasados): {delivered.loc[late, 'atraso_dias'].median():.0f} dias")
oc = delivered.merge(customers, on="customer_id")
oc["atrasado"] = oc.atraso_dias > 0
by = oc.groupby("customer_state").agg(n=("order_id", "count"), pct=("atrasado", "mean"))
print((by[by.n >= 1000].assign(pct=lambda d: d.pct * 100).sort_values("pct", ascending=False).head(8).round(2)))
orders.order_status.value_counts().plot(kind="bar", title="Pedidos por status")
plt.tight_layout()
"""
)
md("## Bloco 3 — Dinheiro e item")
code(
    """gmv, frete = items.price.sum(), items.freight_value.sum()
print(f"GMV R$ {gmv:,.0f} | frete R$ {frete:,.0f} ({frete/gmv*100:.1f}% do GMV)")
pp = items.groupby("order_id").price.sum()
print(f"Ticket médio {pp.mean():.2f} | mediana {pp.median():.2f}")
print((payments.payment_type.value_counts(normalize=True) * 100).round(1))
payments.payment_type.value_counts().plot(kind="bar", title="Meios de pagamento")
plt.tight_layout()
"""
)
md("## Bloco 4 — Experiência (reviews)")
code(
    """print((reviews.review_score.value_counts(normalize=True).sort_index() * 100).round(1))
print("nota média", round(reviews.review_score.mean(), 2))
print("% notas 1-2", round((reviews.review_score <= 2).mean() * 100, 1))
print("% com texto", round(reviews.review_comment_message.notna().mean() * 100, 1))
rev = reviews.merge(
    orders[["order_id", "order_status", "order_delivered_customer_date", "order_estimated_delivery_date"]],
    on="order_id",
)
d = rev[rev.order_status == "delivered"].copy()
d["atrasado"] = d.order_delivered_customer_date > d.order_estimated_delivery_date
print("nota no prazo", round(d.loc[~d.atrasado, "review_score"].mean(), 2))
print("nota atrasado", round(d.loc[d.atrasado, "review_score"].mean(), 2))
print("% 1-2 atrasado", round((d.loc[d.atrasado, "review_score"] <= 2).mean() * 100, 1))
reviews.review_score.value_counts().sort_index().plot(kind="bar", title="Notas de review")
plt.tight_layout()
"""
)
md("## Bloco 5 — Cliente e retenção")
code(
    """vc = orders.merge(customers, on="customer_id").groupby("customer_unique_id").order_id.nunique()
print("clientes", f"{vc.size:,}", "| % um pedido", round((vc == 1).mean() * 100, 2))
print((customers.customer_state.value_counts(normalize=True).head(5) * 100).round(1))
"""
)
md("## Bloco 6 — Oferta")
code(
    """print("produtos", len(products), "categorias", products.product_category_name.nunique(), "sellers", len(sellers))
itp = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
cat = itp.groupby("product_category_name").price.sum().sort_values(ascending=False)
print(cat.head(10).round(0))
print("top 10 % GMV", round(cat.head(10).sum() / cat.sum() * 100, 1))
"""
)
md(
    "## Bloco 7 — Síntese\n\n"
    "1. Atraso raro, nota destruída (2,57 vs 4,29).\n"
    "2. Reviews ruins + texto para classificar.\n"
    "3. 96,9% compram uma vez.\n"
    "4. Frete relevante; não vira agente próprio nesta fase.\n"
    "5. Cancelados com nota ~1,8.\n\n"
    "Priorização e agentes: pasta `docs/`."
)

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "notebooks" / "01_analise_exploratoria.ipynb"
out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("escrito", out)
