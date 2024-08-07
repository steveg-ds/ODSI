import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, dcc

class Judging:
    @staticmethod
    def layout():
        return dbc.Container([
            html.Hr(),
            # Header with logos and tournament name
            dbc.Row([
                dbc.Col(html.Img(src="/assets/bpcc_logo.png", height="60px"), width="auto"),
                dbc.Col(html.H3("BS \nSpeech and Debate Tournament", id="tournament-name",className="text-center"), width=True), # this needs an ID so it can update when judge logs in
                dbc.Col(html.Img(src="/assets/bpcc_debate_logo.png", height="60px"), width="auto")
            ], className="align-items-center mb-4"),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Judge: ", id='set-judge-name', className="d-flex justify-content-center"),
        
                        ],
                        className="d-flex flex-column align-items-center"
                    ),
                    dbc.Col(html.Label("Round Number: ",                                                id='set-round-number'),                                 className="d-flex           justify-content-center")
                ],
                className="align-items-center mb-4"
            ),
            html.Hr(),
            # Resolution
            dbc.Row([
                dbc.Col(html.Label("RESOLUTION:", className="font-weight-bold text-center"), width=12),
                dbc.Col(dbc.Input(type="text", id="resolution-input", placeholder="Please Enter the Resolution (e.g. Taxation Is Theft)", value='',), width=12)
            ], className="mb-3"),
            html.Hr(),
            # Affirmative and Negative inputs
            dbc.Row([
                dbc.Col([
                    dbc.Label("AFFIRMATIVE: (write code to show)", className="font-weight-bold text-center", id='aff-name'),
                ], width=6, className="text-center"),
                
                dbc.Col([
                    dbc.Label("NEGATIVE: (write code to show)", className="font-weight-bold text-center", id='neg-name'),
                ], width=6, className="text-center")
            ], className="mb-3"),
            html.Hr(),
            # Points and ranks
            dbc.Row([
                dbc.Col([
                    dbc.Label("AFFIRMATIVE (Speaker Points)", className="font-weight-bold text-center", id='aff-speaks'),
                ], width=4, className="text-center"),
                
                
                dbc.Col([ # TODO: I want these buttons next to each other not on topp of each other 
                    dbc.Label("Please Rank Each Debater 1-5 for Each Category:", className="font-weight-bold text-center"),
                    dbc.Row([
                        dbc.Col(dbc.Button("Open Speaker Point Calculator", color="primary", id="open-calc", size='sm'), width='auto'),
                        dbc.Col(dbc.Button("Open Speaker Point Guide", color="primary", id="open-guide", size='sm'), width='auto'),
                    ], justify="center")
                ], width=4, className="text-center"),

                
                dbc.Col([
                    dbc.Label("NEGATIVE (Speaker Points)", className="font-weight-bold text-center", id='neg-speaks'),
                ], width=4, className="text-center"),
            ], className="mb-3"),
            html.Hr(),
            # Comments section
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
                                            {"label": "AFFIRMATIVE", "value": "affirmative"},
                                            {"label": "NEGATIVE", "value": "negative"}
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
            html.Hr(),
            # RFD
            dbc.Row([
                dbc.Col([
                    dbc.Label("Reason for Decision:", className="font-weight-bold text-center"),
                    dbc.Textarea(id='reason-for-decision', style={"width": "100%", "height": "200px"}, value='')
                ])
            ], className="mb-3"),
            html.Hr(),

            # Competitor and school inputs (centered)
            dbc.Row([
                dbc.Col([
                    dbc.Label("Represented by:", className="font-weight-bold text-center"),
                    dbc.Input(type="text", placeholder="Competitor Name", id="competitor-name", value=''),
                    dbc.Input(type="text", placeholder="Competitor School/Program", id="competitor-school", className="mt-2", value='')
                ], width=12, className="text-center")
            ], className="mb-3"),
            # Acknowledgment checkbox (centered)
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
            
            # Submit button (centered)
            dbc.Row([
                dbc.Col(dbc.Button("Submit", color="primary", id="submit-judging"), width=12, className="text-center")
            ]),
            html.Hr(),
            # Modal for login/signup
            dbc.Modal([
                dbc.ModalHeader("Login or Signup"),
                dbc.ModalBody(
                    dbc.Form([
                        dbc.Row([
                            dbc.Col(dbc.Label("Username", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="text", placeholder="Enter username", id="login-username"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("Password", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="password", placeholder="Enter password", id="login-password"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Button("Login", color="primary", id="login-button"), width=6),
                            dbc.Col(dbc.Button("Signup", color="success", id="signup-button"), width=6)
                        ])
                    ])
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ml-auto")
                ),
            ], id="modal", size="md", is_open=True, backdrop="static"),
            # Modal for signup
            dbc.Modal([
                dbc.ModalHeader("Signup"),
                dbc.ModalBody(
                    dbc.Form([
                        dbc.Row([
                            dbc.Col(dbc.Label("First Name", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="text", placeholder="Enter first name", id="signup-firstname"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("Last Name", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="text", placeholder="Enter last name", id="signup-lastname"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("School", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="text", placeholder="Enter school name", id="signup-school"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("Email Address", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="email", placeholder="Enter email address", id="signup-email"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("Username", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="text", placeholder="Enter username", id="signup-username"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Label("Password", className="font-weight-bold text-center"), width=12),
                            dbc.Col(dbc.Input(type="password", placeholder="Enter password", id="signup-password"), width=12)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Button("Submit", color="success", id="submit-signup"), width=12)
                        ])
                    ])
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-signup-modal", className="ml-auto")
                ),
            ], id="signup-modal", size="md", is_open=False, backdrop="static"),
            # Modal for signup error
            dbc.Modal([
                dbc.ModalHeader("Signup Error"),
                dbc.ModalBody(id="signup-error-message", className="text-center"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-signup-error-modal", className="ml-auto")
                ),
            ], id="signup-error-modal", size="md", is_open=False, backdrop="static"),
            dbc.Modal([
                dbc.ModalHeader("Login Error"),
                dbc.ModalBody(id="login-error-message", className="text-center"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-login-error-modal", className="ml-auto")
                ),
            ], id="login-error-modal", size="md", is_open=False, backdrop="static"),
            # Modal for speaker point calculator
            dbc.Modal([
                dbc.ModalHeader("Speaker Point Calculator", className="text-center"),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Affirmative"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Category (1-5 ):", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Negative"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="delivery-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Delivery", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="delivery-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="courtesy-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Courtesy", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="courtesy-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", 
                                      id="tone-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Appropriate Tone", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="tone-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="org-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Organization", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="org-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="logic-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Logic", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="logic-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="sup-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Support", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="sup-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="cx-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Cross-Examination", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="cx-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Input(type="text", id="ref-aff", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Label("Refutation", className="font-weight-bold text-center"),
                        ], width=4, className="text-center"),
                        dbc.Col([
                            dbc.Input(type="text", id="ref-neg", placeholder="Enter value", className="text-center"),
                        ], width=4, className="text-center"),
                    ], className="mb-3"),
                ], id="calc-modal-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-calc", className="ml-auto")
                ),
            ], id="calc-modal", size="md", is_open=False, backdrop="static"),
            
        dbc.Modal(
            [
                dbc.ModalHeader("Ballot Submitted"),
                dbc.ModalBody("Ballot", className="text-center"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="ballot-submission-button", className="ml-auto")
                )
            ],
            id='ballot-submission-modal'
        ),
            dcc.Interval(id='modal-close-interval', interval=2000, n_intervals=0),
        dbc.Modal(
        [
            dbc.ModalHeader("Ballot Submission Error"),
            dbc.ModalBody(id="incomplete-ballot-message-body", className="text-center"),
            dbc.ModalFooter(
                dbc.Button("Close", id="incomplete-ballot-close-button", className="ml-auto")
            )
        ],
        id='incomplete-ballot-modal',
        is_open=False  # Initially closed
    ),
    dcc.Interval(id="error-modal-close-interval", interval=2500, n_intervals=0),
    
    # speaker point confirmation modal
    dbc.Modal(
            [
                dbc.ModalHeader("Speaker Point Check"),
                dbc.ModalBody(
                    dbc.Row([
                        dbc.Col(html.Label(id='speaker-point-label')),
                        dbc.Col(
                            dbc.Checklist(
                                options=[
                                    {"label": "", "value": True},
                                ],
                                value=[],
                                id="accept-points-checkbox",
                                inline=True
                            ),
                            width="auto"
                        )
                    ], justify="center"),
                    className="text-center",
                    id="speaker-point-body"
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="speaker-point-close-button", className="ml-auto")
                )
            ],
            id='speaker-point-modal',
            is_open=False  # Initially closed
        ),
    
    dbc.Modal(
        [
            dbc.ModalHeader("Confirm Low Point Win"),
            dbc.ModalBody(
                dbc.Row([
                    dbc.Col(html.Label(id='lpw-label')),  # Placeholder for dynamic label text
                    dbc.Col(
                        dbc.Checklist(
                            options=[
                                {"label": "Accept", "value": True},
                            ],
                            value=[],
                            id="accept-lpw-checkbox",
                            inline=True
                        ),
                    )
                ], justify="center"),
                className="text-center",
                id="lpw-point-body"
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="lpw-close-button", className="ml-auto")
            )
    ],
    id='lpw-modal',
    is_open=False  # Initially closed
)


        ], fluid=True)