## Imports
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from parse_input import parse_input_directory
from parse_input import get_df_data_from_date
from parse_input import offset_df_column_date

from dash.dependencies import Input, Output
from dash_table import DataTable

import pandas as pd

import plotly
import plotly.graph_objects as go
import plotly.express as px

df = parse_input_directory()
df['id'] = df.index

df_data_trade = pd.DataFrame()
df_data_stock = pd.DataFrame()

app = dash.Dash()

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}



app.layout = html.Div([

        dash_table.DataTable(
            id='trade-row-ids',
            data=df.to_dict('records'),
            #  columns=[{"name": i, "id": i} for i in df.columns],
            sort_action='native',
            row_selectable='single',
            selected_rows=[0],
            #style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
            # style_cell={'textAlign': 'center'},
            # style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            # style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
            columns=[
                {'name': 'date', 'id': 'date', 'type': 'any', 'editable': False},
                {'name': 'iter', 'id': 'iter', 'type': 'numeric', 'editable': False},
                {'name': '$_daily', 'id': '$_daily', 'type': 'numeric', 'editable': False},
                {'name': '%_daily', 'id': '%_daily', 'type': 'numeric', 'editable': False},
                {'name': '$_max', 'id': '$_max', 'type': 'numeric', 'editable': False},
                {'name': '%_max', 'id': '%_max', 'type': 'numeric', 'editable': False},
                {'name': '$_min', 'id': '$_min', 'type': 'numeric', 'editable': False},
                {'name': '%_min', 'id': '%_min', 'type': 'numeric', 'editable': False},
                {'name': '$_mean', 'id': '$_mean', 'type': 'numeric', 'editable': False},
                {'name': '%_mean', 'id': '%_mean', 'type': 'numeric', 'editable': False},
            ],
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{%_daily} < 100',
                        'column_id': '%_daily'
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_daily} > 100  && {%_daily} < 100.5',
                        'column_id': '%_daily'
                    },
                    'backgroundColor': 'dodgerblue',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_daily} > 100.5',
                        'column_id': '%_daily'
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_daily} > 100',
                        'column_id': '%_daily'
                    },
                    'backgroundColor': 'dodgerblue',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_max} < 100.05',
                        'column_id': '%_max'
                    },
                    'backgroundColor': 'red',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_max} > 100.05 && {%_max} < 100.1',
                        'column_id': '%_max'
                    },
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_max} > 100.1',
                        'column_id': '%_max'
                    },
                    'backgroundColor': 'dodgerblue',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{%_max} > 100.5',
                        'column_id': '%_max'
                    },
                    'backgroundColor': 'green',
                    'color': 'white'
                },
                {
                    'if': {
                        'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
                    },
                    'textAlign': 'left'
                },
            ]
        ),

        html.Div(id="group_PF_asset_graph_1", children=[

                html.Div(dcc.Graph(id="display_PF_asset_graph_1", ),
                         style={'display': 'inline-block', 'width': '68%'}, ),

                html.Div(dcc.Graph(id="display_PF_asset_graph_2", ),
                         style={'display': 'inline-block', 'width': '30%'}, ),
        ], style={'display': 'inline-block', 'width': '100%'}
                 ),

        html.Div(id="group_PF_asset_graph_2", children=[

            html.Div(dcc.Graph(id="display_PF_asset_graph_3", ),
                     style={'display': 'inline-block', 'width': '48%'}, ),

            html.Div(dcc.Graph(id="display_PF_asset_graph_4", ),
                     style={'display': 'inline-block', 'width': '48%'}, ),
        ], style={'display': 'inline-block', 'width': '100%'}
                 ),

        DataTable(
            id='stock-row-ids',
            row_selectable='single',
            selected_rows=[0],
            # style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'textAlign': 'center', 'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
            columns = [
                {'name': 'date', 'id': 'date', 'type': 'any', 'editable': False},
                {'name': 'tic', 'id': 'tic', 'type': 'numeric', 'editable': False},
                {'name': 'open', 'id': 'open', 'type': 'numeric', 'editable': False},
                {'name': 'close', 'id': 'close', 'type': 'numeric', 'editable': False},
                {'name': 'trend', 'id': 'trend', 'type': 'any', 'editable': False},
                {'name': 'high', 'id': 'high', 'type': 'numeric', 'editable': False},
                {'name': 'low', 'id': 'low', 'type': 'numeric', 'editable': False},
                {'name': 'earning', 'id': 'earning', 'type': 'numeric', 'editable': False},
            ],
            data=[],
            sort_action='native',
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{earning} > 0',
                        'column_id': 'earning'
                    },
                    'backgroundColor': 'blue',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{earning} < 0',
                        'column_id': 'earning'
                    },
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{trend} = "up"',
                        'column_id': 'trend'
                    },
                    'backgroundColor': 'blue',
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{trend} = "down"',
                        'column_id': 'trend'
                    },
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
            ]
        ),

        html.Div(id="group_STK_asset_graph_1", children=[

            html.Div(dcc.Graph(id="display_STK_asset_graph_1", ),
                     style={'display': 'inline-block', 'width': '31%'}, ),

            html.Div(dcc.Graph(id="display_STK_asset_graph_2", ),
                     style={'display': 'inline-block', 'width': '31%'}, ),

            html.Div(dcc.Graph(id="display_STK_asset_graph_3", ),
                     style={'display': 'inline-block', 'width': '31%'}, ),

        ], style={'display': 'inline-block', 'width': '100%'}
                 ),


    ]
)

