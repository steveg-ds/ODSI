import dash_bootstrap_components as dbc

def no_ballot_modal():
    return dbc.Modal(
            [
            dbc.ModalHeader("No Ballot "),
            dbc.ModalBody(id='no-ballot-body', className="text-center"),
            dbc.ModalFooter(
                dbc.Button("Close", id="no-ballot-button", className="ml-auto")
            )
            ],
            id='no-ballot-modal'
        )