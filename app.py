from dash import Dash, html, dcc
import dash
import sys


sys.path.append("./module")



app = Dash(__name__, use_pages=True,title='GLT Dashboard-Demo')

app.layout = html.Div([
    html.H1('GLT ADAM control DashBoard-Demo'),
    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port='8052')
