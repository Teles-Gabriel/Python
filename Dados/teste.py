import pandas as pd
import numpy as np
import matplotlib.pyplot as plit
import plotly.graph_objects as go
import plotly.express as px
import datetime
import warnings
warnings.filterwarnings('ignore')

### ler os arquivos em csv
######metadados
customers_df = pd.read_csv("./archive/olist_customers_dataset.csv")
geo_df = pd.read_csv("./archive/olist_geolocation_dataset.csv")
orderitem_df = pd.read_csv("./archive/olist_order_items_dataset.csv")
orderpay_df = pd.read_csv("./archive/olist_order_payments_dataset.csv")
orderreviews_df = pd.read_csv("./archive/olist_order_reviews_dataset.csv")
orders_df = pd.read_csv("./archive/olist_orders_dataset.csv")
products_df = pd.read_csv("./archive/olist_products_dataset.csv")
sellers_df = pd.read_csv("./archive/olist_sellers_dataset.csv")
categname_df = pd.read_csv("./archive/product_category_name_translation.csv")
pd.set_option('display.max_columns', 500)
customers_df.shape


#print(customers_df.head(10))
#print(geo_df.head(10))
#print(orderitem_df.head(10))

print("customers_df:")
print(customers_df.head())

print("\ngeo_df:")
print(geo_df.head())

print("\norderitem_df:")
print(orderpay_df.head)

print("\norderpay_df:")
print(orderpay_df.head())

print("\norderreviews_df:")
print(orderreviews_df.head())

print("\norders_df:")
print(orders_df.head())

print("\nproducts_df:")
print(products_df.head())

print("\nsellers_df:")
print(sellers_df.head())

print("\ncategname_df:")
print(categname_df.head())

##

print("customers_df:\n")
print(customers_df.info())

print("\ngeo_df:\n")
print(geo_df.info())

print("\norderitem_df:\n")
print(orderitem_df.info())

print("\norderpay_df:\n")
print(orderpay_df.info())

print("\norderreviews_df:\n")
print(orderreviews_df.info())

print("\norders_df:\n")
print(orders_df.info())

print("\nproducts_df:\n")
print(products_df.info())

print("\nsellers_df:\n")
print(sellers_df.info())

print("\ncategname_df:\n")
print(categname_df.info())

##renomear colunas

print('............................................................')
print('É aqui seu cego')
customers_df = customers_df.rename(columns={"customer_zip_code_prefix": "zip_code"})
geo_df = geo_df.rename(columns={"geolocation_zip_code_prefix": "zip_code"})

#####Merge dos dataframes

data = orders_df.merge(customers_df, on="customer_id").merge(orderitem_df, on="order_id").merge(products_df, on="product_id").merge(categname_df, on="product_category_name").merge(orderpay_df, on="order_id").merge(sellers_df, on="seller_id").merge(orderreviews_df, on="order_id")
print(data.head())
print('......................................')
# Porcentagem de valores nulos
print((100 * data.isna().sum() / len(data) ).sort_values(ascending=False))

print('.......................................')
print(data.describe())

print('.................................')

fig = px.histogram(data, x="review_score")
fig.show()

###porcentagem

percentage = data["review_score"].value_counts(normalize=True) * 100

fig = px.bar(percentage, x=percentage.index, y=percentage.values, text=percentage.values, labels={"x": "Nota", "y": "Percentagem"})
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.show()

# Clientes com o maior número cumulativo de pedidos (em pagamentos).
top_customers = data.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
top_customers.rename(columns={"payment_value":"total_paid"}, inplace=True)

# calcular as colunas "% of Total Sales" e "Cum % of Total Sales"
top_customers["% of Total Sales"] = (top_customers["total_paid"] / top_customers["total_paid"].sum()) * 100
top_customers["Cum % of Total Sales"] = top_customers["% of Total Sales"].cumsum()

# criar um gráfico de linhas do Plotly
fig = px.line(top_customers, x=range(1, len(top_customers) + 1), y="Cum % of Total Sales")

# definir as etiquetas do eixo x e y e o título do gráfico
fig.update_layout(
    xaxis_title="Número de Clientes",
    yaxis_title="Total Vendas Cumulativo %",
    title="Contribuição % para as vendas por número de clientes"
)

# adicionar uma linha de preenchimento abaixo do gráfico
fig.add_shape(
    type="rect",
    xref="x",
    yref="paper",
    x0=0,
    y0=0,
    x1=40000,
    y1=1,
    fillcolor="green",
    opacity=0.2,
    layer="below"
)

# atualizar o layout da forma para ajustar a altura do preenchimento
fig.update_shapes(dict(xref='x', yref='paper'))

# adicionar um texto explicativo na figura
fig.add_annotation(
    x=55000,
    y=75,
    text="40k clientes (+-42% do total)<br> representam +-80% das vendas",
    font=dict(
        size=14,
        color="black"
    ),
    showarrow=False,
)

# exibir a figura
fig.show()