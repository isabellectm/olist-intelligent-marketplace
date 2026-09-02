"""Fase 1 — análise exploratória da Olist (7 blocos).

Rode na raiz do repositório:
    python notebooks/01_analise_exploratoria.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
FIG = ROOT / "outputs" / "figuras"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams["figure.figsize"] = (8, 4.5)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def load():
    orders = pd.read_csv(
        DATA / "olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )
    return {
        "orders": orders,
        "items": pd.read_csv(DATA / "olist_order_items_dataset.csv"),
        "payments": pd.read_csv(DATA / "olist_order_payments_dataset.csv"),
        "reviews": pd.read_csv(DATA / "olist_order_reviews_dataset.csv"),
        "customers": pd.read_csv(DATA / "olist_customers_dataset.csv"),
        "products": pd.read_csv(DATA / "olist_products_dataset.csv"),
        "sellers": pd.read_csv(DATA / "olist_sellers_dataset.csv"),
        "geo": pd.read_csv(DATA / "olist_geolocation_dataset.csv"),
        "translation": pd.read_csv(DATA / "product_category_name_translation.csv"),
    }


def bloco_1_dicionario(dfs):
    print("\n=== BLOCO 1 — Dicionário e ligações ===")
    print(
        "Pedido (orders) liga cliente, itens, pagamentos e reviews.\n"
        "Item liga produto e vendedor. Cliente e vendedor ligam à geolocalização pelo CEP.\n"
        "customer_id é por pedido; customer_unique_id é a pessoa real."
    )
    for name, df in dfs.items():
        print(f"{name:12} {len(df):>10,} linhas  |  colunas: {list(df.columns)}")


def bloco_2_operacao(orders, customers):
    print("\n=== BLOCO 2 — Operação do pedido ===")
    print("Período:", orders.order_purchase_timestamp.min(), "→", orders.order_purchase_timestamp.max())
    print(orders.order_status.value_counts())
    delivered = orders[orders.order_status == "delivered"].copy()
    delivered["atraso_dias"] = (
        delivered.order_delivered_customer_date - delivered.order_estimated_delivery_date
    ).dt.days
    delivered["lead_dias"] = (
        delivered.order_delivered_customer_date - delivered.order_purchase_timestamp
    ).dt.days
    late = delivered["atraso_dias"] > 0
    print(f"Entregues: {len(delivered):,}")
    print(f"% atrasados (depois da data prometida): {late.mean()*100:.2f}%")
    print(f"Mediana de atraso (só atrasados): {delivered.loc[late, 'atraso_dias'].median():.0f} dias")
    print(f"Mediana do prazo real de entrega: {delivered.lead_dias.median():.0f} dias")

    oc = delivered.merge(customers, on="customer_id")
    oc["atrasado"] = oc.atraso_dias > 0
    by_uf = oc.groupby("customer_state").agg(n=("order_id", "count"), pct_atraso=("atrasado", "mean"))
    by_uf["pct_atraso"] *= 100
    print("Maiores % de atraso (UF com pelo menos 1.000 entregas):")
    print(by_uf[by_uf.n >= 1000].sort_values("pct_atraso", ascending=False).head(8).round(2))

    status = orders.order_status.value_counts()
    fig, ax = plt.subplots()
    status.plot(kind="bar", ax=ax, color="#1f4e79")
    ax.set_title("Pedidos por status")
    ax.set_ylabel("Quantidade")
    fig.tight_layout()
    fig.savefig(FIG / "01_status_pedidos.png", dpi=120)
    plt.close()
    return delivered


def bloco_3_dinheiro(items, payments):
    print("\n=== BLOCO 3 — Dinheiro e item ===")
    gmv = items.price.sum()
    frete = items.freight_value.sum()
    print(f"GMV (soma dos preços): R$ {gmv:,.0f}")
    print(f"Frete total: R$ {frete:,.0f} ({frete/gmv*100:.1f}% do GMV)")
    por_pedido = items.groupby("order_id").agg(itens=("order_item_id", "count"), valor=("price", "sum"), frete=("freight_value", "sum"))
    print(f"Ticket médio: R$ {por_pedido.valor.mean():.2f} | mediana: R$ {por_pedido.valor.median():.2f}")
    print(f"Itens por pedido (média): {por_pedido.itens.mean():.2f}")
    print("Meios de pagamento (% de linhas):")
    print((payments.payment_type.value_counts(normalize=True) * 100).round(1))

    fig, ax = plt.subplots()
    payments.payment_type.value_counts().plot(kind="bar", ax=ax, color="#2e75b6")
    ax.set_title("Pagamentos por meio")
    fig.tight_layout()
    fig.savefig(FIG / "02_meios_pagamento.png", dpi=120)
    plt.close()


def bloco_4_reviews(reviews, orders):
    print("\n=== BLOCO 4 — Experiência (reviews) ===")
    print((reviews.review_score.value_counts(normalize=True).sort_index() * 100).round(1))
    print(f"Nota média: {reviews.review_score.mean():.2f}")
    print(f"% notas 1 ou 2: {(reviews.review_score <= 2).mean()*100:.1f}%")
    print(f"% com texto de comentário: {reviews.review_comment_message.notna().mean()*100:.1f}%")

    rev = reviews.merge(
        orders[
            [
                "order_id",
                "order_status",
                "order_delivered_customer_date",
                "order_estimated_delivery_date",
            ]
        ],
        on="order_id",
        how="left",
    )
    d = rev[rev.order_status == "delivered"].copy()
    d["atrasado"] = d.order_delivered_customer_date > d.order_estimated_delivery_date
    print(f"Nota média no prazo: {d.loc[~d.atrasado, 'review_score'].mean():.2f}")
    print(f"Nota média atrasado: {d.loc[d.atrasado, 'review_score'].mean():.2f}")
    print(f"% notas 1-2 no prazo: {(d.loc[~d.atrasado, 'review_score'] <= 2).mean()*100:.1f}%")
    print(f"% notas 1-2 atrasado: {(d.loc[d.atrasado, 'review_score'] <= 2).mean()*100:.1f}%")
    canc = rev[rev.order_status == "canceled"]
    print(f"Nota média em cancelados: {canc.review_score.mean():.2f} (n={len(canc)})")

    fig, ax = plt.subplots()
    reviews.review_score.value_counts().sort_index().plot(kind="bar", ax=ax, color="#c45911")
    ax.set_title("Distribuição das notas de review")
    ax.set_xlabel("Nota")
    fig.tight_layout()
    fig.savefig(FIG / "03_notas_review.png", dpi=120)
    plt.close()

    fig, ax = plt.subplots()
    d.groupby("atrasado").review_score.mean().rename({False: "No prazo", True: "Atrasado"}).plot(
        kind="bar", ax=ax, color=["#548235", "#c00000"]
    )
    ax.set_title("Nota média: no prazo vs atrasado")
    ax.set_ylim(0, 5)
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(FIG / "04_nota_vs_atraso.png", dpi=120)
    plt.close()


def bloco_5_retencao(orders, customers):
    print("\n=== BLOCO 5 — Cliente e retenção ===")
    oc = orders.merge(customers, on="customer_id")
    vc = oc.groupby("customer_unique_id").order_id.nunique()
    print(f"Clientes únicos: {vc.size:,}")
    print(f"% com um único pedido: {(vc == 1).mean()*100:.2f}%")
    print(f"% com 2 ou mais pedidos: {(vc >= 2).mean()*100:.2f}%")
    print(f"Máximo de pedidos de um cliente: {vc.max()}")
    print("Concentração por UF:")
    print((customers.customer_state.value_counts(normalize=True).head(8) * 100).round(1))

    fig, ax = plt.subplots()
    pd.Series({"1 pedido": (vc == 1).mean() * 100, "2+ pedidos": (vc >= 2).mean() * 100}).plot(
        kind="bar", ax=ax, color="#7030a0"
    )
    ax.set_title("Recompra: quase toda a base compra uma vez")
    ax.set_ylabel("% de clientes")
    fig.tight_layout()
    fig.savefig(FIG / "05_recompra.png", dpi=120)
    plt.close()


def bloco_6_oferta(items, products, sellers, translation):
    print("\n=== BLOCO 6 — Oferta (produtos e vendedores) ===")
    print(f"Produtos: {len(products):,} | categorias: {products.product_category_name.nunique()}")
    print(f"Vendedores: {len(sellers):,}")
    itp = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    cat = (
        itp.groupby("product_category_name")
        .agg(gmv=("price", "sum"), n=("order_id", "count"))
        .sort_values("gmv", ascending=False)
    )
    print("Top 10 categorias por GMV:")
    print(cat.head(10).round(0))
    print(f"Top 10 = {cat.head(10).gmv.sum() / cat.gmv.sum() * 100:.1f}% do GMV")
    sv = items.groupby("seller_id").price.sum().sort_values(ascending=False)
    print(f"Top 10 vendedores = {sv.head(10).sum() / sv.sum() * 100:.1f}% do GMV")
    print(f"Top 50 vendedores = {sv.head(50).sum() / sv.sum() * 100:.1f}% do GMV")

    fig, ax = plt.subplots()
    cat.head(10).gmv.sort_values().plot(kind="barh", ax=ax, color="#1f4e79")
    ax.set_title("Top 10 categorias por GMV (R$)")
    fig.tight_layout()
    fig.savefig(FIG / "06_top_categorias.png", dpi=120)
    plt.close()


def bloco_7_sintese():
    print("\n=== BLOCO 7 — Síntese (entrada da priorização) ===")
    print(
        "1. Atraso é raro (~6,8%), mas destrói a nota (2,57 vs 4,29; 54% de notas 1-2).\n"
        "2. Há massa de reviews ruins e texto livre (~15% notas 1-2; 41% com comentário).\n"
        "3. A base quase não recompra (96,9% com um pedido).\n"
        "4. Frete pesa (16,5% do GMV) e o ticket é baixo (mediana ~R$ 87).\n"
        "5. Exceções (cancelado/indisponível) são poucas, mas a nota de cancelados é ~1,8.\n"
        "Detalhamento: docs/priorizacao_problemas.md"
    )


def main():
    dfs = load()
    bloco_1_dicionario(dfs)
    bloco_2_operacao(dfs["orders"], dfs["customers"])
    bloco_3_dinheiro(dfs["items"], dfs["payments"])
    bloco_4_reviews(dfs["reviews"], dfs["orders"])
    bloco_5_retencao(dfs["orders"], dfs["customers"])
    bloco_6_oferta(dfs["items"], dfs["products"], dfs["sellers"], dfs["translation"])
    bloco_7_sintese()
    print(f"\nGráficos salvos em {FIG}")


if __name__ == "__main__":
    main()
