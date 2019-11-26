import dash
import dash_html_components as html
import dash_core_components as dcc
from flaskApp import app, db
import chart_studio.plotly as ply
import plotly.graph_objects as ply_go
from flaskApp.models import User, Post
import pandas as pd
import operator
import collections


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://codepen.io/amyoshino/pen/jzXypZ.css']



dash_server = dash.Dash(
    __name__,
    server=app,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)


def query_lang():
    posts = Post.query.all()
    lang_list = []
    lang_dict = {}
    for p in posts:
        for lang in p.language.split(', '):
            lang_list.append(lang.upper())

    lang_df = pd.DataFrame(lang_list)
    unique_lang = lang_df[0].unique()

    for item in lang_list:
        lang_dict[item] = lang_dict.get(item, 0) + 1

    return lang_dict

def query_category():
    posts = Post.query.all()
    lang_list = []
    lang_dict = {}
    for p in posts:
        for lang in p.category.split(', '):
            lang_list.append(lang.upper())

    lang_df = pd.DataFrame(lang_list)
    unique_lang = lang_df[0].unique()

    for item in lang_list:
        lang_dict[item] = lang_dict.get(item, 0) + 1

    lang_list = sorted(lang_dict.items(), key=operator.itemgetter(1))
    lang_dict = collections.OrderedDict(lang_list)
    return lang_dict






dash_server.layout = html.Div(
    html.Div([


        html.Div(
            [
                html.Div([
                    dcc.Graph(id='language_usage',
                              figure=ply_go.Figure(
                                  data=[ply_go.Pie(labels=list(query_lang().keys()),
                                                   values=list(query_lang().values()))],
                                  layout=ply_go.Layout(
                                      title='Language Usage')
                              ))
                ], className='six columns'
                ),

                html.Div([
                    dcc.Graph(id='project types',


                                 figure=ply_go.Figure(
                                     data=[ply_go.Bar(x=list(query_category().values()),
                                        y=list(query_category().keys()),
                                                                orientation='h' )],
                                     layout=ply_go.Layout(
                                         title='Project Types')
                                 )

   




                              )
                ], className='six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)


if __name__ == '__main__':
    dash_server.run_server(debug=True)
