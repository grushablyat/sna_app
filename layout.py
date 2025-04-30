from textwrap import dedent as d

import dash
from dash import dcc
from dash import html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

layout = html.Div([
    ###################################### Заголовок ######################################
    html.Div(
        id='title',
        className='row',
        children=[html.H1('Анализ дружеских связей пользователя ВК')],
        style={'textAlign': 'center'},
    ),
    ###################################### Главный ряд ######################################
    html.Div(
        id='main-row',
        className='row',
        children=[
            ###################################### Левая панель ######################################
            html.Div(
                id='left-bar',
                className='three columns',
                children=[
                    ###################################### Target user ID section ######################################
                    html.Div(
                        id='target-user-id-section',
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d('''
                            **ID пользователя**
        
                            Укажите идентификатор интересуемого пользователя ВК:
                            ''')),
                            dcc.Input(
                                id='target-user-id-input',
                                type='number',
                                min=0, max=10000000000,
                                placeholder='Введите ID',
                                className='twelve columns',
                            ),
                            html.Br(),
                            html.Button(
                                'Начать анализ',
                                id='target-user-id-button',
                                n_clicks=0,
                                className='twelve columns'
                            ),
                            dcc.Markdown(
                                id='target-user-id-error',
                                style={'color': 'red'},
                            ),
                        ],
                        style={'height': '250px'},
                    ),
                    ###################################### Analyzer section ######################################
                    html.Div(
                        id='analyzer-section',
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d('''
                            **Анализ связей**
                            ''')),
                            html.Button(
                                'Вычислить центральности',
                                id='calculate-centralities-button',
                                className='twelve columns',
                                n_clicks=0,
                            ),
                            html.Button(
                                'Обнаружить сообщества',
                                id='detect-communities-button',
                                className='twelve columns',
                                n_clicks=0,
                            ),
                        ],
                        style={'height': '250px'},
                    ),
                    ###################################### Options section ######################################
                    html.Div(
                        id='options-section',
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d('''
                            **Опции**
                            
                            Выберите необходимые опции:
                            ''')),
                            dcc.Checklist(
                                id='options-checklist',
                                options={
                                    'labels': 'Подписи узлов графа (ID пользователей)',
                                    'communities': 'Выделение обнаруженных сообществ'
                                },
                                value=['labels', 'communities'],
                            ),
                            html.Button(
                                'Обновить граф',
                                id='apply-graph-options-button',
                                className='twelve columns',
                                n_clicks=0,
                            )
                        ],
                        style={'height': '250px'},
                    ),
                ],
            ),

            ###################################### Граф в центре ######################################
            html.Div(
                className='five columns',
                children=[
                    html.Div(
                        className='twelve columns',
                        children=[
                            html.H3('Граф дружеских связей'),
                        ],
                        style={'textAlign': 'center'},
                    ),
                    # dcc.Tabs(
                    #     className='twelve columns',
                    #     id='central-graph-tabs',
                    #     value='tab-1-nx-image',
                    #     children=[
                    #         dcc.Tab(
                    #             ###################################### Изображение графа ######################################
                    #             className='twelve columns',
                    #             label='Image',
                    #             value='tab-1-nx-image',
                    #             children=[
                                    html.Div(
                                        className='twelve columns',
                                        children=[
                                            html.Img(
                                                id='graph-image',
                                                # src=dash.get_asset_url('network_graph.png'),
                                                src=None,
                                                alt='image',
                                                className='twelve columns',
                                            )
                                        ]
                                    ),
                    #             ]
                    #         ),
                    #         dcc.Tab(
                    #             ###################################### Интерактивный граф ######################################
                    #             ### Don't sure if we need to create interactive graph, but may be ###
                    #             #####################################################################
                    #             className='twelve columns',
                    #             label='Interactive Graph',
                    #             value='tab-2-interactive-graph',
                    #             children=[
                    #                 dcc.Graph(
                    #                     className='twelve columns',
                    #                     id='interactive-graph',
                    #                     # figure=network_graph(YEAR, ACCOUNT)),
                    #                     figure=None,
                    #                 ),
                    #             ]
                    #         )
                    #     ]
                    # ),
                ]
            ),

            ###################################### Таблица справа ######################################
            html.Div(
                className='four columns',
                children=[
                    # dash.dash_table.DataTable(pd.read_csv('network_metrics.csv').to_dict('records'), id='metrics-table')
                    dash.dash_table.DataTable(None, id='metrics-table')

                    ### There will be tabs with metrics
                    ### Every tab will contain button to calculate a metric and table of top nodes by current metric
                    ### Button click callback function will update table
                ]
            )
        ]
    )
])
