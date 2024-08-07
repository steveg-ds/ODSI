import dash_bootstrap_components as dbc

def speaker_point_calculator_modal():
    return dbc.Modal([
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