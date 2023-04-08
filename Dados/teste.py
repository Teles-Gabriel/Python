import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import datetime
import warnings

warnings.filterwarnings("ignore")

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
##print(orderitem_df.head(10))
#
#print("customers_df:")
#print(customers_df.head())
#
#print("\ngeo_df:")
#print(geo_df.head())
#
#print("\norderitem_df:")
#print(orderpay_df.head)
#
#print("\norderpay_df:")
#print(orderpay_df.head())
#
#print("\norderreviews_df:")
#print(orderreviews_df.head())
#
#print("\norders_df:")
#print(orders_df.head())
#
#print("\nproducts_df:")
#print(products_df.head())
#
#print("\nsellers_df:")
#print(sellers_df.head())
#
#print("\ncategname_df:")
#print(categname_df.head())
#
###
#
#print("customers_df:\n")
#print(customers_df.info())
#
#print("\ngeo_df:\n")
#print(geo_df.info())
#
#print("\norderitem_df:\n")
#print(orderitem_df.info())
#
#print("\norderpay_df:\n")
#print(orderpay_df.info())
#
#print("\norderreviews_df:\n")
#print(orderreviews_df.info())
#
#print("\norders_df:\n")
#print(orders_df.info())
#
#print("\nproducts_df:\n")
#print(products_df.info())
#
#print("\nsellers_df:\n")
#print(sellers_df.info())
#
#print("\ncategname_df:\n")
#print(categname_df.info())
#
###renomear colunas
#
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

### HISTOGRAMA ###

#fig = px.histogram(data, x="review_score")
#fig.show()

###porcentagem

percentage = data["review_score"].value_counts(normalize=True) * 100

fig = px.bar(percentage, x=percentage.index, y=percentage.values, text=percentage.values, labels={"x": "Nota", "y": "Percentagem"})
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig.show()

# Clientes com o maior número cumulativo de pedidos (em pagamentos).
## Aplicação de Pareto
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

# renomear a coluna "payment_value" para "total_paid"
top_customers.rename(columns={"payment_value" : "total_paid"}, inplace=True)


# criar um gráfico de barras do Plotly
fig = px.bar(top_customers[:10], x="total_paid", y="customer_unique_id", orientation="h")

# atualizar as configurações de layout do gráfico
fig.update_layout(
    title="Top 10 Clientes por Valor Total Pago",
    xaxis_title="Valor Total Pago",
    yaxis_title="ID do Cliente Único"
)

# exibir o gráfico
fig.show()


# agrupar o dataframe por "customer_state" e contar o número de "order_id" por estado
top_orders_cities = data.groupby("customer_state")["order_id"].count().reset_index().sort_values("order_id", ascending=False)

# renomear a coluna "order_id" para "count"
top_orders_cities.rename(columns={"order_id":"count"}, inplace=True)

# criar um gráfico de barras do Plotly
fig = px.bar(top_orders_cities[:10], x="count", y="customer_state", orientation="h")

# atualizar as configurações de layout do gráfico
fig.update_layout(
    title="TOP 10 Estados por Número de Pedidos",
    xaxis_title="Número de Pedidos",
    yaxis_title="Estado"
)

# exibir o gráfico
fig.show()


### Filtrando as cidades que mais geram dinheiro

top_ordersbyvalue_cities = data.groupby("customer_city")["payment_value"].sum().reset_index().sort_values("payment_value", ascending=False)
top_ordersbyvalue_cities["% of Total Payments"] = (top_ordersbyvalue_cities["payment_value"] / top_ordersbyvalue_cities["payment_value"].sum()) * 100
top_ordersbyvalue_cities["Cum % of Total Payments"] = top_ordersbyvalue_cities["% of Total Payments"].cumsum() 

# criar um gráfico de barras do Plotly
fig = px.bar(top_ordersbyvalue_cities[:10], x="% of Total Payments", y="customer_city", orientation="h")

# atualizar as configurações de layout do gráfico
fig.update_layout(
    title="TOP 10 Cidades por Geração de Receita",
    xaxis_title="Porcentagem do Total de Pagamentos",
    yaxis_title="Cidade do Cliente"
)

# exibir o gráfico
fig.show()


# criar um gráfico de linha do Plotly
fig = px.line(top_ordersbyvalue_cities, x=range(1, len(top_ordersbyvalue_cities)+1), y="Cum % of Total Payments")

