from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd

# Data statis buah sesuai dengan yang tertera pada jobsheet
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 1, 2, 2, 4, 5],
    'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
})

# Inisialisasi dengan prefix khusus agar routing reverse proxy Nginx berjalan lancar
app = Dash(__name__, requests_pathname_prefix='/dash/')
server = app.server  # Variabel utama yang akan dipanggil oleh Gunicorn sebagai WSGI

app.layout = html.Div([
    html.H2('Dash Plotly — Demo'),
    html.Div('Pilih metrik untuk chart:', style={'marginTop': '6px'}),
    dcc.RadioItems(
        options=['Amount'],
        value='Amount',
        id='metric',
        inline=True
    ),
    html.Hr(),
    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=6,
        style_table={'overflowX': 'auto'}
    ),
    html.Br(),
    dcc.Graph(id='chart')
])

@callback(
    Output('chart', 'figure'),
    Input('metric', 'value')
)
def update_graph(selected_metric):
    fig = px.bar(df, x="Fruit", y=selected_metric, color="City", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)