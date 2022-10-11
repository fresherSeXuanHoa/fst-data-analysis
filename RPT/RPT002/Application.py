from dash import Dash, html, dcc
from firebase_admin import credentials, firestore

import locale
import pandas as pd
import firebase_admin
import plotly.express as px
import dash_bootstrap_components as dbc

# Configuration for Dash application
dash_app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "Xây Dựng Sản Phẩm Tiềm Năng - Sales - 19520101 - Lê Xuân Hòa"

# Configuration for Firestore application
collection_name = 'tbl-19520101'
fire_store_auth_json = 'iuh-19520101-2f8f0-firebase-adminsdk-if2dg-3e9ecb5869.json'

credential = credentials.Certificate(fire_store_auth_json)
app = firebase_admin.initialize_app(credential)
database = firestore.client()

# Configuration for Heruku
server = dash_app.server

# Load Dataset from Google Fire
sales_firestone_df = pd.DataFrame(list(map((lambda sale : sale.to_dict()), database.collection(collection_name).stream())))
sales_firestone_df["YEAR_ID"] = sales_firestone_df["YEAR_ID"].astype("str")
sales_firestone_df["QTR_ID"] = sales_firestone_df["QTR_ID"].astype("str")
sales_firestone_df["PROFIT"] = sales_firestone_df["SALES"] - (sales_firestone_df["QUANTITYORDERED"] * sales_firestone_df["PRICEEACH"])

# Calculate Some Needed Data
totalSales = round(sum(sales_firestone_df["SALES"]), 2)
totalProfit = round(sum(sales_firestone_df["PROFIT"]), 2)
topSalesByDealSize = sales_firestone_df.groupby("DEALSIZE")["SALES"].apply(sum).sort_values(ascending=False).head(1)
topProfitByDealSize = sales_firestone_df.groupby("DEALSIZE")["PROFIT"].apply(sum).sort_values(ascending=False).head(1)

# Set Location
locale.setlocale( locale.LC_ALL, '' )

# First Figure
sale_by_year_pd = pd.DataFrame({"YEAR_ID": [2003, 2004, 2005], "SALES": sales_firestone_df.groupby("YEAR_ID")["SALES"].apply(sum)})
totalSalesByYearFig = px.bar(sale_by_year_pd, x="YEAR_ID", y="SALES", labels={"YEAR_ID": "Năm", "SALES": "Doanh Số"}, title="Doanh Số Bán Hàng Theo Năm")

# Second Figure
percentSalesByDealSize = px.sunburst(sales_firestone_df, path=['YEAR_ID', 'DEALSIZE'], values='SALES', title='Tỉ Lệ Đóng Góp Của Danh Số Theo Từng Danh Mục Trong Từng Năm')
percentSalesByDealSize.update_traces(textinfo="label + percent parent")
percentSalesByDealSize.update_layout()

# Third Figure
profit_by_year_pd = pd.DataFrame({"YEAR_ID": [2003, 2004, 2005], "PROFIT": sales_firestone_df.groupby("YEAR_ID")["PROFIT"].apply(sum)})
totalProfitByYearFig = px.bar(profit_by_year_pd, x="YEAR_ID", y="PROFIT", labels={"YEAR_ID": "Năm", "PROFIT": "Lợi Nhuận"}, title="Lợi Nhuận Bán Hàng Theo Năm")

# Fourth Figure
percentProfitByDealSize = px.sunburst(sales_firestone_df, path=['YEAR_ID', 'DEALSIZE'], values='PROFIT', title='Tỉ Lệ Đóng Góp Của Lợi Nhuận Theo Từng Danh Mục Trong Từng Năm')
percentProfitByDealSize.update_traces(textinfo="label + percent parent")
percentProfitByDealSize.update_layout()

dash_app.layout = dbc.Container(
    [
        html.Div(
            children=[
                html.Div(
                    children="Xây Dựng Sản Phẩm Tiềm Năng - Sales - 19520101 - Lê Xuân Hòa",
                    className="p-3 bg-primary text-white text-uppercase fw-bold"
                )
            ]),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        children=[
                            html.P(
                                children="Doanh Số Sales",
                                className="h4 p-2 text-black text-uppercase fw-bold"
                            ),
                            html.P(
                                children=(locale.currency(totalSales, grouping=True )),
                                className="p-2 text-danger text-uppercase fw-bold display-6"
                            )
                        ], className='p-2 my-2 bg-white border')
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            html.P(
                                children="Lợi Nhuận",
                                className="h4 p-2 text-black text-uppercase fw-bold"
                            ),
                            html.P(
                                children=(locale.currency(totalProfit, grouping=True )),
                                className="p-2 text-danger text-uppercase fw-bold display-6"
                            )
                        ], className='p-2 my-2 bg-white border')
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            html.P(
                                children="Top Doanh Số",
                                className="h4 p-2 text-black text-uppercase fw-bold"
                            ),
                            html.P(
                                children=(locale.currency(int(topSalesByDealSize), grouping=True )),
                                className="p-2 text-danger text-uppercase fw-bold display-6"
                            )
                        ], className='p-2 my-2 bg-white border')
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            html.P(
                                children="Top Lợi Nhuận",
                                className="h4 p-2 text-black text-uppercase fw-bold"
                            ),
                            html.P(
                                children=(locale.currency(int(topProfitByDealSize), grouping=True )),
                                className="p-2 text-danger text-uppercase fw-bold display-6"
                            )
                        ], className='p-2 my-2 bg-white border')
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children=dcc.Graph(figure=totalSalesByYearFig), className="border"
                ), className='my-2 py-2 '),
                dbc.Col(html.Div(
                    children=dcc.Graph(figure=percentSalesByDealSize), className="border"
                ), className='my-2 py-2')
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    children=dcc.Graph(figure=totalProfitByYearFig), className="border"
                ), className='my-2 py-2'),
                dbc.Col(html.Div(
                    children=dcc.Graph(figure=percentProfitByDealSize), className="border"
                ), className='my-2 py-2 ')
            ]
        )
    ], className="bg-light"
)

if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8090)
