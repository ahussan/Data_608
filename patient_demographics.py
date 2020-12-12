import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import resources

patient_data_df = pd.read_csv(resources.data_url)

# gender count
df_gender = pd.DataFrame(patient_data_df.groupby('gender').size(), columns=['count'])
df_gender_final = df_gender.reset_index()

# gender age
df_gender_race_age_final = pd.DataFrame(patient_data_df.groupby(['race', 'gender', 'age']).size()).reset_index()
df_gender_race_age_final.rename(columns={0: "count"}, inplace=True)
df_gender_race_age_final = df_gender_race_age_final.replace('?', 'Unknown')

# age-gender - bar graph
df_gender_age_final = df_gender_race_age_final.groupby(['age', 'gender']).sum().reset_index()
df_gender_age_male = df_gender_age_final[df_gender_age_final['gender'] == 'Male']
df_gender_age_female = df_gender_age_final[df_gender_age_final['gender'] == 'Female']

# gender race
df_gender_race_final = pd.DataFrame(patient_data_df.groupby(['race', 'gender']).size()).reset_index()
df_gender_race_final.rename(columns={0: "count"}, inplace=True)
df_gender_race_final = df_gender_race_final.replace('?', 'Unknown')
df_male = df_gender_race_final[df_gender_race_final['gender'] == 'Male']
df_female = df_gender_race_final[df_gender_race_final['gender'] == 'Female']

# race- age
df_race_age_final = df_gender_race_age_final.groupby(['age', 'race']).sum().reset_index()
df_race_age_final_ca = df_race_age_final[df_race_age_final['race'] == 'Caucasian']
df_race_age_final_aa = df_race_age_final[df_race_age_final['race'] == 'AfricanAmerican']
df_race_age_final_his = df_race_age_final[df_race_age_final['race'] == 'Hispanic']
df_race_age_final_as = df_race_age_final[df_race_age_final['race'] == 'Asian']

demographics_tab = html.Div([
    html.H3('Demographics', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            # html.H4('Gender', style={'textAlign': 'center'}),
            dcc.Graph(id='g_gender', config={"displaylogo": False},
                      figure={
                          'data': [
                              {
                                  'labels': df_gender_race_age_final['gender'],
                                  'values': df_gender_race_age_final['count'],
                                  'type': 'pie',
                                  'hole': .4
                              }
                          ],
                          'layout':
                              {
                                  'title': 'Gender Distribution',
                                  'legend': {'orientation': "h"},
                                  'annotations': [{
                                      "font": {
                                          "size": 20
                                      },
                                      'text': 'Gender', "showarrow": False}]
                              }

                      })
        ], className="four columns"),

        html.Div([
            # html.H4('Race', style={'textAlign': 'center'}),
            dcc.Graph(id='g_race', config={"displaylogo": False},
                      figure={
                          'data': [
                              {
                                  'labels': df_gender_race_age_final['race'],
                                  'values': df_gender_race_age_final['count'],
                                  'type': 'pie',
                                  'hole': .4
                              }
                          ],
                          'layout':
                              {
                                  'title': 'Race Distribution',
                                  'legend': {'orientation': "h"},
                                  'annotations': [{
                                      "font": {
                                          "size": 20
                                      },
                                      'text': 'Race', "showarrow": False}]
                              }

                      })
        ], className="four columns"),

        html.Div([
            # html.H4('Age', style={'textAlign': 'center'}),
            dcc.Graph(id='g_age', config={"displaylogo": False},
                      figure={
                          'data': [
                              {
                                  'labels': df_gender_race_age_final['age'],
                                  'values': df_gender_race_age_final['count'],
                                  'type': 'pie',
                                  'hole': .4
                              }
                          ],
                          'layout':
                              {
                                  'title': 'Age Distribution',
                                  'legend': {'orientation': "h"},
                                  'annotations': [{
                                      "font": {
                                          "size": 20
                                      },
                                      'text': 'Age', "showarrow": False}]
                              }

                      })
        ], className="four columns")

    ], className="row", style={"margin": "1% 3%"}),

    html.Div([
        html.Div([
            # html.H4('Race - Gender distribution', style={'textAlign': 'center'}),
            dcc.Graph(
                id='race_gender_graph', config={"displaylogo": False},
                figure={
                    'data': [
                        {'x': df_male['race'], 'y': df_male['count'] / sum(df_gender_race_final['count']) * 100,
                         'type': 'bar', 'name': 'male', 'marker': {'color': '#1E90FF'}},
                        {'x': df_female['race'], 'y': df_female['count'] / sum(df_gender_race_final['count']) * 100,
                         'type': 'bar', 'name': 'female', 'marker': {'color': '#3CB371'}}
                    ],
                    'layout': {
                        'title': 'Race-Gender Distribution',
                        'xaxis': {'title': 'Race'},
                        'yaxis': {'title': '% Population'}
                    }
                }
            )
        ], className="six columns"),

        html.Div([
            # html.H4('Age - Gender Disrtibution', style={'textAlign': 'center'}),
            dcc.Graph(
                id='age_gender_graph', config={"displaylogo": False},
                figure={
                    'data': [
                        {'x': df_gender_age_male['age'],
                         'y': df_gender_age_male['count'] / sum(df_gender_age_final['count']) * 100,
                         'type': 'bar', 'name': 'male', 'marker': {'color': '#1E90FF'}},
                        {'x': df_gender_age_female['age'],
                         'y': df_gender_age_female['count'] / sum(df_gender_age_final['count']) * 100,
                         'type': 'bar', 'name': 'female', 'marker': {'color': '#3CB371'}}
                    ],
                    'layout': {
                        'title': 'Age-Gender Distribution',
                        "marker": {
                            "color": "rgb(101, 32, 31)"
                        },
                        'xaxis': {'title': 'Age'},
                        'yaxis': {'title': '% Population'}
                    }
                }
            )
        ], className="six columns"),
    ], className="row", style={"margin": "1% 3%"}),

    html.Div([
        html.Div([
            # html.H4('Age - Gender Disrtibution', style={'textAlign': 'center'}),
            dcc.Graph(
                id='race_age_graph', config={"displaylogo": False},
                figure={
                    'data': [go.Bar(x=df_race_age_final_ca['age'],
                                    y=df_race_age_final_ca['count'] / sum(df_race_age_final['count']) * 100,
                                    name='Caucasian'
                                    ),
                             go.Bar(x=df_race_age_final_aa['age'],
                                    y=df_race_age_final_aa['count'] / sum(df_race_age_final['count']) * 100,
                                    name='AfricanAmerican'
                                    ),
                             go.Bar(x=df_race_age_final_his['age'],
                                    y=df_race_age_final_his['count'] / sum(df_race_age_final['count']) * 100,
                                    name='Hispanic'
                                    ),
                             go.Bar(x=df_race_age_final_as['age'],
                                    y=df_race_age_final_as['count'] / sum(df_race_age_final['count']) * 100,
                                    name='Asian'
                                    )

                             ],
                    'layout': go.Layout(
                        title='Race-Age Distribution',
                        # legend = dict(orientation='h', y=-0.20),
                        barmode='stack',
                        xaxis=dict(title='Age'),
                        yaxis=dict(title='% Population'),
                    )
                }
            )
        ])
    ], className="row", style={"margin": "1% 3%"})

]
)
