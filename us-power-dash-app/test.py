import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import visdcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Don't commit this!
# For testing convenience only.
mapbox_access_token = 'pk.eyJ1IjoiZXRwaW5hcmQiLCJhIjoiY2luMHIzdHE0MGFxNXVubTRxczZ2YmUxaCJ9.hwWZful0U2CQxit4ItNsiQ'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = [go.Scattermapbox(lat=[38.8484], lon=[-98.921], mode='markers', marker=dict(size=8),
text = ['test'])]

layout = go.Layout(autosize=True, hovermode='closest', mapbox=dict(bearing=0,
    accesstoken = mapbox_access_token,
    center=dict(lat=38.8484, lon=-98.921),
    pitch=0, zoom=5))
fig = dict(data=data, layout=layout)

app.layout = html.Div([
dcc.Graph(id='graph', figure=fig),
visdcc.Run_js(id = 'javascript'),
html.H2('LongLat: ', id='lnglat-display')

])
@app.callback(
    Output('javascript', 'run'),
    [Input('graph', 'id')])
def getlnglat(x): 
    if x: 
        return(
        '''
            let map1 = document.getElementById('graph')
            let map = map1._fullLayout.mapbox._subplot.map
            map.on('click', function(e) {
            let lngLat = e.lngLat
            setProps({'event': {lng: lngLat.lng, lat: lngLat.lat}})
            })
        
        ''')
    return ""

@app.callback(
    Output('lnglat-display', 'children'),
    [Input('javascript', 'event')])    
def showlnglat(event):
    if event:
        return f'Lon:{event["lng"]} Lat:{event["lat"]} '
    return 'Click on the map for lnglat'
    
@app.callback(
    Output('graph', 'figure'),
    [Input('javascript', 'event')])    
def update_pointer(event):
    data = [go.Scattermapbox(lat=[38.8484], lon=[-98.921], 
        mode='markers', marker=dict(size=8), text = ['test'])]
    if event:
        data = [go.Scattermapbox(lat=[event["lat"]], lon=[event["lng"]], 
        mode='markers', marker=dict(size=10), text = ['test'])]

    layout = go.Layout(autosize=True, hovermode='closest', 
        mapbox=dict(bearing=0,
        accesstoken = mapbox_access_token,
        center=dict(lat=38.8484, lon=-98.921),
        pitch=0, zoom=5))
    fig = dict(data=data, layout=layout)
    return fig
   
if __name__ == '__main__':
    app.run_server(debug=True)
