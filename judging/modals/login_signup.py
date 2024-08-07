import dash_bootstrap_components as dbc

def login_signup_modal():
    return dbc.Modal([
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
        
    ], id="modal", size="md", is_open=True, backdrop="static")