import dash_bootstrap_components as dbc
from dash import html

def speaker_point_confirmation_modal():
    return dbc.Modal(
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
        )