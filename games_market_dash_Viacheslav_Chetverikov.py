import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output


# Исходный код
df = pd.read_csv('games.csv')

# Исключим из данных проекты, для которых имеются пропуски данных в любой из колонок
df.dropna(inplace=True)


# Исключим из данных проекты ранее 2000 года:
df = df[df.Year_of_Release >= 2000]


app = dash.Dash()


app.layout = html.Div([




    html.Div([
        html.Div([
             html.H2('Cостояние игровой индустрии', style={
                 "margin-bottom": "0px", 'color': '#21135c'})


             ], className="header_seven_columns",
        ),


        html.Div([
            html.Img(src="/assets/games.jpeg",
                 style={"width": "50%",  "border-radius": "100px"})

        ], className="header_five_columns",
        ),
    ], className="row flex-display"),





    html.Div([


        html.H6(
            'Дашборд отражает характеристики игровых проектов, начиная с 2000 года 💫'),
        html.P('С помощью фильтров возможно выбрать интересующий жанр, рейтинг и интервал годов выпуска. Визуализации показывают выпуск игр по годам и платформам, а также оценки игроков и критиков (их может быть больше чем количество уникальных игр, так как оценки также различаются в зависимости от платформы игры).         Количество значений фильтра жанра рейтинга зависит от выбранного жанра игры.')


    ], style={"margin-bottom": "15px"}),







    html.Div([
        html.Div([
            html.H6(children='Выберите жанр 💬',
                    style={
                        'textAlign': 'center',
                        'color': '#21135c',
                        "margin-top": "-5px"}
                    ),



            dcc.Dropdown(id='genre',
                         multi=False,
                         clearable=False,
                         value='Role-Playing',
                         placeholder='Не указан жанр',
                         options=[{'label': c, 'value': c}
                                  for c in (df['Genre'].unique())], className='dcc_compon')


        ], className="card_container six columns",
        ),


        html.Div([
            html.H6(children='Выберите рейтинг 📊',
                    style={
                        'textAlign': 'center',
                        'color': '#21135c',
                        "margin-top": "-5px"}
                    ),



            dcc.Dropdown(
                id='rating',
                multi=False,
                clearable=False,
                value='M',
                placeholder='Не указан рейтинг',
                options=[], className='dcc_compon'

            ),

        ], className="card_container six columns",
        ),
    ], className="row flex-display"),



    html.Div([
        html.Div([



            html.P('Количество уникальных игр',
                   className='fix_label',
                   style={
                       'textAlign': 'center',
                       'color': '#800080',
                       'fontSize': 16}),




            html.P(className='fix_label',
                   id="games_count",
                   style={'textAlign': 'center',
                          "margin-top": "-10px",
                          'color': '#21135c'}),







        ], className="create_container six columns"),

        html.Div([
            html.P(),
        ], className="six columns"),

    ], className="row flex-display"),








    html.Div([



        html.Div([
            dcc.Graph(id='stacked_area',
                      config={'displayModeBar': 'hover'}),
        ], className="create_container six columns"),


        html.Div([
            dcc.Graph(id="scatter_plot")

        ], className="create_container six columns"),

    ], className="row flex-display"),






    html.Div([
        html.Div([
            html.P('Интервал годов выпуска 🕒', className='fix_label', style={
                'color': '#800080', 'margin-right': '1%', "margin-bottom": "10px"}),
            dcc.RangeSlider(id='select_years',
                            min=2000,
                            max=2016,
                            dots=False,
                            value=[2000, 2016],
                            marks={str(yr): str(yr) for yr in range(2000, 2016, 2)}),


        ], className="create_container six columns"),


        html.Div([
            html.P(),
        ], className="six columns"),

    ], className="row flex-display"),







])


# Зависимость значения фильтра рейтинга от жанра

@app.callback(
    Output('rating', 'options'),
    Input('genre', 'value'))
def get_country_options(genre):
    df_upd = df[df['Genre'] == genre]
    return [{'label': i, 'value': i} for i in df_upd['Rating'].unique()]


# Значение рейтинга по умолчанию

@app.callback(
    Output('rating', 'value'),
    Input('rating', 'options'))
def get_country_value(rating):
    return [k['value'] for k in rating][0]

    # Количество выбранных игр


@app.callback(Output('games_count', 'children'),
              [Input('genre', 'value')],
              [Input('rating', 'value')],
              [Input('select_years', 'value')])
def update_games_count(genre, rating, select_years):
    # Подставляем значения
    df_games = df[(df['Genre'] == genre) & (df['Rating'] == rating)
                  & (df['Year_of_Release'] >= select_years[0]) & (df['Year_of_Release'] <= select_years[1])]

    # Возвращаем количество уникальных игр
    return df_games['Name'].nunique()

  # Scatter Plot


@app.callback(Output('scatter_plot', 'figure'),
              [Input('genre', 'value')],
              [Input('rating', 'value')],
              [Input('select_years', 'value')])
