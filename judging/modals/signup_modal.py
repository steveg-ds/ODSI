import dash_bootstrap_components as dbc

def signup_modal():
    return dbc.Modal([
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
            