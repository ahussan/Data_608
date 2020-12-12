import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import resources

patient_data_dd_df = pd.read_csv(resources.data_url)

patient_readmit_df_final = patient_data_dd_df[(patient_data_dd_df['medical_specialty'] != '?')]

readmission_tab = html.Div([
    html.H3('Medical Reason and Re-admission Data', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H6('Medical Reason for Hospital Admission'),
            dcc.Dropdown(
                id='medical_Reason_dropdown',
                options=[{'label': opt, 'value': opt} for opt in
                         patient_readmit_df_final.medical_specialty.unique()],
                value='InternalMedicine'
            ),
            html.Div(id='medical_reason_content')  # the medical reason chart
        ], className="six columns"),

        html.Div([
            html.H6('Re-Admission (Days)'),
            dcc.Dropdown(
                id='readmission_dropdown_days',
                options=[{'label': i, 'value': i} for i in ['>30', '<30', 'NO']],
                value='<30'
            ),
            html.Div(id='readmission_content')  # the Readmission plot
        ], className="six columns"),

    ], className="row", style={"margin": "1% 3%"})
])
