import os

import dash
import dash.dependencies as dd
import pandas as pd

from layout import layout
from data_extraction import simple_export, simple_import, get_user_data, fast_get_friends
from social_network_analyzer import SocialNetworkAnalyzer


app = dash.Dash(__name__)
app.title = 'Анализ дружеских связей пользователя ВК'

TARGET_USER_ID = None

app.layout = layout


@app.callback(
    [
        dd.Output('graph-image', 'src'),
        dd.Output('target-user-id-error', 'children'),
        dd.Output('tables-tabs', 'value'),
    ],
    dd.Input('target-user-id-button', 'n_clicks'),
    [
        dd.State('target-user-id-input', 'value'),
        dd.State('options-checklist', 'value'),
    ],
    prevent_initial_call=True,
)
def target_user_id_button_clicked(n_clicks, input_value, options):
    result = {
        'graph-image': None,
        'target-user-id-error': '',
        'tables-tabs': 'tab-1-friends-table',
    }

    for _ in [0]:
        user = get_user_data(input_value)

        if not user:
            result['target-user-id-error'] = 'Некорректный ID, возможно отсутствует Интернет-соединение'
            break

        if 'historical' in options and os.path.exists(f'dumps/users_relations_{input_value}.txt'):
            friends, relations = simple_import(input_value)
        else:
            friends, relations = fast_get_friends(input_value)
            simple_export(input_value, friends, relations)

        if not relations:
            result['target-user-id-error'] = 'Некорректный ID, возможно у пользователя закрытый профиль'
            break

        friends_filename = f'friends_list_{input_value}.csv'
        image_filename = (f'graph_image_{input_value}_'
                    f'{"l" if "labels" in options else "n"}_'
                    f'{"c" if "communities" in options else "n"}.png')

        analyzer = SocialNetworkAnalyzer()
        analyzer.load_from_edges(nodes=[friend.id for friend in friends], edges=relations, users=friends)

        if 'communities' in options:
            analyzer.detect_communities()

        analyzer.calculate_centralities()
        analyzer.save_results()

        if not ('historical' in options and os.path.exists(f'assets/{image_filename}')):
            analyzer.visualize(
                f'assets/{image_filename}',
                labels='labels' in options,
                communities='communities' in options,
            )

        if not ('historical' in options and os.path.exists(f'tables/{friends_filename}')):
            analyzer.save_friends_list(output_file=f'tables/{friends_filename}')

        result['graph-image'] = dash.get_asset_url(image_filename)
        break

    return [v for k, v in result.items()]


# Tab switches
@app.callback(
    dd.Output('table-place', 'children'),
    dd.Input('tables-tabs', 'value'),
    dd.State('target-user-id-input', 'value'),
    prevent_initial_call=True,
)
def switch_table_tab(current_tab, input_value):
    if current_tab == 'tab-1-friends-table':
        return dash.dash_table.DataTable(pd.read_csv(f'tables/friends_list_{input_value}.csv').to_dict('records'))
    if current_tab == 'tab-2-metrics-table':
        return dash.dash_table.DataTable(pd.read_csv('test_metrics.csv').to_dict('records'))
    return dash.dash_table.DataTable(None)


if __name__ == '__main__':
    pass
    app.run(debug=True, host='0.0.0.0', port=8051)
