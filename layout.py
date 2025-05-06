from textwrap import dedent as d

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
                            dcc.Checklist(
                                id='historical-checklist',
                                options={
                                    'historical': 'Импортировать данные (при наличии)',
                                },
                                value=['historical'],
                            ),
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
                        style={'height': '300px'},
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
                                    'communities': 'Выделение обнаруженных сообществ',
                                },
                                value=[],
                            ),
                            html.Button(
                                'Обновить граф',
                                id='apply-graph-options-button',
                                className='twelve columns',
                                n_clicks=0,
                            )
                        ],
                        style={'height': '300px'},
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
                    html.Img(
                        id='graph-image',
                        src=None,
                        alt='image',
                        className='twelve columns',
                    ),
                ],
            ),

            ###################################### Таблица справа ######################################
            html.Div(
                id='tables-section',
                className='four columns',
                children=[
                    dcc.Tabs(
                        id='tables-tabs',
                        className='twelve columns',
                        value='tab-1-friends-table',
                        children=[
                            dcc.Tab(
                                value='tab-1-friends-table',
                                label='Друзья',
                            ),
                            dcc.Tab(
                                value='tab-2-betweenness-table',
                                label='Посредническая центральность',
                            ),
                            dcc.Tab(
                                value='tab-3-eigenvector-table',
                                label='Степень влиятельности',
                            ),
                            dcc.Tab(
                                value='tab-4-pagerank-table',
                                label='PageRank',
                            ),
                            dcc.Tab(
                                value='tab-5-communities-table',
                                label='Сообщества',
                            ),
                        ],
                    ),
                    html.Div(
                        id='table-place',
                        className='twelve columns',
                        style={
                            'height': '70vh',
                            'overflow': 'scroll',
                        }
                    ),
                ],
            ),
        ],
    ),
])