def update_graph(genre, rating, select_years):
    df_upd1 = df[(df['Genre'] == genre) & (df['Rating'] == rating)
                 & (df['Year_of_Release'] >= select_years[0]) & (df['Year_of_Release'] <= select_years[1])]

    return {
        'data': [
            go.Scatter(
                name='Sports',
                x=df_upd1[df_upd1['Genre'] == 'Sports']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Sports']['Critic_Score'],
                mode='markers'
            ),

            go.Scatter(
                name='Racing',
                x=df_upd1[df_upd1['Genre'] == 'Racing']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Racing']['Critic_Score'],
                mode='markers'
            ),

            go.Scatter(
                name='Misc',
                x=df_upd1[df_upd1['Genre'] == 'Misc']['User_Score'],
                y=df_upd1[df_upd1['Genre'] == 'Misc']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Platform',
                x=df_upd1[df_upd1['Genre'] ==
                          'Platform']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Platform']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Action',
                x=df_upd1[df_upd1['Genre'] == 'Action']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Action']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Puzzle',
                x=df_upd1[df_upd1['Genre'] == 'Puzzle']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Puzzle']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Shooter',
                x=df_upd1[df_upd1['Genre'] == 'Shooter']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Shooter']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Fighting',
                x=df_upd1[df_upd1['Genre'] ==
                          'Fighting']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Fighting']['Critic_Score'],
                mode='markers'
            ),



            go.Scatter(
                name='Simulation',
                x=df_upd1[df_upd1['Genre'] ==
                          'Simulation']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Simulation']['Critic_Score'],
                mode='markers'
            ),



            go.Scatter(
                name='Role-Playing',
                x=df_upd1[df_upd1['Genre'] ==
                          'Role-Playing']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Role-Playing']['Critic_Score'],
                mode='markers'
            ),



            go.Scatter(
                name='Adventure',
                x=df_upd1[df_upd1['Genre'] ==
                          'Adventure']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Adventure']['Critic_Score'],
                mode='markers'
            ),


            go.Scatter(
                name='Strategy',
                x=df_upd1[df_upd1['Genre'] ==
                          'Strategy']['User_Score'],
                y=df_upd1[df_upd1['Genre'] ==
                          'Strategy']['Critic_Score'],
                mode='markers'
            )

        ],

        'layout': go.Layout(
            title='Оценки игроков и критиков',
            xaxis={'title': 'Оценка игроков'},
            yaxis={'title': 'Оценка критиков'},
            hovermode='closest'),

    }


# Stacked area plot
@app.callback(Output('stacked_area', 'figure'),
              [Input('rating', 'value')],
              [Input('genre', 'value')],
              [Input('select_years', 'value')])
def update_graph(rating, genre, select_years):
    st = df.groupby(['Year_of_Release', 'Platform', 'Genre', 'Rating'])[
        'Name'].nunique().reset_index()
    st = st[(st['Genre'] == genre) & (st['Rating'] == rating)
            & (st['Year_of_Release'] >= select_years[0]) & (df['Year_of_Release'] <= select_years[1])]

    return {

        'data': [
            go.Scatter(
                name='PS2',
                x=st[st['Platform'] == 'PS2']['Year_of_Release'],
                y=st[st['Platform'] == 'PS2']['Name'],
                type='scatter',
                stackgroup='one'
            ),


            go.Scatter(
                name='X360',
                x=st[st['Platform'] == 'X360']['Year_of_Release'],
                y=st[st['Platform'] == 'X360']['Name'],
                type='scatter',
                stackgroup='one'
            ),

            go.Scatter(
                name='PS3',
                x=st[st['Platform'] == 'PS3']['Year_of_Release'],
                y=st[st['Platform'] == 'PS3']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='DS',
                x=st[st['Platform'] == 'DS']['Year_of_Release'],
                y=st[st['Platform'] == 'DS']['Name'],
                stackgroup='one'
            ),


            go.Scatter(
                name='XB',
                x=st[st['Platform'] == 'XB']['Year_of_Release'],
                y=st[st['Platform'] == 'XB']['Name'],
                stackgroup='one'
            ),



            go.Scatter(
                name='PC',
                x=st[st['Platform'] == 'PC']['Year_of_Release'],
                y=st[st['Platform'] == 'PC']['Name'],
                stackgroup='one'
            ),



            go.Scatter(
                name='Wii',
                x=st[st['Platform'] == 'Wii']['Year_of_Release'],
                y=st[st['Platform'] == 'Wii']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='PSP',
                x=st[st['Platform'] == 'PSP']['Year_of_Release'],
                y=st[st['Platform'] == 'PSP']['Name'],
                stackgroup='one'
            ),


            go.Scatter(
                name='GC',
                x=st[st['Platform'] == 'GC']['Year_of_Release'],
                y=st[st['Platform'] == 'GC']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='GBA',
                x=st[st['Platform'] == 'GBA']['Year_of_Release'],
                y=st[st['Platform'] == 'GBA']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='PS4',
                x=st[st['Platform'] == 'PS4']['Year_of_Release'],
                y=st[st['Platform'] == 'PS4']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='3DS',
                x=st[st['Platform'] == '3DS']['Year_of_Release'],
                y=st[st['Platform'] == '3DS']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='XOne',
                x=st[st['Platform'] == 'XOne']['Year_of_Release'],
                y=st[st['Platform'] == 'XOne']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='PSV',
                x=st[st['Platform'] == 'PSV']['Year_of_Release'],
                y=st[st['Platform'] == 'PSV']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='PS',
                x=st[st['Platform'] == 'PS']['Year_of_Release'],
                y=st[st['Platform'] == 'PS']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='WiiU',
                x=st[st['Platform'] == 'WiiU']['Year_of_Release'],
                y=st[st['Platform'] == 'WiiU']['Name'],
                stackgroup='one'
            ),

            go.Scatter(
                name='DC',
                x=st[st['Platform'] == 'DC']['Year_of_Release'],
                y=st[st['Platform'] == 'DC']['Name'],
                stackgroup='one'
            )




        ],


        'layout': go.Layout(
            title='Выпуск игр по годам и платформам',
            xaxis={'title': 'Год'},
            yaxis={'title': 'Количество игр'},
            hovermode='x unified'
        )


    }


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
