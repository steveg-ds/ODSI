import dash
from dash import Input, Output, State
import dash_bootstrap_components as dbc
from judging import Judging  
from logger_config import logger

class Controller:
    def __init__(self, app, model):
        """
        Initializes the Controller class.

        This constructor sets up the Dash application and the model, retrieves the layout from the Judging class,
        and sets up the necessary callbacks for the application.

        Args:
            app (dash.Dash): The Dash application instance.
            model (object): The model instance that handles the business logic and data operations.

        Attributes:
            app (dash.Dash): The Dash application instance.
            model (object): The model instance that handles the business logic and data operations.
            judging_layout (dict): The layout dictionary retrieved from the Judging class.

        Returns:
            None
        """
        self.app = app
        self.model = model
        self.judging_layout = Judging.layout()  

        # Setup callbacks during initialization
        self.setup_callbacks()

    def setup_callbacks(self):
        """
        Sets up Dash callbacks for various UI interactions.
        """
        @self.app.callback(
        [
            Output('aff-name', 'children'),
            Output('neg-name', 'children'),
            Output('set-judge-name', 'children'),
            Output('set-round-number', 'children'),
            Output('tournament-name', 'children'),
            Output('modal', 'is_open'),
            Output('no-ballot-modal', 'is_open'),
            Output('no-ballot-body', 'children')
        ],
        [Input('login-button', 'n_clicks'),
        Input('no-ballot-button', 'n_clicks')],
        [
            State('login-username', 'value'),
            State('login-password', 'value'),
            State('no-ballot-modal', 'is_open')
        ],
        prevent_initial_call=True
        )
        def update_inputs_on_login(login_clicks, no_ballot_clicks, login_username, login_password, no_ballot_is_open):
            """
            Update hidden inputs in the UI based on the login attempt and handle closing the no-ballot modal.

            Args:
                login_clicks (int): Number of times the login button has been clicked.
                no_ballot_clicks (int): Number of times the no-ballot button has been clicked.
                login_username (str): Username entered in the login form.
                login_password (str): Password entered in the login form.
                no_ballot_is_open (bool): Current state of the no-ballot modal (open or closed).

            Returns:
                tuple: Updated values for affirmative name, negative name, judge name, round number, tournament name, modal is_open,
                no_ballot_modal is_open, and the content for no-ballot-body.
            """
            
            logger.debug(f"Login button clicked. n_clicks: {login_clicks}, username: {login_username}")

            ctx = dash.callback_context
            if ctx.triggered and ctx.triggered[0]['prop_id'] == 'no-ballot-button.n_clicks':
                # Close the no-ballot modal if the no-ballot button was clicked
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True, False, ""

            if login_username is not None and login_password is not None:
                # Attempt to validate login credentials
                debate, action = self.model.validate_login(login_username, login_password)
                

                if action == 'close modal':
                    # Call update_round_info to get the updated values and modal state
                    updated_values = self.model.update_round_info(debate)

                    if updated_values is not None:
                        # Unpack the returned values
                        affirmative_name, negative_name, judge_name, round_number, tournament_name, modal_open = updated_values

                        # Return the updated values and modal state
                        return affirmative_name, negative_name, judge_name, round_number, tournament_name, False, False, ""
                elif action == 'no ballot':
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True, True, "No ballot found for the current debate."
                elif action == 'invalid credentials':
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True, False, "Invalid username or password."

            # Default return if login credentials are missing
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True, False, "Please enter your username and password."


        @self.app.callback(
            [
                Output('aff-speaks', 'children'),
                Output('neg-speaks', 'children')
            ],
            [
                Input('close-calc', 'n_clicks'),
                Input("delivery-aff", "value"),
                Input("courtesy-aff", "value"),
                Input("tone-aff", "value"),
                Input("org-aff", "value"),
                Input("logic-aff", "value"),
                Input("sup-aff", "value"),
                Input("cx-aff", "value"),
                Input("ref-aff", "value"),
                Input("delivery-neg", "value"),
                Input("courtesy-neg", "value"),
                Input("tone-neg", "value"),
                Input("org-neg", "value"),
                Input("logic-neg", "value"),
                Input("sup-neg", "value"),
                Input("cx-neg", "value"),
                Input("ref-neg", "value"),
                State('set-judge-name', 'children'),
                State('set-round-number', 'children'),
                State('aff-name', 'children'),
                State('neg-name', 'children')
            ], 
            prevent_initial_call=True
        )
        def update_speaks_inputs(n_clicks,
            delivery_aff, courtesy_aff, tone_aff, org_aff, logic_aff, sup_aff, cx_aff, ref_aff, delivery_neg, courtesy_neg, tone_neg, org_neg, logic_neg, sup_neg, cx_neg, ref_neg, judge_name, round_number, affirmative_name, negative_name):
            """
            Update hidden inputs for speaker points based on user inputs.

            Args:
                n_clicks (int): Number of times the update function has been clicked.
                delivery_aff, courtesy_aff, tone_aff, org_aff, logic_aff, sup_aff, cx_aff, ref_aff (float): Affirmative speaker points inputs.
                delivery_neg, courtesy_neg, tone_neg, org_neg, logic_neg, sup_neg, cx_neg, ref_neg (float): Negative speaker points inputs.
                judge_name (str): Name of the judge.
                round_number (str): Round number information.
                affirmative_name (str): Name of the affirmative team.
                negative_name (str): Name of the negative team.

            Returns:
                tuple: Labels for affirmative and negative speaker points to update UI.
            """
            # Labels for affirmative and negative speaker points
            aff_speaks_label = "AFFIRMATIVE (Speaker Points)"
            neg_speaks_label = "NEGATIVE (Speaker Points)"

            if n_clicks and n_clicks > 0:
                # Log debug message when updating speaker points 
                logger.debug("Updating speaker points ")
                
                # Calculate affirmative speaker points
                aff_speaker_points = self.model.calculate_speaker_points(
                    delivery_aff, courtesy_aff, tone_aff, org_aff, logic_aff, sup_aff, cx_aff, ref_aff
                )
                
                # Calculate negative speaker points
                neg_speaker_points = self.model.calculate_speaker_points(
                    delivery_neg, courtesy_neg, tone_neg, org_neg, logic_neg, sup_neg, cx_neg, ref_neg
                )
                
                # Check if calculations returned None (invalid inputs)
                if aff_speaker_points is None:
                    aff_speaks_label = "Invalid Inputs for Affirmative"
                else:
                    aff_speaks_label = f"Speaker Points: {aff_speaker_points}"
                
                if neg_speaker_points is None:
                    neg_speaks_label = "Invalid Inputs for Negative"
                else:
                    neg_speaks_label = f"Speaker Points: {neg_speaker_points}"

            # Return updated labels for affirmative and negative speaker points
            return aff_speaks_label, neg_speaks_label


        

        @self.app.callback(
            [
                Output("signup-modal", "is_open"),
                Output("signup-error-modal", "is_open"),
                Output("signup-error-message", "children"),
            ],
            [
                Input("signup-button", "n_clicks"),
                Input("close-signup-modal", "n_clicks"),
                Input("submit-signup", "n_clicks"),
                Input("close-signup-error-modal", "n_clicks"),
            ],
            [
                State("signup-modal", "is_open"),
                State("signup-error-modal", "is_open"),
                State("signup-firstname", "value"),
                State("signup-lastname", "value"),
                State("signup-school", "value"),
                State("signup-email", "value"),
                State("signup-username", "value"),
                State("signup-password", "value")
            ], 
            prevent_initial_call=True
        )
        def toggle_signup_modal(signup_clicks, close_signup_clicks, submit_signup_clicks, close_signup_error_clicks,
                        is_open_signup_modal, is_open_signup_error_modal,
                        firstname, lastname, school, email, username, password):
            """
            Toggle the state of signup and signup error modals based on user interactions.

            Args:
                signup_clicks (int): Number of times the signup button has been clicked.
                close_signup_clicks (int): Number of times the close signup modal button has been clicked.
                submit_signup_clicks (int): Number of times the submit signup button has been clicked.
                close_signup_error_clicks (int): Number of times the close signup error modal button has been clicked.
                is_open_signup_modal (bool): Current state of the signup modal (open or closed).
                is_open_signup_error_modal (bool): Current state of the signup error modal (open or closed).
                firstname (str): First name entered in the signup form.
                lastname (str): Last name entered in the signup form.
                school (str): School entered in the signup form.
                email (str): Email entered in the signup form.
                username (str): Username entered in the signup form.
                password (str): Password entered in the signup form.

            Returns:
                tuple: Updated states for the signup modal and signup error modal, and dash.no_update where appropriate.
            """
            ctx = dash.callback_context

            # Check if callback context is triggered
            if not ctx.triggered:
                return is_open_signup_modal, is_open_signup_error_modal, dash.no_update

            # Identify which button triggered the callback
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Handle different button interactions
            if button_id == "signup-button":
                # Toggle signup modal open
                return True, is_open_signup_error_modal, dash.no_update
            elif button_id == "close-signup-modal":
                # Toggle signup modal close
                return False, is_open_signup_error_modal, dash.no_update
            elif button_id == "submit-signup":
                # Validate signup inputs and handle signup submission
                validation_result = self.model.signup_user(firstname=firstname, lastname=lastname, email=email, password=password, school=school, username=username)
                if len(validation_result) == 0:
                    logger.info(f"Signup successful: {username}")
                    return False, is_open_signup_error_modal, dash.no_update
                else:
                    # Log and show signup error if validation fails
                    logger.warning(f"Signup failed: {validation_result}")
                    return is_open_signup_modal, True, validation_result
            elif button_id == "close-signup-error-modal":
                # Toggle signup error modal close
                return is_open_signup_modal, False, dash.no_update

            # Default return if no button is triggered
            return is_open_signup_modal, is_open_signup_error_modal, dash.no_update


        
        @self.app.callback(
            Output("calc-modal", "is_open"),
            [
                Input("open-calc", "n_clicks"),
                Input("close-calc", "n_clicks")
            ],
            [State("calc-modal", "is_open")], 
            prevent_initial_call=True
        )
        def toggle_calc_modal(open_calc_clicks, close_calc_clicks, is_open_calc_modal):
            """
            Toggle the state of the calculator modal based on user interactions.

            Args:
                open_calc_clicks (int): Number of times the open calculator button has been clicked.
                close_calc_clicks (int): Number of times the close calculator button has been clicked.
                is_open_calc_modal (bool): Current state of the calculator modal (open or closed).

            Returns:
                bool: Updated state of the calculator modal.
            """
            ctx = dash.callback_context

            # Check if callback context is triggered
            if not ctx.triggered:
                return is_open_calc_modal

            # Identify which button triggered the callback
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # Handle different button interactions
            if button_id == "open-calc":
                return True  # Open the calculator modal
            elif button_id == "close-calc":
                return False  # Close the calculator modal

            # Default return if no button is triggered
            return is_open_calc_modal

        @self.app.callback(
            [
                Output("submission-modal", "is_open"),
                Output("submission-modal-header", "children"),
                Output("submission-modal-body", "children"),
                Output("submission-modal-button", "children")
            ],
            [
                Input("submit-judging", "n_clicks"), 
                Input("submission-modal-button", "n_clicks")
            ],
            [
                State("submission-modal", "is_open"),
                State("resolution-input", "value"),
                State("aff-speaks", "children"),
                State("neg-speaks", "children"),
                State("aff-comments", "value"),
                State("neg-comments", "value"),
                State("vote-radio", "value"),
                State("competitor-name", "value"),
                State("competitor-school", "value"),
                State("reason-for-decision", "value"),
                State("acknowledge-checklist", "value"),
                State("judge-name", "value"),
                State("judge-school", "value")
            ]
        )
        def toggle_submission_modal(trigger_clicks, close_clicks, is_open, resolution, aff_speaks, neg_speaks, aff_comments, neg_comments, vote_radio, competitor_name, competitor_school, rfd, ack_chk, judge_name, judge_school):
            
            ctx = dash.callback_context

            if not ctx.triggered:
                return is_open, dash.no_update, dash.no_update, "Close"  # Default button text is "Close"
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            ballot = {
                "Resolution": resolution,
                "Affirmative Speaks": int(aff_speaks.split(" ")[-1]),
                "Affirmative Comments": aff_comments,
                "Negative Speaks": int(neg_speaks.split(" ")[-1]),
                "Negative Comments": neg_comments,
                "Competitor Name": competitor_name,
                "Competitor School": competitor_school,
                "Tabula Rasa Checklist": ack_chk,
                "Judge Name": judge_name,
                "Judge School": judge_school,
                "Reason for Decision": rfd,
                "Winning Side": vote_radio,
            }

            
            button_text = "Close"
                                        
            if button_id == "submit-judging" and trigger_clicks:
                
                missing_fields = self.model.check_ballot_fields(ballot)
                
                invalid_judge_name = self.model.validate_judge_name(ballot)
                
                invalid_judge_school = self.model.validate_judge_school(ballot)
                
                invalid_winner_name = self.model.validate_winner_name(ballot)
                
                invalid_winner_school = self.model.validate_winner_school(ballot)
                
                if missing_fields:
                    logger.info("Missing fields warning triggered")
                    
                    header_message = "Missing Fields"
                    body_message = f"The following fields are incomplete: {', '.join(missing_fields)}"
                    
                elif invalid_judge_name:
                    logger.info("Invalid judge name warning triggered")
                    
                    header_message = "Invalid Judge Name"
                    body_message = f"Judge name should be either {self.model.judge_name} or {self.model.judge_full_name}."
                    
                elif invalid_judge_school:
                    logger.info("Invalid judge school warning triggered")
                    
                    header_message = "Invalid Judge School"
                    body_message = f"Judge school should be {self.model.judge_school}."
                    
                elif invalid_winner_name:
                    logger.info("Invalid competitor name warning triggered")
                    
                    competitor_names = [self.model._aff_name, self.model._aff_full_name] if ballot['Winning Side'] == "Affirmative" else [self.model._neg_name, self.model._neg_full_name]
                    
                    header_message = "Invalid Winner Name"
                    body_message = f"Winner name should be either {competitor_names[0]} or {competitor_names[1]}."
                    
                elif invalid_winner_school:
                    logger.info("Invalid competitor school warning triggered")
                    
                    competitor_school = self.model._aff_school if ballot['Winning Side'] == "Affirmative" else self.model._neg_school
                    
                    header_message = "Invalid Winner School"
                    body_message = f"Winning competitor school should be {competitor_school}."
                    
                else:
                    logger.info("No errors found checking ballot")
                    self.model.submit_ballot(ballot)
                    
                    header_message = "Ballot Submitted"
                    body_message = "Your ballot has been submitted successfully."
                
                return not is_open, header_message, body_message, button_text
            
            elif button_id == "submission-modal-button" and close_clicks:
                return False, dash.no_update, dash.no_update, "Close"
            
            return is_open, dash.no_update, dash.no_update, "Close"