# atualizar as configurações de layout do gráfico
fig.update_layout(
    title="% de Contribuição das Vendas por Número de Cidades",
    xaxis_title="Número de Cidades",
    yaxis_title="% de Contribuição para as Vendas"
)

# preencher a área abaixo da curva
fig.add_shape(
    type="rect",
    xref="x",
    yref="y",
    x0=0,
    y0=0,
    x1=358,
    y1=top_ordersbyvalue_cities["Cum % of Total Payments"][357],
    fillcolor="green",
    opacity=0.3,
    layer="below",
    line_width=0
)

# adicionar um texto ao gráfico
fig.add_annotation(
    x=1000,
    y=70,
    text="358 cidades (+-8,7% do total) <br>contribuem para +-80% das vendas.",
    font=dict(
        size=14,
        color="black"
    ),
    showarrow=False
)

# exibir o gráfico
fig.show()

print("Número de cidades que contribuem com 80% das vendas totais:",
      len(top_ordersbyvalue_cities[top_ordersbyvalue_cities["Cum % of Total Payments"] <= 80]),
      "ou em in %:",
      (len(top_ordersbyvalue_cities[top_ordersbyvalue_cities["Cum % of Total Payments"] <= 80]) / len(top_ordersbyvalue_cities)) * 100)



# Total de pedidos por hora e dia da semana
# Mas antes precisamos converter as colunas de datas para datetime
datesCols = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", 
            "order_delivered_customer_date", "order_estimated_delivery_date", "shipping_limit_date", 
            "review_creation_date", "review_answer_timestamp"]

for col in datesCols:
    data[col] = pd.to_datetime(data[col])

    # Orders by hour
orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"])
orderbyhour = orders_df.groupby(orders_df["order_purchase_timestamp"].dt.hour)["order_id"].count().reset_index().sort_values(by="order_purchase_timestamp", ascending=False)
orderbyhour.rename(columns={"order_id":"Total Orders", "order_purchase_timestamp": "Hour of Day"}, inplace=True)

fig = px.bar(orderbyhour, x='Hour of Day', y='Total Orders', title='Número de pedidos por hora do dia')
fig.update_xaxes(title='Hora do dia')
fig.update_yaxes(title='Número total de pedidos')
fig.show()

# Orders by day of the week
orderbydow = data.groupby(data["order_purchase_timestamp"].dt.day_name())["order_id"].count().reset_index()
orderbydow.rename(columns={"order_id":"Total Orders", "order_purchase_timestamp": "Weekday Name"}, inplace=True)
orderbydow = orderbydow.sort_values(by="Total Orders", ascending=False)

fig = px.bar(orderbydow, x='Weekday Name', y='Total Orders', title='Número de pedidos por dia da semana')
fig.update_xaxes(title='Dia da semana')
fig.update_yaxes(title='Número total de pedidos')
fig.show()

# Define a ordem dos dias da semana
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Converte a coluna "Weekday Name" em uma categoria ordenada
weekday = pd.Categorical(orderbydow['Weekday Name'], categories=weekday_order, ordered=True)

# Cria um novo dataframe ordenado pela coluna de categoria "weekday"
orderbydow_ordered = orderbydow.assign(weekday=weekday).sort_values('weekday')

# Cria um gráfico de barras com os dias da semana em ordem
fig = px.bar(orderbydow_ordered, x='weekday', y='Total Orders', title='Número de pedidos por dia da semana')
fig.update_xaxes(title='Dia da semana')
fig.update_yaxes(title='Número total de pedidos')
fig.show()


reviewsocres = data.groupby("product_category_name")["review_score"].agg(["mean", "count"]).sort_values(by="mean",ascending=False)
bestrated = reviewsocres[reviewsocres["count"]>=30][:10]

fig = go.Figure(go.Bar(
            x=bestrated['mean'],
            y=bestrated.index,
            orientation='h'))

fig.update_layout(
    title='Melhores avaliações',
    xaxis_title='Avaliação média',
    yaxis_title='Categoria do produto',
    height=600,
    width=800,
    margin=dict(l=100, r=20, t=50, b=50),
)

fig.show()


reviewsocres = data.groupby("product_category_name")["review_score"].agg(["mean", "count"]).sort_values(by="mean",ascending=False)
worstrated = reviewsocres[reviewsocres["count"]>=30].sort_values(by='mean')[:10]

