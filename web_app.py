import dash
import dash.dependencies as dd
import pandas as pd

from layout import layout, external_stylesheets
from data_extraction import simple_import
from social_network_analyzer import SocialNetworkAnalyzer


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Анализ дружеских связей пользователя ВК'

TARGET_USER_ID = None

app.layout = layout


@app.callback(
    [
        dd.Output('graph-image', 'src'),
        dd.Output('target-user-id-error', 'children'),
    ],
    dd.Input('target-user-id-button', 'n_clicks'),
    dd.State('target-user-id-input', 'value'),
    prevent_initial_call=True,
)
def target_user_id_button_clicked(n_clicks, input_value):
    friends, relations = simple_import(input_value)

    if not relations:
        return None, 'Некорректный ID, возможно у пользователя закрытый профиль'

    analyzer = SocialNetworkAnalyzer()
    analyzer.load_from_edges(nodes=[friend.id for friend in friends], edges=relations)
    analyzer.calculate_centralities()
    analyzer.detect_communities()
    analyzer.save_results()
    analyzer.visualize(f'assets/network_graph_{input_value}.png')

    return dash.get_asset_url(f'network_graph_{input_value}.png'), ''


# Tab switches
@app.callback(
    dd.Output('table-place', 'children'),
    dd.Input('tables-tabs', 'value'),
    prevent_initial_call=True,
)
def switch_table_tab(value):
    if value == 'tab-1-friends-table':
        return dash.dash_table.DataTable(pd.read_csv('network_metrics.csv').to_dict('records'))
    if value == 'tab-2-metrics-table':
        return dash.dash_table.DataTable(pd.read_csv('test_metrics.csv').to_dict('records'))
    return dash.dash_table.DataTable(None)


if __name__ == '__main__':
    pass
    app.run(debug=True, host='0.0.0.0', port=8051)
