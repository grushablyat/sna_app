from textwrap import dedent as d

import dash
from dash import dcc
from dash import html


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
                    html.Div([
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
                        # dbc.Button('Начать анализ', id='target-user-id-button', color='primary', className='me-1'),
                        html.Button(
                            'Начать анализ',
                            id='target-user-id-button',
                            n_clicks=0,
                            className='twelve columns')
                    ]),
                    ### There will be option panel (labels inclusion, communities coloring checkboxes) ###
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