import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from logger_config import logger

class Controller:
    def __init__(self, tournament, db, model, server):
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.tournament = tournament
        self.db = db
        self.model = model
        self.app.layout = self.tournament.setup_layout()
        self.setup_callbacks()

    ### Callbacks for set up tournament page ### 
    def setup_callbacks(self):
        # Callback for handling file uploads
        @self.app.callback(
            Output('debaters-file-name', 'children'),
            Output('judges-file-name', 'children'),
            Output('rooms-file-name', 'children'),
            Input('upload-debaters', 'filename'),
            Input('upload-judges', 'filename'),
            Input('upload-rooms', 'filename'),
            Input('upload-debaters', 'contents'),
            Input('upload-judges', 'contents'),
            Input('upload-rooms', 'contents'),
            prevent_initial_call=True
        )
        def update_file_labels(debaters_filename, judges_filename, rooms_filename, debaters_contents, judges_contents, rooms_contents):
            """
            Update file labels and process uploaded CSV files for debaters, judges, and rooms.

            Args:
                debaters_filename (str): Filename of the debaters CSV file.
                judges_filename (str): Filename of the judges CSV file.
                rooms_filename (str): Filename of the rooms CSV file.
                debaters_contents (str): Contents of the debaters CSV file.
                judges_contents (str): Contents of the judges CSV file.
                rooms_contents (str): Contents of the rooms CSV file.

            Returns:
                tuple: Alerts indicating CSV validity and updated file labels for debaters, judges, and rooms.
            """
            logger.info("Updating file labels.")

            # Initialize alerts with default values
            debaters_alert = "No file uploaded"
            judges_alert = "No file uploaded"
            rooms_alert = "No file uploaded"

            # TODO: rewrite this to only call set tournament entries once 
            try:
                # Validate and retrieve dataframes for debaters
                if debaters_filename and debaters_contents:
                    debaters_alert, debaters = self.model.get_file_alert_and_df(debaters_filename, debaters_contents)
                    self.model.set_tournament_entries(debaters=debaters)
                    debaters_alert = "Debaters file uploaded successfully"

                # Validate and retrieve dataframes for judges
                if judges_filename and judges_contents:
                    judges_alert, judges = self.model.get_file_alert_and_df(judges_filename, judges_contents)
                    self.model.set_tournament_entries(judges=judges)
                    judges_alert = "Judges file uploaded successfully"

                # Validate and retrieve dataframes for rooms
                if rooms_filename and rooms_contents:
                    rooms_alert, rooms = self.model.get_file_alert_and_df(rooms_filename, rooms_contents)
                    self.model.set_tournament_entries(rooms=rooms)
                    rooms_alert = "Rooms file uploaded successfully"

            except Exception as e:
                logger.error(f"Error processing uploaded files: {str(e)}")
                debaters_alert = f"Error: {str(e)}"
                judges_alert = f"Error: {str(e)}"
                rooms_alert = f"Error: {str(e)}"

            return debaters_alert, judges_alert, rooms_alert

        # Callback for handling form submission
        @self.app.callback(
            Output('submit-button', 'n_clicks'),
            Input('submit-button', 'n_clicks'),
            State('tournament-name', 'value'),
            State('tournament-start-date', 'value'),
            State('tournament-end-date', 'value'),
            prevent_initial_call=True
        )
        def handle_submit(n_clicks, tournament_name, start_date, end_date):
            """
            Handles the submission of tournament data.

            Args:
                n_clicks (int): Number of times the submit button has been clicked.
                tournament_name (str): Name of the tournament.
                start_date (str): Start date of the tournament.
                end_date (str): End date of the tournament.

            Returns:
                None
            """
            if n_clicks:
                logger.info(f"Submit button clicked. Tournament: {tournament_name}, Start Date: {start_date}, End Date: {end_date}")

                try:
                    # Set tournament data in the model
                    self.model.set_tournament_data(tournament_name, start_date, end_date)
                    
                    # Process tournament data
                    self.model.process_tournament_data()
                    
                    logger.info("Successfully processed tournament data.")
                
                except ValueError as ve:
                    logger.error(f"ValueError processing tournament data: {ve}")
                
                except KeyError as ke:
                    logger.error(f"KeyError processing tournament data: {ke}")
                
                except Exception as e:
                    logger.error(f"Error processing tournament data: {e}")

            return None


        ### callbacks for manage tournament ### 
        # Callback for updating tournament dropdown
        @self.app.callback(
            Output('tournament-dropdown', 'options'),
            [Input('tournament-dropdown', 'value')]
        )
        def update_dropdown_options(value):
            """
            Updates dropdown options based on the selected value.

            Args:
                value (str): The selected value from the dropdown.

            Returns:
                list: Updated options for the dropdown, each as a dictionary with 'label' and 'value' keys.
            """
            try:
                logger.info("Updating tournament dropdown options.")
                options = self.model.update_dropdown_options(value)
                
                if options is None:
                    options = []  # Handle None case
                
                # Ensure options is a list; if not, log an error and return an empty list
                if not isinstance(options, list):
                    logger.error(f"Invalid options type: {type(options)}. Expected list.")
                    return []
                
                return options
            
            except ValueError as ve:
                logger.error(f"ValueError updating dropdown options: {ve}")
                return [{'label': 'Error retrieving data', 'value': None}]
            
            except KeyError as ke:
                logger.error(f"KeyError updating dropdown options: {ke}")
                return [{'label': 'Error retrieving data', 'value': None}]
            
            except Exception as e:
                logger.error(f"Error updating dropdown options: {e}")
                return [{'label': 'Error retrieving data', 'value': None}]
        ### Tournament Overview CALLBACKS### 
        
        # Callback for populating search dropdowns based on tournament selection
        @self.app.callback(
            Output('name-dropdown', 'options'),
            Output('school-dropdown', 'options'),
            Output('division-dropdown', 'options'),
            Input('tournament-dropdown', 'value'),
            Input('entry-type-dropdown', 'value'),
            prevent_initial_call=True
        )
        def populate_search_dropdowns(tournament_name, entry_type):
            """
            Populates the search dropdowns with debater names, schools, and divisions for a given tournament.

            Args:
                tournament_name (str): The name of the tournament for which to populate the dropdowns.

            Returns:
                tuple: A tuple containing lists of debater names, schools, and divisions.
            """
            try:
                if tournament_name:
                    logger.info(f"Populating search dropdowns for tournament: {tournament_name}")
                    return self.model.populate_search_dropdowns(tournament_name, entry_type)
                else:
                    logger.warning("No tournament name provided for populating dropdowns.")
                    return [], [], []
            except Exception as e:
                logger.error(f"Error populating search dropdowns: {e}")
                return [], [], []
        
        # Callback for updating the overview table based on filters
        @self.app.callback(
            Output('overview-table', 'children'),
            [
                Input('tournament-dropdown', 'value'),
                Input('entry-type-dropdown', 'value'),
                Input('name-dropdown', 'value'),  
                Input('school-dropdown', 'value'),  
                Input('division-dropdown', 'value') 
            ],
            prevent_initial_call=True
        )
        def update_overview_table(tournament_name, category, name, school, division):
            """
            Updates the overview table based on selected filters.

            Args:
                tournament_name (str): The name of the tournament to filter data from.
                category (str): The category to filter on (e.g., debater, judge).
                name (str): The name of the individual to filter.
                school (str): The school of the individual to filter.
                division (str): The division to filter on (e.g., Novice, Varsity).

            Returns:
                dash_table.DataTable: A DataTable object populated with filtered data.
            """
            try:
                df = self.model.update_overview_table(tournament_name, category, name, school, division)
                logger.info("Updating overview table.")
                return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            except Exception as e:
                logger.error(f"Error updating overview table: {e}")
                # Return an empty table or handle the error as per your application's logic
                return dbc.Table()

        @self.app.callback(
    Output('action-info-header', 'children'),
    Output('action-info-body', 'children'),
    Output('action-info-modal', 'is_open'),
    Output('action-info-auto-close', 'disabled'),
    Input('action-modal-button', 'n_clicks'),
    Input('close-action-info-modal', 'n_clicks'),
    Input('action-info-auto-close', 'n_intervals'),
    State('tournament-dropdown', 'value'),
    State('action-dropdown', 'value'),
    State('entry-type-dropdown', 'value'),
    State('name-dropdown', 'value'),
    State('school-dropdown', 'value'),
    State('division-dropdown', 'value'),
    State('new-entry-value', 'value'),
    State('action-info-modal', 'is_open')
        )
        def update_modal_body(action_click, close_click, n_intervals, tournament_name, action, entry_type, entry_name, entry_school, entry_division, new_value, is_open):
            try:
                if close_click or n_intervals > 0:
                    return "", "", False, True

                if action_click is None or action_click == 0:
                    return "", "", False, True

                if not (tournament_name and action):
                    return "", "", False, True

                logger.info(f"{action} was selected for {tournament_name}.")

                if entry_school is not None:
                    message_name = entry_school + " " + entry_name.split(" ")[-1]
                else:
                    message_name = entry_name
                
                message = ""

                if action == 'Set Active Tournament':
                    is_active_tournament = self.model.set_active_tournament(tournament_name)

                    if is_active_tournament:
                        message = f"{tournament_name} set as active tournament."
                    else:
                        message = f"{tournament_name} is already set as the active tournament."

                elif action == 'Change Division':
                    update_successful = self.model.update_division(
                        tournament_name=tournament_name,
                        entry_name=entry_name,
                        entry_school=entry_school,
                        entry_division=entry_division,
                        new_division=new_value
                    )

                    if update_successful:
                        message = f"Division updated for {message_name}."
                    else:
                        message = f"Failed to update division for {message_name}."
                        
                elif action == 'Change Name':
                    update_successful = self.model.update_name(
                        tournament_name=tournament_name,
                        entry_type=entry_type,
                        entry_name=entry_name,
                        new_name=new_value
                    )

                    if update_successful:
                        message = f"Name updated for {message_name}."
                    else:
                        message = f"Failed to update name for {message_name}."
                        
                elif action == 'Change School':
                    update_successful = self.model.update_school(
                        tournament_name=tournament_name,
                        entry_type=entry_type,
                        entry_name=entry_name,
                        entry_school=entry_school,
                        new_school=new_value
                    )

                    if update_successful:
                        message = f"School updated for {message_name}."
                    else:
                        message = f"Failed to update school for {message_name}."

                elif action == 'Remove Entry':
                    if entry_type in ['Debaters', 'Judges']:
                        update_successful = self.model.remove_entry(
                            tournament_name=tournament_name,
                            entry_type=entry_type,
                            entry_name=entry_name,
                            entry_school=entry_school
                        )
                    elif entry_type == "Rooms":
                        update_successful = self.model.remove_room(
                            tournament_name=tournament_name,
                            entry_name=entry_name
                        )

                    if update_successful:
                        message = f"Entry for {message_name} removed."
                    else:
                        message = f"Failed to remove entry for {message_name}."

                return "Success", message, True, False

            except Exception as e:
                logger.error(f"Exception in update_modal_body: {e}")
                return "", "An error occurred. Please try again.", True, False



      
    ### TABBING TAB CALLBACKS### 
    
        @self.app.callback(
            Output('tabbing-modal', 'is_open'),
            [Input('tabbing-modal-button', 'n_clicks'),
            Input('close-modal-button', 'n_clicks'),
            Input('tournament-dropdown', 'value'),
            Input('tabbing-round-dropdown', 'value'),
            Input("elim-division-dropdown", 'value')],
            [State('tabbing-modal', 'is_open')],
            prevent_initial_call=True
        )
        def toggle_tabbing_modal(open_clicks, close_clicks, tournament_name, num_rounds, division, is_open):
            """
            Toggles the visibility of the tabbing modal based on button clicks.

            Args:
                open_clicks (int): Number of times the open modal button has been clicked.
                close_clicks (int): Number of times the close modal button has been clicked.
                tournament_name (str): Name of the tournament.
                num_rounds (int): Number of preliminary rounds.
                division (str): Division name (e.g., Novice, Varsity).
                is_open (bool): Current state of the modal (open or closed).

            Returns:
                bool: Updated state of the modal (open or closed).
            """
            ctx = dash.callback_context

            if not ctx.triggered:
                return is_open

            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if button_id == 'close-modal-button':
                logger.info("Closing tabbing modal.")
                
                # Update tournament preliminary rounds and structure
                self.model.update_tournament_prelim_num(tournament_name=tournament_name, num_rounds=num_rounds)
                self.model.insert_tournament_structure(tournament_name=tournament_name, num_rounds=num_rounds)
                
                # Tabulate prelims and add preliminary judges
                self.model.tabulate_prelims(tournament_name)
                self.model.add_prelim_judges(tournament_name, division)
                
                return False
            elif button_id == 'tabbing-modal-button':
                return not is_open

            return is_open
            
        @self.app.callback(
    Output('tabbing-round-select-dropdown', 'options'),
    [Input('tournament-dropdown', 'value')],
            prevent_initial_call=True
        )
        def update_round_select_options(tournament_name):
            """
            Updates the options for the round selection dropdown based on the selected tournament name.

            Args:
                tournament_name (str): Name of the tournament.

            Returns:
                list: List of dictionaries representing dropdown options [{ 'label': 'Round 1', 'value': 'Round 1' }, ...].
            """
            if not tournament_name:
                return []

            try:
                # Fetch the number of rounds based on the selected tournament name
                rounds = self.model.get_num_rounds(tournament_name)
                rounds = int(rounds)
                
                # Generate options for each round
                options = [{'label': f"Round {round_num}", 'value': f"Round {round_num}"} for round_num in range(1, rounds + 1)]
                
                logger.info(f"Updated round select options: {options}")
                
                return options
            
            except Exception as e:
                logger.error(f"Error updating round select options: {e}")
                return []
        
        @self.app.callback(
            Output('postings-table', 'children'),
            [
                Input('tournament-dropdown', 'value'),
                Input('tabbing-division-dropdown', 'value'),
                Input('tabbing-round-select-dropdown', 'value'),  
            ],
            prevent_initial_call=True
        )
        def update_postings_table(tournament_name, division, round_num):
            """
            Updates the postings table for a specific round and division in a tournament.

            Args:
                tournament_name (str): Name of the tournament.
                division (str): Division of the tournament (e.g., 'Novice', 'Varsity').
                round_num (int): Round number for which to update the postings table.

            Returns:
                dbc.Table: Dash Bootstrap Components table populated with postings data.
            """
            try:
                # Fetch the updated postings dataframe
                df = self.model.update_postings_table(tournament_name, division, round_num)
                
                logger.info(f"Updated postings table for {tournament_name}, {division}, Round {round_num}")
                
                # Convert the dataframe to a Dash Bootstrap Components table
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
                
                return table
            
            except Exception as e:
                logger.error(f"Error updating postings table: {e}")
                # Return an empty table or handle the error as appropriate for your application
                return dbc.Table([])
        
        @self.app.callback(
    Output("pairing-success-modal", "is_open"),
    [Input("pair-elim-button", "n_clicks"), 
     Input("close-success-modal", "n_clicks"), 
     Input("modal-auto-close", "n_intervals"), 
     Input('tournament-dropdown', 'value'),
     Input('elim-division-dropdown', 'value')],
    [State("pairing-success-modal", "is_open")],
            prevent_initial_call=True
        )
        def toggle_success_modal(run_clicks, close_clicks, n_intervals, tournament_name, division, is_open):
            """
            Toggle the success modal for displaying pairing success information.

            Args:
                run_clicks (int): Number of times the pair-elim-button has been clicked.
                close_clicks (int): Number of times the close-success-modal or modal-auto-close buttons have been clicked.
                n_intervals (int): Number of intervals passed since last update.
                tournament_name (str): Name of the tournament.
                division (str): Division of the tournament (e.g., 'Novice', 'Varsity').
                is_open (bool): Current state of the modal (open or closed).

            Returns:
                bool: Updated state of the success modal (open or closed).
            """
            ctx = dash.callback_context

            if not ctx.triggered:
                return is_open

            prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if prop_id == "pair-elim-button" and run_clicks:
                # Attempt to pair one elimination round
                if self.model.pair_one_elim(tournament_name=tournament_name, division=division):
                    round_name = self.model.get_current_elim_round_name(tournament_name, division)
                    logger.info(f"Paired {round_name} successfully.")
                    
                    # Update modal text with the round name
                    # Replace 'modal_text' with your actual modal text state variable
                    self.modal_text = f"Successfully paired {round_name}."
                    
                    return True
                else:
                    return is_open
            elif prop_id in ["close-success-modal", "modal-auto-close"]:
                return False

            return is_open

        @self.app.callback(
            Output("modal-auto-close", "disabled"),
            [Input("pair-elim-button", "n_clicks")],
            prevent_initial_call=True
        )
        def start_auto_close_interval(n_clicks):
            """
            Start an auto-close interval when a button is clicked.

            Args:
                n_clicks (int): Number of times the button is clicked.

            Returns:
                bool: True to start the auto-close interval, False otherwise.
            """
            if n_clicks:
                # If the button is clicked at least once, return False to stop auto-closing
                return False
            else:
                # Return True to start the auto-close interval if button hasn't been clicked
                return True
            
        ### JUDGING TAB CALBACKS ###
        
        @self.app.callback(
            [
                Output('judging-round-select-dropdown', 'options'),
                Output('ballot-round-select-dropdown', 'options')
            ],
            [Input('tournament-dropdown', 'value')],
            prevent_initial_call=True
        )
        def update_round_select_options(tournament_name):
            """
            Updates the options for the round selection dropdown based on the selected tournament name.

            Args:
                tournament_name (str): Name of the tournament.

            Returns:
                list: List of dictionaries representing dropdown options [{ 'label': 'Round 1', 'value': 'Round 1' }, ...].
            """
            if not tournament_name:
                return []

            try:
                # Fetch the number of rounds based on the selected tournament name
                prelim_rounds, elim_rounds = self.model.get_num_rounds(tournament_name)
                prelim_rounds = int(prelim_rounds)
                
                # Generate options for each round
                options = [{'label': f"Round {round_num}", 'value': f"Round {round_num}"} for round_num in range(1, prelim_rounds + 1)]
                
                elim_rounds = [{'label': elim_round, 'value': elim_round} for elim_round in elim_rounds]
                
                options.extend(elim_rounds)
                logger.info(elim_rounds)
                logger.info(f"Updated round select options: {options}")
                
                return options, options
            
            except Exception as e:
                logger.error(f"Error updating round select options: {e}")
                return []
        @self.app.callback(
            Output('judging-table', 'children'),
            [
                Input('tournament-dropdown', 'value'),
                Input('judging-round-select-dropdown', 'value'), 
            ],
            prevent_initial_call=True
        )
        def update_judging_table(tournament_name, round_num=None, division=None):
            """
            Updates the postings table for a specific round and division in a tournament.

            Args:
                tournament_name (str): Name of the tournament.
                round_num (int): Round number for which to update the postings table.

            Returns:
                dbc.Table: Dash Bootstrap Components table populated with judge data.
            """
            try:
                logger.info(f"Updating judging table for {tournament_name}, Division {division}, Round {round_num}")
                
                # Fetch the updated postings dataframe
                df = self.model.update_judging_table(tournament_name, round_num, division)
                
                # Convert the dataframe to a Dash Bootstrap Components table
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
                
                return table
            
            except Exception as e:
                logger.error(f"Error updating judge table: {e}")
                # Return an empty table or handle the error as appropriate for your application
                return dbc.Table([])
            
        @self.app.callback(
        [
            Output("judge-success-modal", "is_open"),
            Output("judge-modal-auto-close", "disabled"),
            Output("judge-modal-auto-close", "n_intervals")
        ],
        [
            Input("send-ballot-button", "n_clicks"),
            
            Input('tournament-dropdown', 'value'),
             Input('ballot-round-select-dropdown', 'value'),
        ],
        prevent_initial_call=True
        )
        def toggle_judge_success_modal(n_clicks, tournament_name, round_num):
            """
            Toggle the judge success modal based on the number of clicks on send-ballot-button.

            Args:
                n_clicks (int): Number of times the send-ballot-button has been clicked.

            Returns:
                tuple: A tuple containing the is_open state of the modal, whether the auto-close interval is disabled,
                    and the number of intervals (to reset the auto-close timer).
            """
            
            # TODO: the modal pops up but the close button doesn't work and the timer doesn't work
            
            ctx = dash.callback_context

            if not ctx.triggered:
                raise dash.exceptions.PreventUpdate

            # Example condition to trigger the modal
            condition_to_trigger_modal = True  # Replace with your function or condition to trigger the modal

            # Check if the send-ballot-button was clicked
            if ctx.triggered[0]["prop_id"].split(".")[0] == "send-ballot-button":
                logger.info(round_num)
                active_round = self.model.update_active_round(tournament_name, round_num)
                
                if active_round:
                    logger.info("Attempting to send emails to Judges")
                    self.model.notify_judges_of_ballots(tournament_name)
                return active_round, False, 0  # Show modal and enable auto-close interval

            return False, True, 0  # Hide modal and keep auto-close interval disabled

    def run(self):
        self.app.run(debug=True, port=5000, host='0.0.0.0')
