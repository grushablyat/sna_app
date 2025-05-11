from textwrap import dedent as d

from dash import dcc
from dash import html


tabs_style = {
    'width' : '100%',
    'display' : 'flex',
    'flexWrap' : 'wrap',
    'justifyContent' : 'flex-start',
}

tab_style_1 = {
    'borderTop' : '1px solid #cccccc',
    'borderBottom' : '1px solid #cccccc',
    'backgroundColor' : '#FFFFFF',
    'padding' : '8px',
    'textAlign' : 'center',
    'flex' : '1 1 33%',
    'flexBasis': '33%',
    'flexGrow': 0,
}

tab_style_sel_1 = tab_style_1.copy()
tab_style_sel_1['backgroundColor'] = '#F0F2F4'

tab_style_2 = tab_style_1.copy()
tab_style_2['flex'] = '1 1 50%'
tab_style_2['flexBasis'] = '50%'

tab_style_sel_2 = tab_style_2.copy()
tab_style_sel_2['background-color'] = '#F0F2F4'



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
                            dcc.Markdown(d('''
                            Укажите ключ доступа:
                            ''')),
                            dcc.Input(
                                id='access-token-input',
                                type='password',
                                placeholder='Вставьте ключ доступа',
                                className='twelve columns',
                            ),
                            dcc.Checklist(
                                id='import-checklist',
                                options={
                                    'import': 'Импортировать данные (при наличии)',
                                },
                                value=['import'],
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
                        style={'height': '340px'},
                    ),
                    ###################################### User data section ######################################
                    html.Div(
                        id='user-data-section',
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d('''
                            **Подробная информация**
                            
                            Нажмите на узел или ребро графа для отображения подробной информации
                            ''')),
                            html.A(
                                id='user-link-by-click',
                                href=None,
                                children=None,
                                target='_blank'
                            ),
                            html.Pre(
                                id='user-data-by-click',
                                style={
                                    'font-family': 'Tahoma, Verdana, sans-serif',
                                    'text-size': '16px',
                                    'line-height': '18px',
                                },
                            ),
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
                    dcc.Graph(
                        id='interactive-graph',
                        figure=None,
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
                                style=tab_style_1,
                                selected_style=tab_style_sel_1,
                            ),
                            dcc.Tab(
                                value='tab-5-communities-table',
                                label='Сообщества',
                                style=tab_style_1,
                                selected_style=tab_style_sel_1,
                            ),
                            dcc.Tab(
                                value='tab-4-pagerank-table',
                                label='PageRank',
                                style=tab_style_1,
                                selected_style=tab_style_sel_1,
                            ),
                            dcc.Tab(
                                value='tab-2-betweenness-table',
                                label='Посредническая центральность',
                                style=tab_style_2,
                                selected_style=tab_style_sel_2,
                            ),
                            dcc.Tab(
                                value='tab-3-eigenvector-table',
                                label='Степень влиятельности',
                                style=tab_style_2,
                                selected_style=tab_style_sel_2,
                            ),
                        ],
                        style=tabs_style,
                    ),
                    html.Div(
                        id='table-place',
                        className='twelve columns',
                        style={
                            'height': '70vh',
                        }
                    ),
                ],
            ),
        ],
    ),
])
