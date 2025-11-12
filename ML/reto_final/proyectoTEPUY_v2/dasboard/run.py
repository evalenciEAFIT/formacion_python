from dash import Dash, html, dcc

dash = Dash()

dash.layout = [
    html.H1(children='Prueba DASH', style={'textAlign':'center'}),
    html.Textarea("Esto es una prueba....")
]

if __name__ == '__main__':
    dash.run(port=8056, debug=False)