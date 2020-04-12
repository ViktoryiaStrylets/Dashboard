# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly
import plotly.graph_objects as go
import numpy as np
#Load dataset
HOUSING_URL = "/Users/vikus/Documents/SBU\CSE332/ames_housing_data.csv"

original= pd.read_csv(HOUSING_URL)
features = ["SID","Neighborhood","OverallCond","YearBuilt","YearRemodel","YrSold","FullBath","SalePrice","GrLivArea","GarageArea","TotRmsAbvGrd","TotalBsmtSF"]
feat =["OverallCond","GrLivArea","YearBuilt","YearRemodel","TotalBsmtSF","SalePrice","GarageArea","TotRmsAbvGrd","YrSold","FullBath"]

df = original.filter(features, axis=1)
df.dropna(axis=0,inplace=True)
colors = {
    "background": "#f0f5f5",
    'text': '#999F'
}

#initialize the app
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[


    html.H1(
        children='Data Visualization',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Various Visualization Techniques to understand your data better', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(
        dcc.Dropdown(
            id='crossfilter-axis-column',
            options=[{'label': i, 'value': i} for i in df],
            value="YearBuilt",
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}

        ), ),

    html.Div([
        #first column
        html.Div([
            dcc.Graph(
                id='hist-graph',
#
            )],className="six columns"),

        #second column
        html.Div([
            dcc.Graph(id = "parallel coordinates",

                      )
        ],className="six columns")
    ],className="row"),

    html.Div([

        html.Div([
            dcc.Graph(
                id='scatter_plot',
                # hoverData={'points': [{'customdata':'Gilbert'}]}

            )],className="six columns"),

        html.Div([
            dcc.Graph(
                id='heatmap',

   style={"margin-right": "auto", "margin-left": "auto"}
  )], className="six columns"),


    ],className="row")
])


@app.callback(
    dash.dependencies.Output('scatter_plot', 'figure'),
    [dash.dependencies.Input('crossfilter-axis-column', 'value')])
def create_scatter_plot(axis_column_name):
    return {
        'data': [
            dict(
                x=df[df['Neighborhood'] == i][axis_column_name],
                y=df[df['Neighborhood'] == i]['SalePrice'],
                text=df['Neighborhood'],
                customdata=df['Neighborhood'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.Neighborhood.unique()
        ],

        'layout': dict(
            title="Bivariate Scatterplot",
            xaxis={'type': 'log', 'title': 'YearBuilt'},
            yaxis={'title': 'SalePrice'},
            margin={'l': 60, 'b': 40, 't': 40, 'r': 10},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],

        )

    }
def create_graphs(dff,title):
    return [
        { 'data': [
            {
                'x': dff['YearRemodel'],
                'name': 'Year Remodel',
                'type': 'histogram'
            },
            {
                'x': dff['YearBuilt'],
                'name': 'Year Built',
                'type': "histogram"
            }
        ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'title': title + " Neighborhood(s)",

                'font': {
                    'color': colors['text']
                }
            },
        },

        { 'data':[go.Parcoords(
            line = dict(color = dff['SalePrice'],
                        colorscale = 'Electric',
                        showscale = True,
                        cmin = df['SalePrice'].min(),
                        cmax = df['SalePrice'].max()),
            dimensions = list([
                dict(
                    label ='SalePrice', values = dff['SalePrice'].unique()),
                dict(

                    label = '"OverallCond"', values = df["OverallCond"].unique()),
                dict(

                    label="GrLivArea", values=df["GrLivArea"].unique()),

                dict(

                    label="TotRmsAbvGrd", values=df["TotRmsAbvGrd"].unique()),
                dict(

                    label="YrSold", values=df["YrSold"].unique())
            ])
        )
        ],
            'layout':dict(title = title + " Neighborhood",
                          plot_bgcolor = colors['background'],
                          paper_bgcolor = colors['background'])

        },
        {
            'data':[

                go.Heatmap(x=dff.columns.values[8:], y=dff['Neighborhood'].unique(), z=dff[
        ["GrLivArea","GarageArea","TotRmsAbvGrd","TotalBsmtSF","FullBath"]].values,colorscale='Electric', colorbar={"title": "Square feet"}, showscale=True)
            ],
            "layout": go.Layout( title=title + " Neighborhood",
                                plot_bgcolor = colors['background'],
                                paper_bgcolor = colors['background']
    )
        }]

@app.callback(
    [dash.dependencies.Output('hist-graph', 'figure'),dash.dependencies.Output( "parallel coordinates", 'figure'),dash.dependencies.Output( "heatmap", 'figure')],
    [dash.dependencies.Input('scatter_plot', 'hoverData'),dash.dependencies.Input('scatter_plot', 'selectedData')]
)
def update_histograph(hoverData,selectedData):
    if(hoverData==None and selectedData==None):
        return create_graphs(df, "All")
    if(hoverData!=None):
        neighborhood = hoverData['points'][0]['customdata']
        dff = df[df['Neighborhood']==neighborhood]

    if (selectedData != None):
        for point in selectedData:
            data = point[0]
            # dff = df[df['SalePrice']>data[0] or df['SalePrice']<data[0]]
            print(data[0])
    return create_graphs(dff, neighborhood)

if __name__ == '__main__':
    app.run_server(debug=True)