fig = go.Figure(go.Bar(
            x=worstrated['mean'],
            y=worstrated.index,
            orientation='h'))

fig.update_layout(
    title='Produtos com as piores avaliações',
    xaxis_title='Avaliação média',
    yaxis_title='Categoria do produto',
    height=600,
    width=800,
    margin=dict(l=100, r=20, t=50, b=50),
)

fig.show()

# Por exemplo: o pagamento em dinheiro aumenta o cancelamento de pedidos?
cashvscancel = pd.crosstab(data["payment_type"], data["order_status"])
cashvscancel = cashvscancel[["canceled", "delivered"]]
cashvscancel["% Canceled"] = (cashvscancel["canceled"] / cashvscancel["delivered"] ) * 100
cashvscancel["Avg Cancelation Rate"] = (len(data[data["order_status"] == "canceled"]) / len(data[data["order_status"] == "delivered"])) * 100
cashvscancel

##Existe alguma relação entre o tempo de entrega e as pontuações das avaliações?
# Adicionando uma coluna delta que calcula o tempo que levou para o pedido ser entregue
data["TimeToDeliveryinHours"] = (data["order_delivered_customer_date"] - data["order_purchase_timestamp"])
data["TimeToDeliveryinHours"] = data["TimeToDeliveryinHours"].apply(lambda x: x.total_seconds())
data["TimeToDeliveryinHours"] = round((data["TimeToDeliveryinHours"] / 3600) / 24, 2)
data.rename(columns={"TimeToDeliveryinHours" : "TimeToDeliveryinDays"}, inplace=True)

# Principais estatísticas do tempo de entrega
data[["TimeToDeliveryinDays"]].describe()


# Define a ordem crescente dos valores da pontuação de avaliação
score_order = sorted(data['review_score'].unique())

# Converte a coluna "review_score" em uma categoria ordenada
score = pd.Categorical(data['review_score'], categories=score_order, ordered=True)

# Cria um novo dataframe ordenado pela coluna de categoria "score"
data_ordered = data.assign(score=score).sort_values('score')

# Cria um seletor de pontuação de avaliação em ordem crescente
fig = px.box(data_ordered, x='score', y='TimeToDeliveryinDays', color='score',
             title='Relação entre a pontuação da avaliação e o tempo de entrega')

fig.update_xaxes(title='Pontuação da avaliação')
fig.update_yaxes(title='Tempo de entrega (dias)')

fig.show()


# Define o limite superior dos valores
q_high = data["TimeToDeliveryinDays"].quantile(0.95)

# Cria um novo dataframe sem os valores atípicos
data_no_outliers = data[data["TimeToDeliveryinDays"] < q_high]

# Define a ordem crescente dos valores da pontuação de avaliação
score_order = sorted(data_no_outliers['review_score'].unique())

# Converte a coluna "review_score" em uma categoria ordenada
score = pd.Categorical(data_no_outliers['review_score'], categories=score_order, ordered=True)

# Cria um novo dataframe com a coluna de categoria "score"
data_score = data_no_outliers.assign(score=score)

data_score = data_score.assign(score=score).sort_values('score')

# Cria um seletor de pontuação de avaliação em ordem crescente
fig = px.box(data_score, x='score', y='TimeToDeliveryinDays', color='score',
             title='Relação entre a pontuação da avaliação e o tempo de entrega')

fig.update_xaxes(title='Pontuação da avaliação', categoryorder='array', categoryarray=score_order)
fig.update_yaxes(title='Tempo de entrega (dias)')

fig.show()


# Vendedores com melhor tempo de entrega
sellersdeliverytime = data.groupby("seller_city")["TimeToDeliveryinDays"].agg(["min", "max", "mean", "std", "count" ]).dropna().sort_values("mean").reset_index()
# Filtro para vendedores com 30 ou mais pedidos em seu histórico
sellersdeliverytime = sellersdeliverytime[sellersdeliverytime["count"]>=30]

fastestdeliverysellers = sellersdeliverytime[:10]
slowestdeliverysellers = sellersdeliverytime.sort_values("mean", ascending=False)[:10]

# Vendedores com entrega mais rápida.
fastestdeliverysellers

# Vendedores com entrega mais lenta.
slowestdeliverysellers

# Junte a pontuação média de avaliação à tabela acima.
avg_review_score_seller = data.groupby("seller_city")["review_score"].mean().dropna().sort_values(ascending=False).reset_index()

