import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import patient_demographics
import patient_medical_reason
import resources

app = dash.Dash(__name__, external_stylesheets=resources.external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True


patient_data_df = pd.read_csv(resources.data_url)

patient_data_df['admit_type'] = patient_data_df['admission_type_id'].map(resources.event_dictionary)

df_med_readmit_final = pd.DataFrame(
    patient_data_df.groupby(['medical_specialty', 'admit_type', 'time_in_hospital', 'num_lab_procedures',
                             'num_medications', 'readmitted']).size()).reset_index()
df_med_readmit_final = df_med_readmit_final[(df_med_readmit_final['medical_specialty'] != '?')]
df_med_readmit_final.rename(columns={0: "count"}, inplace=True)
df_med_readmit_final = df_med_readmit_final.sort_values(by=['count'], ascending=False)

#print(df_med_readmit_final.head(10))

df_gender_race_age_final = pd.DataFrame(patient_data_df.groupby(['race', 'gender', 'age']).size()).reset_index()
df_gender_race_age_final.rename(columns={0: "count"}, inplace=True)
df_gender_race_age_final = df_gender_race_age_final.replace('?', 'Unknown')

# race- age
df_race_age_final = df_gender_race_age_final.groupby(['age', 'race']).sum().reset_index()

df_ms_final = df_med_readmit_final

'''
app layout - contains html part of the app
'''
app.layout = html.Div(style={'backgroundColor': resources.colors['background']}, children=[
    html.H1('Demographics Dashboard and Re-admission Statistics', style={
        'textAlign': 'center',
        'color': resources.colors['text']

    }),
    html.H4('DATA 608 Final Project from Anjal Hussan', style={
        'textAlign': 'center',
        'color': resources.colors['text']
    }),
    html.H6('Data source: ' + resources.data_source,
            style={
                'textAlign': 'center',
                'color': resources.colors['text']
            }),

    #send value='Admission_tab' to make it default
    dcc.Tabs(id="tabs", className="row", style={"margin": "2% 3%", "height": "20", "verticalAlign": "middle"},
             value='admission_tab', children=[
            dcc.Tab(label='Demographics', value='demographic_tab'),
            dcc.Tab(label='Admission Reason And Re-Admission Rate', value='admission_tab'),
        ]),
    html.Div(id='tabs-content')
])

'''
Call Back functions
'''
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'demographic_tab':
        return patient_demographics.demographics_tab
    elif tab == 'admission_tab':
        return patient_medical_reason.readmission_tab


# Tab 1 callback
@app.callback(dash.dependencies.Output('medical_reason_content', 'children'),
              [dash.dependencies.Input('medical_Reason_dropdown', 'value')])
def medical_reason_dropdown(value):
    df_ms_final = df_med_readmit_final[df_med_readmit_final['medical_specialty'] == value].copy()
    graphs = [dcc.Graph(id='g_gender', config={"displaylogo": False},
                        figure={
                            'data': [
                                {
                                    'labels': df_ms_final['admit_type'],
                                    'values': df_ms_final['count'],
                                    'type': 'pie',
                                    'hole': .4
                                }
                            ],
                            'layout':
                                {
                                    'title': 'Patient Hospital Admission',
                                    'annotations': [{
                                        "font": {
                                            "size": 10
                                        },
                                        'text': 'Admission Type', "showarrow": False}]
                                }

                        })]

    return graphs


# Tab 1 callback
@app.callback(dash.dependencies.Output('readmission_content', 'children'),
              [dash.dependencies.Input('readmission_dropdown_days', 'value')]
              )
def page_2_dropdown(val):
    df = df_med_readmit_final[df_med_readmit_final['readmitted'] == str(val)].copy()
    # return df_ms_final
    gr = []
    x = df['time_in_hospital']
    hist_data = [x]
    group_labels = ['Time Spent in the Hospital']
    fig = ff.create_distplot(hist_data, group_labels)
    gr.append(dcc.Graph(id='abc', figure=fig))

    return gr


if __name__ == '__main__':
    app.run_server(debug=True)
