import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
import datetime
import warnings


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

data = orders_df.merge(customers_df, on="customer_id").merge(orderitem_df, on="order_id").merge(products_df, on="product_id").merge(categname_df, on="product_category_name").merge(orderpay_df, on="order_id").merge(sellers_df, on="seller_id").merge(orderreviews_df, on="order_id")
print(data.head())
print('......................................')

##Existe alguma relação entre o tempo de entrega e as pontuações das avaliações?
# Adicionando uma coluna delta que calcula o tempo que levou para o pedido ser entregue
data["TimeToDeliveryinHours"] = (data["order_delivered_customer_date"] - data["order_purchase_timestamp"])
data["TimeToDeliveryinHours"] = data["TimeToDeliveryinHours"].apply(lambda x: x.total_seconds())
data["TimeToDeliveryinHours"] = round((data["TimeToDeliveryinHours"] / 3600) / 24, 2)
data.rename(columns={"TimeToDeliveryinHours" : "TimeToDeliveryinDays"}, inplace=True)


mean_delivery_time_by_state = data.groupby('customer_state')['TimeToDeliveryinDays'].mean().reset_index()

mean_delivery_time_by_state


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