sellerPerf = sellersdeliverytime.merge(avg_review_score_seller, on="seller_city")

# Gráfico de regressão linear entre a média de tempo de entrega e a média da pontuação de avaliação
fig = px.scatter(sellerPerf, x='mean', y='review_score', trendline='ols', 
                 title='Relação entre a média de tempo de entrega e a média da pontuação de avaliação')

fig.update_xaxes(title='Média de tempo de entrega (dias)')
fig.update_yaxes(title='Média da pontuação de avaliação')

fig.show()


# Top 10 estados com o maior tempo médio de entrega
highestTTDstates = data.groupby("customer_state")["TimeToDeliveryinDays"].mean().dropna().sort_values(ascending=False).reset_index()
highestTTDstates = highestTTDstates[:10]

# Gráfico de barras com o tempo médio de entrega por estado
fig = px.bar(highestTTDstates, x='TimeToDeliveryinDays', y='customer_state',
             orientation='h', title='Top 10 estados com o maior tempo médio de entrega')

fig.update_yaxes(title='Estado')
fig.update_xaxes(title='Tempo médio de entrega (dias)')

fig.show()


# Top 10 estados com o menor tempo médio de entrega
lowestTTDstates = data.groupby("customer_state")["TimeToDeliveryinDays"].mean().dropna().sort_values(ascending=True).reset_index()
lowestTTDstates = lowestTTDstates[:10]

# Gráfico de barras com o tempo médio de entrega por estado
fig = px.bar(lowestTTDstates, x='TimeToDeliveryinDays', y='customer_state',
             orientation='h', title='Top 10 estados com o menor tempo médio de entrega')

fig.update_yaxes(title='Estado')
fig.update_xaxes(title='Tempo médio de entrega (dias)')

fig.show()


# Mediana do tempo de entrega por ano
deliverytimevstime = data.groupby(data["order_purchase_timestamp"].dt.year)["TimeToDeliveryinDays"].median().dropna()

# Converte ano em categoria (e não um número)
deliverytimevstime.index = deliverytimevstime.index.astype(str)

# Gráfico de barras com a mediana do tempo de entrega por ano
fig = px.bar(deliverytimevstime, x=deliverytimevstime.index, y='TimeToDeliveryinDays',
             title='Mediana do tempo de entrega por ano')

fig.update_xaxes(title='Ano')
fig.update_yaxes(title='Mediana de entrega em dias')

fig.show()


# Média da pontuação da avaliação por ano
scorevstime = data.groupby(data["order_purchase_timestamp"].dt.year)["review_score"].mean().dropna()

# Converte o índice do grupo em uma categoria
scorevstime.index = scorevstime.index.astype(str)

# Gráfico de barras com a média da pontuação da avaliação por ano
fig = px.bar(scorevstime, x=scorevstime.index, y='review_score',
             title='Média da pontuação da avaliação por ano')

fig.update_xaxes(title='Ano')
fig.update_yaxes(title='Pontuação média da avaliação')

fig.show()

print('---------------------------------------------------')

top_categ_by_revenue = data.groupby("product_category_name").agg({'order_id':'nunique','payment_value':'sum'}).sort_values("payment_value", ascending=False)[:10]
top_categ_by_revenue.rename(columns={"order_id":"NumOfOrders", "payment_value":"Revenues"}, inplace=True)

top_categ_by_revenue



# Agrupar os dados por estado e obter a média do tempo de entrega
mean_delivery_time_by_state = data.groupby('customer_state')['TimeToDeliveryinDays'].mean().reset_index()

mean_delivery_time_by_state

#geopandas

print('--------------------------------------------------')


geojson_file = './gis-dataset-brasil-master/uf/geojson/uf.json'
geojson_data = gpd.read_file(geojson_file)
geojson_data.head(10)

geojson_data['tempo_entrega'] = mean_delivery_time_by_state['TimeToDeliveryinDays']

geojson_data.head()

fig = px.choropleth_mapbox(geojson_data, 
                           geojson=geojson_data.geometry, 
                           locations=geojson_data.index, 
                           color='tempo_entrega',
                           color_continuous_scale='YlOrRd',
                           mapbox_style='open-street-map',
                           zoom=3, center={'lat': -15.788497, 'lon': -47.879873},
                           opacity=0.5)

fig.show()
