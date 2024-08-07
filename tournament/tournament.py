import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table

class Tournament:
    @staticmethod
    def setup_layout():
        """
        Sets up the main layout of the tournament dashboard with tabs for different sections.

        Returns:
            dbc.Container: A container with tabs for Welcome, Set Up Tournament, and Manage Tournament sections.
        """
        return dbc.Container([
            dcc.Tabs([
                dcc.Tab(label='Welcome', children=Tournament.welcome_layout()),
                dcc.Tab(label='Set Up Tournament', children=Tournament.setup_tournament_layout()),
                dcc.Tab(label='Manage Tournament', children=Tournament.results_layout())
            ])
        ], fluid=True, style={'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'})

    @staticmethod
    def welcome_layout():
        """
        Provides the layout for the Welcome tab, including introductory information and instructions.

        Returns:
            dbc.Container: A container with welcome text, introduction, and usage instructions.
        """
        return dbc.Container([
            dbc.Row([
                dbc.Col(html.Img(src='/assets/ipda.png', style={'width': '50%', 'marginTop': '20px'}), width=10)
            ], className='mb-4', justify='center'),
            dbc.Row([
                dbc.Col(dbc.Textarea(
                    value='Hello and Welcome to Version 0.1 of the (Unofficially) Official Debate Software of The IPDA (ODSI)',
                    style={'width': '100%', 'height': '50px'}, readOnly=True), width=12),
            ], className='mb-3', justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("Introduction", className="font-weight-bold"), width=12)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Textarea(
                    value='    There are currently two web applications underlying ODSI. This one, which is primarily designed for coaches, allows you to create and edit tournaments, and then enter judges, competitors, and rooms into it. The other web application is designed for judges and serves primarily as a digital ballot. All users are required to signup or login to access anything important such as judging a round or creating a tournament\n\n   The goal is to make this as easy of an experience as possible for debaters, judges, and coaches. \n\n  Additionally, the primary goal of this project is for IPDA to have tabbing and judging software specifically tailored to its needs to advance what is, in my humble opinion, the best form of debate both in terms of the debates and in terms of the community. If there are any features you would like to see, please email me at estarcia97@gmail.com',
                    style={'width': '100%', 'height': '300px'}, readOnly=True), width=12),
            ], className='mb-3', justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("How to Use", className="font-weight-bold"), width=12)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Textarea(value='Update as needed IDK its pretty straight forward', style={'width': '100%', 'height': '50px'}, readOnly=True), width=12),
            ], className='mb-3', justify='center')
        ])

    @staticmethod
    def setup_tournament_layout():
        """
        Provides the layout for the Set Up Tournament tab, allowing users to input tournament details and upload necessary files.

        Returns:
            dbc.Container: A container with inputs for tournament details and file upload components.
        """
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Label("Tournament Name", className="font-weight-bold"), width=12),
                dbc.Col(dbc.Input(type="text", placeholder="Enter Tournament Name", id="tournament-name"), width=12)
            ], className="mb-3", justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("Tournament Start Date", className="font-weight-bold"), width=12),
                dbc.Col(dbc.Input(type="date", placeholder="Enter Start Date", id="tournament-start-date"), width=6),
                dbc.Col(dbc.Label("Tournament End Date", className="font-weight-bold"), width=12),
                dbc.Col(dbc.Input(type="date", placeholder="Enter End Date", id="tournament-end-date"), width=6)
            ], className="mb-3", justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("Upload Debaters", className="font-weight-bold"), width=12),
                dbc.Col(dcc.Upload(id='upload-debaters', children=html.Div(['Drag and Drop or ', html.A('Select Debater Files')]), style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }), width=12),
                dbc.Col(html.Div(id='debaters-file-name'), width=12)
            ], className="mb-3", justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("Upload Judges", className="font-weight-bold"), width=12),
                dbc.Col(dcc.Upload(id='upload-judges', children=html.Div(['Drag and Drop or ', html.A('Select Judge Files')]), style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }), width=12),
                dbc.Col(html.Div(id='judges-file-name'), width=12)
            ], className="mb-3", justify='center'),
            dbc.Row([
                dbc.Col(dbc.Label("Upload Rooms", className="font-weight-bold"), width=12),
                dbc.Col(dcc.Upload(id='upload-rooms', children=html.Div(['Drag and Drop or ', html.A('Select Room Files')]), style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }), width=12),
                dbc.Col(html.Div(id='rooms-file-name'), width=12)
            ], className="mb-3", justify='center'),
            dbc.Row([
                dbc.Col(dbc.Button("Submit", id="submit-button", color="primary", className="mr-1"), width=12)
            ], className="mb-3", justify='center')
        ])

    @staticmethod
    def results_layout():
        """
        Provides the layout for the Manage Tournament tab, allowing users to manage tournament entries, view results, and perform actions.

        Returns:
            dbc.Container: A container with components for managing tournament entries and viewing results.
        """
        return dbc.Container([
            dbc.Row([
                dbc.Col(dbc.Label("Select Tournament", className="font-weight-bold"), width=12),
                dbc.Col(dcc.Dropdown(
                    id='tournament-dropdown',
                    placeholder="Select A Tournament to Manage"
                ), width=12),
            ], className="mb-3", justify='center'),

            dbc.Row([
                dbc.Col(dcc.Tabs(id='manage-tabs', children=[
                    dcc.Tab(label='Tournament Overview', children=[
                        dbc.Row([
                            dbc.Col(dbc.Label("Tournament Overview", className="font-weight-bold"), width=12),
                        ], className="mb-3", justify='center'),

                        dbc.Row([
                            dbc.Col(dbc.Label("Select Category to Edit", className="font-weight-bold"), width=12),
                            dbc.Col(dcc.Dropdown(
                                id='entry-type-dropdown',
                                options=[
                                    {'label': 'Debaters', 'value': 'Debaters'},
                                    {'label': 'Judges', 'value': 'Judges'},
                                    {'label': 'Rooms', 'value': 'Rooms'}
                                ],
                                placeholder="Select Entry Category"
                            ), width=12),
                        ], className="mb-3", justify='center'),

                        dbc.Row([
                            dbc.Col([
                                html.Label('Name'),
                                dcc.Dropdown(id='name-dropdown'),
                            ], width=4),
                            dbc.Col([
                                html.Label('School'),
                                dcc.Dropdown(id='school-dropdown'),
                            ], width=4),
                            dbc.Col([
                                html.Label('Division'),
                                dcc.Dropdown(id='division-dropdown'),
                            ], width=4),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(dbc.Table(id='overview-table', striped=True, bordered=True, hover=True), width=12),
                        ], className='mb-3', justify='center'),

                        dbc.Row([
                            dbc.Col(dbc.Label("Select Action To Take", className="font-weight-bold"), width=12),
                            dbc.Col(dcc.Dropdown(
                                id='action-dropdown',
                                options=[
                                    {'label': 'Set Active Tournament', 'value': 'Set Active Tournament'},
                                    {'label': 'Change Name', 'value': 'Change Name'},
                                    {'label': 'Change Division', 'value': 'Change Division'},
                                    {'label': 'Change School', 'value': 'Change School'},
                                    {'label': 'Remove Entry', 'value': 'Remove Entry'},
                                ],
                                placeholder="Select Action"
                            ), width=12),
                        ], className="mb-3", justify='center'),

                        dbc.Row([
                            dbc.Col(dbc.Input(type="text", placeholder="Enter New Value", id="new-entry-value"), width=12),
                        ], className="mb-3", justify='center'),

                        dbc.Row([
                            dbc.Col(dbc.Button("Take Action", id="action-modal-button", color="primary"), width=12)
                        ], className="mb-3", justify='center'),

                        dbc.Modal([
                            dbc.ModalHeader(id='action-info-header'),
                            dbc.ModalBody(id='action-info-body'),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="close-action-info-modal", className="ml-auto")
                            ),
                        ], id="action-info-modal", is_open=False),
                        dcc.Interval(id="action-info-auto-close", interval=2500, n_intervals=0, disabled=True),
                    ]),

                    dcc.Tab(label='Tabbing', children=[
                        dbc.Row([
                            dbc.Col(dbc.Button("Open Tabbing Window", id="tabbing-modal-button", className="ml-auto")),
                        ], className='my-3 align-items-center'),

                        dbc.Row([
                            dbc.Col(html.Label('Division:'), width=4),
                            dbc.Col(dcc.Dropdown(
                                id='tabbing-division-dropdown',
                                options=[
                                    {'label': 'Novice', 'value': 'Novice'},
                                    {'label': 'Junior Varsity', 'value': 'Junior Varsity'},
                                    {'label': 'Varsity', 'value': 'Varsity'},
                                    {'label': 'Professional', 'value': 'Professional'},
                                    {'label': 'Team IPDA', 'value': 'Team IPDA'}
                                ],
                                placeholder='Select Division'
                            ), width=6),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(html.Label('Round'), width=4),
                            dbc.Col(dcc.Dropdown(
                                id='tabbing-round-select-dropdown',
                                options=[],  # Populate options dynamically based on callback
                                placeholder='Select Round'
                            ), width=6),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(dbc.Table(id='postings-table', striped=True, bordered=True, hover=True), width=12),
                        ], className='mb-3', justify='center'),

                        dbc.Row([
                            dbc.Col(html.Label('Select Division'), width=4),
                            dbc.Col(dcc.Dropdown(
                                id='elim-division-dropdown',
                                options=[
                                    {'label': 'Novice', 'value': 'Novice'},
                                    {'label': 'Junior Varsity', 'value': 'Junior Varsity'},
                                    {'label': 'Varsity', 'value': 'Varsity'},
                                    {'label': 'Professional', 'value': 'Professional'},
                                    {'label': 'Individual Debate', 'value': 'Individual Debate'},
                                    {'label': 'Team IPDA', 'value': 'Team IPDA'}
                                ],
                                placeholder='Select Division'
                            ), width=6),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(dbc.Button("Pair (Next) Elim Round", id="pair-elim-button", className="ml-auto")),
                        ], className='my-3 align-items-center'),
                    ]),

                    dcc.Tab(label='Manage Judging', children=[
                        dbc.Row([
                            dbc.Col(html.Label('Round'), width=4),
                            dbc.Col(dcc.Dropdown(
                                id='judging-round-select-dropdown',
                                options=[],  # Populate options dynamically based on callback
                                placeholder='Select Round'
                            ), width=6),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(dbc.Table(id='judging-table', striped=True, bordered=True, hover=True), width=12),
                        ], className='mb-3', justify='center'),

                        dbc.Row([
                            dbc.Col(html.Label('Round'), width=4),
                            dbc.Col(dcc.Dropdown(
                                id='ballot-round-select-dropdown',
                                options=[],  # Populate options dynamically based on callback
                                placeholder='Select Round'
                            ), width=6),
                        ], className='mb-3'),

                        dbc.Row([
                            dbc.Col(dbc.Button("Send Round Ballots", id="send-ballot-button", className="ml-auto")),
                        ], className='my-3 align-items-center'),
                    ]),
                ]), width=12),
            ], className='mb-3', justify='center'),

            ### TABBING MODAL ###
            dbc.Modal([
                dbc.ModalHeader("Modal Header"),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col(html.Label('Number of Rounds:'), width=6),
                        dbc.Col(dcc.Dropdown(
                            id='tabbing-round-dropdown',
                            options=[
                                {"label": str(i), "value": i} for i in range(11)
                            ],
                        ), width=6),
                    ]),
                ]),
                dbc.ModalFooter(
                    dbc.Button("Save", id="close-modal-button", className="ml-auto")
                ),
            ], id="tabbing-modal", is_open=False),
            dbc.Modal([
                dbc.ModalHeader("Success"),
                dbc.ModalBody("Pairing Completed Successfully."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-success-modal", className="ml-auto")
                ),
            ], id="pairing-success-modal", is_open=False),
            dcc.Interval(id="modal-auto-close", interval=2500, n_intervals=0, disabled=True),
            
            dbc.Modal([
                dbc.ModalHeader("Success"),
                dbc.ModalBody("Ballots Sent Successfully"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-judge-success-modal", className="ml-auto")
                ),
            ], id="judge-success-modal", is_open=False),
            dcc.Interval(id="judge-modal-auto-close", interval=2500, n_intervals=0, disabled=True)
        ])
