import dash
import pandas as pd

from layout import layout
from data_extraction import simple_import
from social_network_analyzer import SocialNetworkAnalyzer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Анализ дружеских связей пользователя ВК'

TARGET_USER_ID = None

app.layout = layout


@app.callback(
    # dash.dependencies.Output('title', 'children'),
    [
        dash.dependencies.Output('graph-image', 'src'),
        dash.dependencies.Output('target-user-id-error', 'children'),
    ],
    dash.dependencies.Input('target-user-id-button', 'n_clicks'),
    dash.dependencies.State('target-user-id-input', 'value'),
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
    analyzer.visualize(f'assets/network_graph_{input_value}.png')

    return dash.get_asset_url(f'network_graph_{input_value}.png'), ''


if __name__ == '__main__':
    pass
    app.run(debug=True, host='0.0.0.0', port=8051)
