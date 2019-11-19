import dash
import dash_html_components as html
import dash_core_components as dcc
from flaskApp import app, db
import chart_studio.plotly as ply
import plotly.graph_objects as ply_go
from flaskApp.models import User, Post
import pandas as pd


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

    # for item in lang_dict:
    #     lang_dict[item] = str(lang_dict[item])

    # print(lang_dict.keys())
    # print(lang_dict.values())

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

    # for item in lang_dict:
    #     lang_dict[item] = str(lang_dict[item])

    print(lang_dict.keys())
    print(lang_dict.values())

    return lang_dict


print(query_category())



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

   

                            #   figure=ply_go.Figure(
                            #       data=[ply_go.Treemap(
                                      
                            #              labels = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
                            #              parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
                            #       )]

                            #   )

                    #         figure={
                    #     'data': [
                    #         {'x': list(query_category()), 'y': list(query_category().values()),
                    #          'type': 'bar', 'name': 'SF', 'orientation':'h'},
                    #         # {'x': [1, 2, 3], 'y': [2, 9, 8], 'type': 'bar', 'name': u'Montréal'},
                    #     ],
                    #     'layout': {
                    #         'title': 'Graph 2'
                    #     }
                    # }


                              )
                ], className='six columns'
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one')
)


if __name__ == '__main__':
    dash_server.run_server(debug=True)
