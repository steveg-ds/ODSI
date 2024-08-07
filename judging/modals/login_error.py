import dash_bootstrap_components as dbc

def login_error_modal():
    return dbc.Modal([
                dbc.ModalHeader("Login Error"),
                dbc.ModalBody(id="login-error-message", className="text-center"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-login-error-modal", className="ml-auto")
                ),
            ], id="login-error-modal", size="md", is_open=False, backdrop="static")