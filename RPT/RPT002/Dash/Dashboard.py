from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# collection_name = 'tbl-19520101'
# fire_store_auth_json = '../conf/auth/iuh-19520101-2f8f0-firebase-adminsdk-if2dg-355b4c424e.json'

# credential = credentials.Certificate(fire_store_auth_json)
# app = firebase_admin.initialize_app(credential)
# database = firestore.client()

dataset_path = '../conf/database/orginal_sales.csv'
sales_firestone_df = pd.read_csv(dataset_path)
sales_firestone_df["YEAR_ID"] = sales_firestone_df["YEAR_ID"].astype("str")
sales_firestone_df["QTR_ID"] = sales_firestone_df["QTR_ID"].astype("str")

app_dash = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

productQuantityFig = px.histogram(sales_firestone_df, x="YEAR_ID", y="QUANTITYORDERED",
                                  barmode="group", color="QTR_ID", title='Tổng số lượng sản phẩm theo quý và năm', histfunc="sum",
                                  labels={'YEAR_ID': 'Các năm 2003, 2004 và 2005', 'QTR_ID': 'Quý trong năm', 'Sum': 'Tổng số lượng sản phẩm'})

saleFig = px.pie(sales_firestone_df, values='SALES', names='YEAR_ID',
                 labels={'YEAR_ID': 'Năm', 'SumSaleQTRYEAR': 'Doanh số'},
                 title='Tổng doanh số theo năm')

billFig = px.sunburst(sales_firestone_df, path=['YEAR_ID', 'QTR_ID'], values='QUANTITYORDERED',
                      color='QUANTITYORDERED',
                      labels={'parent': 'Năm', 'labels': 'Quý',
                              'QUANTITYORDERED': 'Số lượng sản phẩm'},
                      title='Tỉ lệ số lượng sản phẩm theo quý và năm')

app_dash.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=productQuantityFig)
                                        ), className='fig-area'),
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=saleFig)
                                        ), className='fig-area'),
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=billFig)
                                        ), className='fig-area')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=productQuantityFig)
                                        ), className='fig-area')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=saleFig)
                                        ), className='fig-area')
                            ]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=billFig)
                                        ), className='fig-area'),
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=billFig)
                                        ), className='fig-area')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=saleFig)
                                        ), className='fig-area'),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=productQuantityFig)
                                        ), className='fig-area'),
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=saleFig)
                                        ), className='fig-area')
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        children=dcc.Graph(
                                            figure=billFig)
                                        ), className='fig-area'),
                            ]
                        ),
                    ]
                )
            ]
        ),
    ]
)

if __name__ == '__main__':
    app_dash.run_server(debug=True, port=8090)