@app.callback(
    [Output("display_PF_asset_graph_1", "figure"),
     Output("display_PF_asset_graph_2", "figure"),
     Output("display_PF_asset_graph_3", "figure"),
     Output("display_PF_asset_graph_4", "figure"),
     Output("stock-row-ids", "data"), ],
     Input('trade-row-ids', 'derived_viewport_selected_row_ids'),)
def update_graphs(row_ids):

    global df
    global df_data_trade
    global df_data_stock

    while True:
        try:
            id = row_ids[0]
            break
        except TypeError:
            id = 0
            break

    id_stk = 0

    date = df["date"][id]

    df_data, df_stocks_table = get_df_data_from_date(date)

    df_data_trade = df_data
    df_data_stock = df_stocks_table
    df_data_stock['id'] = df_data_stock.index

    #ticker = df_stocks_table["tic"][id_stk]

    table_data = df_stocks_table.to_dict('records')

    fig_PF_account = px.line(df_data, x="date",
                             y=['account_$', 'stocks_$', 'total_$'])

    fig_PF_tot_val = px.line(df_data, x="date",
                             y=['total_$', "profit_0.05", "profit_0.1", "profit_0"])

    fig_reward = px.bar(df_data, x="date",
                        y=['reward_$'])

    fig_sum_stock = px.bar(df_data, x="date",
                           y=['sum'])

    return fig_PF_tot_val, fig_PF_account, fig_reward, fig_sum_stock, table_data



@app.callback(
    [Output("display_STK_asset_graph_1", "figure"),
     Output("display_STK_asset_graph_2", "figure"),
     Output("display_STK_asset_graph_3", "figure"),],
#     Input('stock-row-ids', 'derived_viewport_selected_row_ids'),)
    Input('stock-row-ids', 'selected_row_ids'), )
def update_graphs(row_ids):

    global df_data_trade
    global df_data_stock

    while True:
        try:
            id = row_ids[0]
            break
        except TypeError:
            id = 0
            break

#    if row_ids is None:
#        id = 0
        # pandas Series works enough like a list for this to be OK
        #row_ids = df['id']
#    else:
        #dff = df.loc[row_ids]
#        id = 0

    df_stk = df_data_stock.copy()
    df_trd = df_data_trade.copy()

    ticker = df_stk["tic"][id]

    clnm_val = ticker + "_val_$"
    clnm_flow = ticker + "_flow_$"
    clnm_nb = ticker + "_nb"

    df_trd , df_trd_val = offset_df_column_date(df_trd, clnm_val, clnm_flow, clnm_nb)

    fig_STK_val = px.line(df_trd, x="date", y=[clnm_val])

    #fig_STK_flow = px.bar(df_trd_val, x="date", y=[clnm_flow, clnm_nb], barmode="group")

    fig_STK_flow = px.bar(df_trd_val, x="date", y=[clnm_flow])

    fig_STK_nb = px.bar(df_trd_val, x="date", y=[clnm_nb])

    return fig_STK_val, fig_STK_flow, fig_STK_nb


