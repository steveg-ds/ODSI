import dash_bootstrap_components as dbc
from dash import html, dcc

def submission_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(id='submission-modal-header', className="text-center"),
            dbc.ModalBody([
                html.Div(id="submission-modal-body", className="text-center")
            ]),
            dbc.ModalFooter(
                dbc.Button(id='submission-modal-button', className="ml-auto")
            )
        ],
        id="submission-modal",
        size="md",
        is_open=False,
        backdrop="static"
    )
    
    
    ### old submission modal callback ###
        # @self.app.callback(
        #     [
        #         Output("general-modal", "is_open"),
        #         Output("general-modal-header", "children"),
        #         Output("general-modal-body", "children")
        #     ],
        #     [
        #         Input("submit-judging", "n_clicks"),
        #         Input("ballot-submission-button", "n_clicks"),
        #         Input("no-ballot-button", "n_clicks")
        #     ],
        #     [
        #         State("aff-speaks", "children"),
        #         State("aff-comments", "value"),
        #         State("neg-speaks", "children"),
        #         State("neg-comments", "value"),
        #         State("competitor-name", "value"),
        #         State("competitor-school", "value"),
        #         State("acknowledge-checklist", "value"),
        #         State("judge-name", "value"),
        #         State("judge-school", "value"),
        #         State("reason-for-decision", "value"),
        #         State("vote-radio", "value"),
        #         State("general-modal", "is_open"),
        #         State("lpw-checkbox", "value")
        #     ],
        #     prevent_initial_call=True
        # )
        # def handle_ballot_submission_and_errors(submit_clicks, ballot_close_clicks, error_close_clicks, aff_speaks, aff_comments, neg_speaks, neg_comments, competitor_name, competitor_school, acknowledge_chk, judge_name, judge_school, rfd, winner, general_modal_is_open, lpw_checkbox_value):
        #     ctx = dash.callback_context

        #     # Check if callback context is triggered
        #     if not ctx.triggered:
        #         return general_modal_is_open, dash.no_update, dash.no_update

        #     # Identify which component triggered the callback
        #     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        #     if trigger_id == "submit-judging" and submit_clicks:
        #         # Validate required fields for ballot submission
        #         missing_fields = self.model.check_ballot_fields(
        #             aff_speaks, aff_comments, neg_speaks, neg_comments, competitor_name,
        #             competitor_school, acknowledge_chk, judge_name, judge_school, rfd, winner
        #         )

        #         if missing_fields:
        #             error_message = "The following fields are incomplete: " + ", ".join(missing_fields)
        #             logger.info("Ballot Submission Error: Incomplete ballot")
        #             return True, "Incomplete Ballot", error_message  # Open general modal with error message

        #         # Handle specific validation checks
        #         if not acknowledge_chk:
        #             return True, "Acknowledgement Required", "Please acknowledge Tabula Rasa"

        #         if competitor_name not in [self.model._aff_name, self.model._neg_name] or competitor_name not in [self.model._aff_full_name, self.model._neg_full_name]:
        #             label = f"Winner name should be either {self.model._aff_name} or {self.model._aff_full_name}" if winner == "Affirmative" else f"Winner name should be either {self.model._neg_name} or {self.model._neg_full_name}"
        #             return True, "Invalid Winner Name", label

        #         if competitor_school not in [self.model._aff_school, self.model._neg_school]:
        #             label = f"School name should be either {self.model._aff_school} or {self.model._neg_school}"
        #             return True, "Invalid School Name", label

        #         if judge_name not in [self.model._judge_name, self.model._judge_full_name] or judge_school != self.model._judge_school:
        #             label = f"Judge name should be either {self.model._judge_name} or {self.model._judge_full_name}"
        #             return True, "Invalid Judge Name", label

        #         if not rfd:
        #             return True, "Reason for Decision Required", "Please provide a reason for decision"

        #         # Check if speaker points are less than 20
        #         if int(aff_speaks) < 20 or int(neg_speaks) < 20:
        #             label = f"Speaker points for {self.model._aff_name} or {self.model._neg_name} are less than 20. Are you sure?"
        #             return True, "Low Speaker Points", label  # Open general modal with speaker point message

        #         # Check for low point win
        #         if winner.lower() == "affirmative":
        #             label = f"Confirm low point win for {self.model._aff_name}" if int(aff_speaks) < int(neg_speaks) else None
        #         else:
        #             label = f"Confirm low point win for {self.model._neg_name}" if int(neg_speaks) < int(aff_speaks) else None

        #         if label:
        #             # Add checkbox to confirm low point win
        #             body_content = html.Div([
        #                 html.P(label),
        #                 dcc.Checklist(
        #                     id="lpw-checkbox",
        #                     options=[{"label": "I confirm the low point win", "value": "confirm"}],
        #                     value=[]
        #                 )
        #             ])
        #             return True, "Confirm Low Point Win", body_content  # Open general modal with LPW message

        #         # Submit ballot if all fields are valid
        #         if self.model.submit_ballot(aff_speaks, aff_comments, neg_speaks, neg_comments, rfd, winner):
        #             logger.info("Ballot Submitted")
        #             return True, "Submission Successful", "Ballot submitted successfully"  # Open general modal with submission message

        #         # Return current states if submit button is not clicked or fields are incomplete
        #         return general_modal_is_open, dash.no_update, dash.no_update

        #     if trigger_id == "no-ballot-button" and error_close_clicks:
        #         # Close the modal when the no ballot button is clicked
        #         return False, dash.no_update, dash.no_update

        #     if trigger_id == "ballot-submission-button" and ballot_close_clicks:
        #         # Handle closing of the general modal
        #         return False, dash.no_update, dash.no_update

        #     # Default return if no specific action is triggered
        #     return general_modal_is_open, dash.no_update, dash.no_update