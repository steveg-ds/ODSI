import dash_bootstrap_components as dbc

def signup_error_modal():
    return dbc.Modal([
                dbc.ModalHeader("Signup Error"),
                dbc.ModalBody(id="signup-error-message", className="text-center"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-signup-error-modal", className="ml-auto")
                ),
            ], id="signup-error-modal", size="md", is_open=False, backdrop="static")