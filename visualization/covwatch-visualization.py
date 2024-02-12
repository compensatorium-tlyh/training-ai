# Biomarker-based interactive dropdown
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

biomarkers = ["SpO2", "BP Dia", "BP Sys", "HRV", "Stress", "HR", "Body Temp"]
labels = [1, 0.75, 0.5, 0.25, 0]
markers = ["circle", "circle-open", "cross-thin-open", "x-open", "x"]

# Read the data
file_label = "/home/ihsannh17/Downloads/RMP/github-repos/etc/2023-12-(04-14)_Label.csv"
df_raw = pd.read_csv(file_label)

# Merge Name and Device Code
df_raw['Name_Device'] = df_raw['Name'] + ' ' + df_raw['Device Code']
df_raw["Time (WIB)"] = pd.to_datetime(df_raw["Time (WIB)"])

# Get unique names for grouping
unique_names = pd.Index(df_raw['Name_Device'].unique())

app.layout = html.Div([
    html.Div([
        html.Label("Select Biomarker:"),
        dcc.Dropdown(
            options=[{'label': biomarker, 'value': biomarker} for biomarker in biomarkers],
            value=biomarkers[0],
            id='biomarker-dropdown'
        ),
        # html.Label("Select Labels:"),
        dcc.Checklist(
            options=[{'label': f'Label {label}', 'value': label} for label in labels],
            value=labels,
            id='label-checkbox',
            inline=True
        ),
        # html.Label("Select People:"),
        dcc.Checklist(
            options=[{'label': person.split()[0], 'value': person} for person in unique_names],
            value=unique_names,
            id='person-checkbox',
            inline=True,
            style={'columnCount': 6, 'width': '50000px'}
        )
    ], style={'width': '90%', 'margin': '0 auto', 'padding': '1px', 'color': 'black'}),

    dcc.Graph(id='biomarker-graph')
], style={'backgroundColor': '#F4F6F8'})


@callback(
    Output('biomarker-graph', 'figure'),
    Input('biomarker-dropdown', 'value'),
    Input('label-checkbox', 'value'),
    Input('person-checkbox', 'value')
)
def update_graph(biomarker, selected_labels, selected_people):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=[biomarker])

    for person in selected_people:
        df = df_raw[df_raw['Name_Device'] == person]

        for label in selected_labels:
            _df = df[df['Code'] == label]
            symbol = markers[labels.index(label)]

            fig.add_trace(go.Scatter(
                x=_df["Time (WIB)"],
                y=_df[biomarker],
                mode='markers',
                name=f"{person}-{label}",
                marker=dict(symbol=symbol, size=7)
            ))

    fig.update_layout(
        title=biomarker,
        xaxis_title='Time',
        yaxis_title='',
        height=600,
        showlegend=True
    )
    fig.update_yaxes(overlaying='y', side='right')
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8070)
