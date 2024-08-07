import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, dcc
from modals import *

class Judging:
    @staticmethod
    def layout():
        return dbc.Container([
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Img(src="/assets/bpcc_logo.png", height="60px"), width="auto"),
                dbc.Col(html.H3("BS Speech and Debate Tournament", id="tournament-name", className="text-center"), width=True),
                dbc.Col(html.Img(src="/assets/bpcc_debate_logo.png", height="60px"), width="auto")
            ], className="align-items-center mb-4"),
            html.Br(),
            dbc.Row([
                dbc.Col(html.Label("Judge: ", id='set-judge-name', className="d-flex justify-content-center")),
                dbc.Col(html.Label("Round Number: ", id='set-round-number', className="d-flex justify-content-center"))
            ], className="align-items-center mb-4"),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.Label("RESOLUTION:", className="font-weight-bold text-center"), width=12),
                dbc.Col(dbc.Input(type="text", id="resolution-input", placeholder="Please Enter the Resolution (e.g. Taxation is theft)", value=''), width=12)
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dbc.Label("AFFIRMATIVE:", className="font-weight-bold text-center", id='aff-name'), width=6, className="text-center"),
                dbc.Col(dbc.Label("NEGATIVE:", className="font-weight-bold text-center", id='neg-name'), width=6, className="text-center")
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dbc.Label("AFFIRMATIVE (Speaker Points)", className="font-weight-bold text-center", id='aff-speaks'), width=4, className="text-center"),
                dbc.Col([
                    dbc.Label("Please Rank Each Debater 1-5 for Each Category:", className="font-weight-bold text-center"),
                    dbc.Row([
                        dbc.Col(dbc.Button("Open Speaker Point Calculator", color="primary", id="open-calc", size='sm'), width='auto'),
                        dbc.Col(dbc.Button("Open Speaker Point Guide", color="primary", id="open-guide", size='sm'), width='auto'),
                    ], justify="center")
                ], width=4, className="text-center"),
                dbc.Col(dbc.Label("NEGATIVE (Speaker Points)", className="font-weight-bold text-center", id='neg-speaks'), width=4, className="text-center"),
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Please Provide Constructive Comments for the Affirmative:", className="font-weight-bold text-center"),
                    dbc.Textarea(id='aff-comments', style={"width": "100%", "height": "200px"}, value='')
                ]),
                dbc.Col([
                    dbc.Label("Please Provide Constructive Comments for the Negative:", className="font-weight-bold text-center"),
                    dbc.Textarea(id='neg-comments', style={"width": "100%", "height": "200px"}, value='')
                ])
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(dbc.Label("Vote for the AFFIRMATIVE / NEGATIVE", className="font-weight-bold text-center")),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "AFFIRMATIVE", "value": "Affirmative"},
                                            {"label": "NEGATIVE", "value": "Negative"}
                                        ],
                                        value=None,
                                        id="vote-radio",
                                        inline=True
                                    ),
                                    width={"size": 6, "offset": 3}
                                ),
                            ], className="align-items-center")
                        ])
                    ),
                    width=12,
                    className="mb-3 text-center"
                )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Represented by:", className="font-weight-bold text-center"),
                    dbc.Input(type="text", placeholder="Competitor Name", id="competitor-name", value=''),
                    dbc.Input(type="text", placeholder="Competitor School/Program", id="competitor-school", className="mt-2", value='')
                ], width=12, className="text-center")
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    dbc.Label("Reason for Decision:", className="font-weight-bold text-center"), 
                    width={"size": 12, "offset": 5},  # Adjust width and offset to center the label
                    className="mb-2 mt-2"
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Textarea(
                        id='reason-for-decision', 
                        style={"width": "100%", "height": "200px"}, 
                        value=''
                    ),
                    width={"size": 12}  # Adjust width and offset to center the textarea
                )
            ], className="mb-3", justify="center"),
            html.Hr(),
            
            dbc.Row([
                dbc.Col(
                    dbc.Checklist(
                        options=[
                            {"label": "I acknowledge the decision is based on the arguments made during the debate and not on my personal beliefs.", "value": True}
                        ],
                        value=False,
                        id="acknowledge-checklist",
                        inline=True
                    ),
                    width=12,
                    className="text-center"
                )
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Adjudicated by:", className="font-weight-bold text-center"),
                    dbc.Input(type="text", placeholder="Judge Name", id="judge-name", value=''),
                    dbc.Input(type="text", placeholder="Judge School/Program", id="judge-school", className="mt-2", value='')
                ], width=12, className="text-center")
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col(dbc.Button("Submit", color="primary", id="submit-judging"), width=12, className="text-center")
            ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(login_signup_modal(), width=12),
                dbc.Col(signup_modal(), width=12),
                dbc.Col(signup_error_modal(), width=12),
                dbc.Col(login_error_modal(), width=12),
                dbc.Col(speaker_point_calculator_modal(), width=12),
                dbc.Col(submission_modal(), width=12),
                dbc.Col(speaker_point_confirmation_modal(), width=12),
                
                dbc.Col(no_ballot_modal(), width=12)
            ]),
            dcc.Interval(id='modal-close-interval', interval=2000, n_intervals=0),
            dcc.Interval(id="error-modal-close-interval", interval=2500, n_intervals=0)
        ], fluid=True)
