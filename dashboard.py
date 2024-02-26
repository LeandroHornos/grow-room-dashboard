# GENERAL
import pandas as pd

# DASH
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc

# PLOTLY
import plotly.express as px
import plotly.graph_objects as go


# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# DATA LOADING FROM CSV FILE
# ------------------------------------------------------------------------
path='./data'
file='sample_greenhouse_data_clean.csv'

df = pd.read_csv(f'{path}/{file}')
df['datetime'] = pd.to_datetime(df['datetime'])

print(df.columns)

# FILTRO POR FECHA

fecha_hora_min = df['datetime'].min()

# Obtener la fecha y hora máxima
fecha_hora_max = df['datetime'].max()

print("Fecha y hora mínima:", fecha_hora_min)
print("Fecha y hora máxima:", fecha_hora_max)


fecha_inicial = '2021-03-03'
fecha_final = fecha_hora_max

# Convertir las fechas a objetos datetime
fecha_inicial = pd.to_datetime(fecha_inicial)
fecha_final = pd.to_datetime(fecha_final)




# Filtrar el DataFrame para quedarte solo con las filas dentro del rango de fechas
df_filtrado = df[(df['datetime'] >= fecha_inicial) & (df['datetime'] <= fecha_final)]

# Table

columns=[]
for col in df.columns:
    print(f'{col}:{df[col].dtype}')
    if df[col].dtype == 'float':
        print(col)
        item = dict(id=col, name=col, type='numeric', format=dict(specifier=',.2f'))  # Example result 47,359.02
        columns.append(item)
    else:
        item = dict(id=col, name=col)
        columns.append(item)

# PLOTS
# --------------------------------------------------------------------------

# Temperature line plot

t_vs_dt = px.line(df_filtrado, x="datetime",
                  y="online temperature celsius",
                  title='Temperature [°C]',
                  color_discrete_sequence=px.colors.qualitative.D3
                 )
t_vs_dt.update_yaxes(tickformat='.2f', showgrid=True)

# Humidity line plot

h_vs_dt = px.line(df_filtrado, x="datetime",
                  y="online humidity percentage",
                  title='Relative Humidity [%]',
                  color_discrete_sequence=px.colors.qualitative.Set2
                 )

h_vs_dt.update_yaxes(tickformat='.2f', showgrid=True)

# CO2 line plot

co2_vs_dt = px.line(df_filtrado, x="datetime",
                    y="greenhouse equivalent co2 ppm",
                    title='CO2[PPM]',
                    color_discrete_sequence=px.colors.qualitative.Bold
                   )
co2_vs_dt.update_yaxes(tickformat='.2f', showgrid=True)

# GAUGES
# -------------------------------------------------------------------------------

# Config
bar = '#746c7a'
good = 'PaleGreen'
warning = '#faea5f'
danger = 'Salmon'

# Plots
gauge_temp = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 25,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Temperature"},
    gauge = {
            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': bar},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 27], 'color': good},
                {'range': [27, 35], 'color': warning},
                {'range': [35, 50], 'color': danger},],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 35}}
))

gauge_hum = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 45,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Humidity [%]"},
    gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': bar},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': good},
                {'range': [40, 70], 'color': warning},
                {'range': [70, 100], 'color': danger},],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70}}
))

gauge_co2 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 675,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "CO2 [ppm]"},
    gauge = {
        'axis': {'range': [None, 2000], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': bar},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 500], 'color': good},
            {'range': [500, 1000], 'color': warning},
            {'range': [1000, 2000], 'color': danger},],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 1000}}

))


# App layout
# ------------------------------------------------------------------------
app.layout = dbc.Container([
    html.H1('GROW ROOM CONTROL PANEL', className='text-center mt-2 mb-2'),
    html.Div([
        html.Div([dcc.Graph(figure=gauge_temp)], className="col-lg-4"),
        html.Div([dcc.Graph(figure=gauge_hum)], className="col-lg-4"),
        html.Div([dcc.Graph(figure=gauge_co2)], className="col-lg-4")
             ], className="row"),
    html.Div([dcc.Graph(figure=t_vs_dt)]),
    html.Div([dcc.Graph(figure=h_vs_dt)]),
    html.Div([dcc.Graph(figure=co2_vs_dt)]),
    html.Div([dash_table.DataTable(data=df.to_dict('records'), columns=columns, page_size=10, style_cell={'whiteSpace':'normal','height':'auto'})]),
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
