import os

import dash
import dash.dependencies as dd
import pandas as pd

from config import TABLES
from layout import layout
from vk_data_extractor import simple_export, simple_import, get_user_data, fast_get_friends
from social_network_analyzer import SocialNetworkAnalyzer


app = dash.Dash(__name__)
app.title = 'Анализ дружеских связей пользователя ВК'
app.layout = layout


# Start analysis
@app.callback(
    [
        dd.Output('target-user-id-error', 'children'),
        dd.Output('tables-tabs', 'value'),
        dd.Output('interactive-graph', 'figure'),
    ],
    dd.Input('target-user-id-button', 'n_clicks'),
    [
        dd.State('target-user-id-input', 'value'),
        dd.State('historical-checklist', 'value'),
        dd.State('access-token-input', 'value'),
    ],
    prevent_initial_call=True,
)
def target_user_id_button_clicked(n_clicks, input_value, options, access_token):
    result = {
        'target-user-id-error': '',
        'tables-tabs': 'tab-1-friends-table',
        'interactive-graph': None,
    }

    for _ in [0]:
        user = get_user_data(input_value, access_token)

        if not user:
            result['target-user-id-error'] = 'Некорректный ID, возможно отсутствует Интернет-соединение'
            break

        if 'historical' in options and os.path.exists(f'dumps/dump_{input_value}.txt'):
            friends, relations = simple_import(input_value)
        else:
            friends, relations = fast_get_friends(input_value, access_token)
            simple_export(input_value, friends, relations)

        if not relations:
            result['target-user-id-error'] = 'Некорректный ID, возможно у пользователя закрытый профиль'
            break

        metrics_filename = f'{TABLES}/metrics_{input_value}.csv'

        analyzer = SocialNetworkAnalyzer()
        analyzer.load_from_edges(friends, relations)

        analyzer.calculate_centralities()
        analyzer.detect_communities()
        analyzer.save_results(metrics_filename)

        result['interactive-graph'] = analyzer.create_interactive_graph(input_value)
        break

    return [v for k, v in result.items()]


@app.callback(
    dd.Output('table-place', 'children'),
    dd.Input('tables-tabs', 'value'),
    dd.State('target-user-id-input', 'value'),
    prevent_initial_call=True,
)
def switch_table_tab(current_tab, input_value):
    if not os.path.exists(f'{TABLES}/metrics_{input_value}.csv'):
        return dash.dash_table.DataTable(None)

    metric = None

    if current_tab == 'tab-1-friends-table':
        pass
    elif current_tab == 'tab-2-betweenness-table':
        metric = 'Посредническая центральность'
    elif current_tab == 'tab-3-eigenvector-table':
        metric = 'Степень влиятельности'
    elif current_tab == 'tab-4-pagerank-table':
        metric = 'PageRank'
    elif current_tab == 'tab-5-communities-table':
        metric = 'Сообщества'

    columns = ['ID', 'Имя']
    columns.append(metric) if metric else None

    return dash.dash_table.DataTable(pd.read_csv(
        f'{TABLES}/metrics_{input_value}.csv',
        usecols=columns,
    ).sort_values(metric if metric else 'ID', ascending=False if metric else True).to_dict('records'), page_size=20)


@app.callback(
    dd.Output('user-data-by-click', 'children'),
    dd.Input('interactive-graph', 'clickData'),
    dd.State('access-token-input', 'value'),
    prevent_initial_call=True,
)
def node_clicked(clickData, access_token):
    data = clickData['points'][0]
    type = data.get('text', None)

    if type:
        user_id = data.get('text')
        user = get_user_data(int(user_id), access_token, extended=True)
        return user.info()
    else:
        text = data.get('hovertext')
        text = text.replace('<br>', ' ')
        text = text.split(' ')

        user1 = get_user_data(text[1], access_token)
        user2 = get_user_data(text[3], access_token)

        return f'Связь между:\n{user1.__str__()}\n{user2.__str__()}'


if __name__ == '__main__':
    pass
    app.run(debug=False, host='0.0.0.0', port=8050)
