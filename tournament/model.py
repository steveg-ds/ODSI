import pandas as pd 
from dash import html
import io
import base64
import dash_bootstrap_components as dbc
import random
from typing import Optional
from logger_config import logger

class AutoPropertiesMeta(type):
    def __new__(cls, name, bases, dct):
        for key, value in dct.items():
            if not key.startswith('_') and isinstance(value, property):
                # Create getter
                getter_name = key
                getter = lambda self, key=key: getattr(self, f"_{key}")
                # Create setter
                setter_name = key
                setter = lambda self, value, key=key: setattr(self, f"_{key}", value)
                dct[key] = property(getter, setter)
        return super().__new__(cls, name, bases, dct)

class Model(metaclass=AutoPropertiesMeta): 
    """
    Model class for managing tournament data including debaters, judges, rooms, and tournament details.

    Attributes:
        debaters (DataFrame): DataFrame containing debater information.
        judges (DataFrame): DataFrame containing judge information.
        rooms (DataFrame): DataFrame containing room information.
        tournament_name (str): Name of the tournament.
        start_date (str): Start date of the tournament (format: 'YYYY-MM-DD').
        end_date (str): End date of the tournament (format: 'YYYY-MM-DD').
    """

    def __init__(self, tabbing, db, email):
        """Initialize Model with None values for attributes."""
        
        self.tabbing = tabbing
        self._debaters = None
        self._judges = None
        self._rooms = None
        self._tournament_name = None
        self._start_date = None
        self._end_date = None
        self.db = db
        self.email = email
        
    def log_call(func):
        def wrapper(self, *args, **kwargs):
            logger.info(f"{func.__name__} called")
            return func(self, *args, **kwargs)
        return wrapper
        
    @log_call
    def get_file_alert_and_df(self, filename: str, contents: str) -> tuple:
        """
        Processes an uploaded file and returns an alert message and a DataFrame.

        This method handles the uploaded file, decodes its contents, and reads it into a pandas DataFrame if it is a CSV file.
        It also generates an alert message indicating the status of the file upload.

        Parameters:
            filename (str): The name of the uploaded file.
            contents (str): The contents of the uploaded file, encoded in base64.

        Returns:
            tuple: A tuple containing:
                - alert (dbc.Alert or html.Div): An alert message indicating the status of the file upload.
                - df (pd.DataFrame or None): A DataFrame containing the file data if the file is a valid CSV, otherwise None.
        """
        try:
            if not filename or not contents:
                logger.warning("No file or contents provided")
                return html.Div(), None

            logger.info(f"Received file: {filename}")

            if filename.endswith('.csv'):
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                logger.info(f"CSV file uploaded and read: {filename}")
                alert = dbc.Alert(f"File uploaded: {filename}", color="info", style={'marginTop': '10px'})
                return alert, df
            else:
                logger.error(f"Invalid file type uploaded: {filename}")
                alert = dbc.Alert("Only CSV files are allowed!", color="danger", style={'marginTop': '10px'})
                return alert, None

        except Exception as e:
            logger.error(f"Error processing uploaded file: {filename}, Error: {e}")
            alert = dbc.Alert("Error processing uploaded file!", color="danger", style={'marginTop': '10px'})
            return alert, None
    
    @log_call
    def set_tournament_entries(self, debaters: pd.DataFrame, judges: pd.DataFrame, rooms: pd.DataFrame) -> None:
        """
        Sets the tournament entries for debaters, judges, and rooms.

        This method assigns the provided DataFrames for debaters, judges, and rooms to the respective attributes of the Model class.

        Parameters:
            debaters (pd.DataFrame): DataFrame containing debater information.
            judges (pd.DataFrame): DataFrame containing judge information.
            rooms (pd.DataFrame): DataFrame containing room information.

        Returns:
            None
        """
        try:
            logger.info("Setting tournament entries")
            self.debaters = debaters
            self.judges = judges
            self.rooms = rooms
        except Exception as e:
            logger.error(f"Error setting tournament entries: {e}")
            raise  # Re-raise the exception for higher-level handling
    
    @log_call
    def set_tournament_data(self, tournament_name: str, start_date: str, end_date: str) -> None:
        """
        Sets the tournament data including the name, start date, and end date.

        This method assigns the provided tournament name, start date, and end date to the respective attributes of the Model class.

        Parameters:
            tournament_name (str): The name of the tournament.
            start_date (str): The start date of the tournament (format: 'YYYY-MM-DD').
            end_date (str): The end date of the tournament (format: 'YYYY-MM-DD').

        Returns:
            None
        """
        try:
            logger.info("Setting tournament data")
            self.tournament_name = tournament_name
            self.start_date = start_date
            self.end_date = end_date
        except Exception as e:
            logger.error(f"Error setting tournament data: {e}")
            raise  # Re-raise the exception for higher-level handling
        
    @log_call
    def process_tournament_data(self):
        """
        Processes data from the tournament app and stores it in the database.

        This method processes debaters and judges, ensuring they are associated with their respective schools.
        It also processes the list of rooms and prepares the data for uploading to the database.

        Returns:
            None
        """
        try:
            logger.info("Starting process_tournament_data")

            # Initialize the dictionary to hold schools and their associated debaters and judges
            schools_dict = {}
            
            # Check if debaters data is available
            if self._debaters is not None:
                schools = self._debaters['School'].values.tolist()
                logger.info(f"Found {len(schools)} schools in debaters data")

                # Populate the schools_dict with schools from the debaters data
                for school in schools:
                    schools_dict[school] = {"Debaters": None, "Judges": None}

            # Prepare lists and sets to hold debaters and judges
            all_debaters = []
            all_judges = []
            unique_debater_ids = set()
            unique_judge_ids = set()

            # Process debaters and judges if data is available
            if self.debaters is not None and self.judges is not None:
                logger.info("Processing debaters and judges")

                # Process each school, and filter debaters and judges accordingly
                for school in schools:
                    for idx, debater in enumerate(self.debaters.to_dict(orient='records'), start=1):
                        if debater['School'] == school:
                            debater_entry = {
                                "First Name": debater['First Name'],
                                "Last Name": debater['Last Name'],
                                "Division": debater['Division'],
                                "School": school,
                                "ID": idx
                            }
                            # Ensure debater IDs are unique
                            if idx not in unique_debater_ids:
                                unique_debater_ids.add(idx)
                                all_debaters.append(debater_entry)

                    for idx, judge in enumerate(self.judges.to_dict(orient='records')):
                        if judge['School'] == school:
                            judge_entry = {
                                "First Name": judge['First Name'],
                                "Last Name": judge['Last Name'],
                                "School": school,
                                "Email": judge['Email'], # TODO: eventually this will need to check that email addresses are valid on the tournament setup screen and alert users if there is an invalid email address
                                "ID": idx
                            }
                            # Ensure judge IDs are unique
                            if idx not in unique_judge_ids:
                                all_judges.append(judge_entry)
                                unique_judge_ids.add(idx)

                logger.info(f"Processed {len(all_debaters)} debaters and {len(all_judges)} judges")

            # Prepare the list of rooms
            rooms_list = self.rooms["Rooms"].values.tolist()
            logger.info(f"Processed {len(rooms_list)} rooms")

            # Update the tabbing object with processed data
            self.tabbing.debaters = all_debaters
            self.tabbing.judges = all_judges
            self.tabbing.rooms = rooms_list

            # Prepare data for database insertion
            data = {
                "Tournament Name": self._tournament_name,
                "Start Date": self._start_date,
                "End Date": self._end_date, 
                "Debaters": all_debaters,
                "Judges": all_judges,
                "Rooms": rooms_list,
            }
            
            # Insert the data into the database
            if self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": self.tournament_name}) is None:
                self.db.insert_document(collection_name="Tournaments", document=data)
                logger.info(f"Tournament data for {self._tournament_name} inserted into the database")

        except Exception as e:
            logger.error(f"Error processing tournament data: {e}")
            raise  # Re-raise the exception for higher-level handling
    
    @log_call
    def update_overview_table(self, tournament_name: str, category: str, name: Optional[str] = None, 
                            school: Optional[str] = None, division: Optional[str] = None) -> pd.DataFrame:
        """
        Updates the overview table for a given tournament and category.

        Args:
            tournament_name (str): The name of the tournament.
            category (str): The category to update (e.g., 'Debaters', 'Judges', 'Rooms').
            name (str, optional): The name to filter by (e.g., 'First Last'). Defaults to None.
            school (str, optional): The school to filter by. Defaults to None.
            division (str, optional): The division to filter by. Defaults to None.

        Returns:
            pd.DataFrame: The filtered and updated DataFrame.
        """
        logger.info(f"Updating overview table for tournament: {tournament_name}, category: {category}")

        try:
            # Validate inputs
            if not tournament_name or not category:
                logger.warning("Tournament name or category not provided")
                return pd.DataFrame({"Taxation is theft": [True]})
                    
            # Retrieve the data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if data is None:
                logger.error(f"No data found for tournament: {tournament_name}")
                return pd.DataFrame({"No data found": [True]})
            
            data = pd.DataFrame(data[category])
            logger.info(f"Data retrieved for category: {category}")

            if category != "Rooms": 
                # Remove the 'ID' column from the data
                data.drop("ID", axis=1, inplace=True)
                logger.info("'ID' column dropped from data")

                # Filter data by school if provided
                if school is not None:
                    data = data[data['School'] == school]
                    logger.info(f"Data filtered by school: {school}")

                # Filter data by name if provided
                elif name is not None:
                    first_name, last_name = name.split(" ")
                    data = data.loc[(data['First Name'] == first_name) & (data['Last Name'] == last_name)]
                    logger.info(f"Data filtered by name: {name}")

                # Filter data by division if provided
                elif division is not None:
                    data = data[data['Division'] == division]
                    data.drop("Division", axis=1, inplace=True)
                    logger.info(f"Data filtered by division: {division}")

            return data

        except Exception as e:
            logger.error(f"Error updating overview table: {e}")
            return pd.DataFrame({"Error": [True]})
    
    @log_call
    def set_active_tournament(self, tournament_name: str) -> bool:
        """
        Update the active tournament in the database. Ensures only one active tournament exists.
        
        Parameters:
        - tournament_name (str): The name of the tournament to set as active.

        Returns:
        - bool: True if the operation was successful, raises an exception otherwise.
        """
        try:
            # Ensure tournament_name is a string
            if not isinstance(tournament_name, str):
                raise TypeError("tournament_name must be a string.")
            
            # Find all documents with 'Active Tournament' as a key
            active_tournaments = self.db.find_documents(
                collection_name="Tournaments",
                query={"Active Tournament": {"$exists": True}}
            )

            # If there are no active tournaments, insert the new active tournament
            if len(active_tournaments) == 0:
                self.db.insert_document(
                    collection_name="Tournaments",
                    document={"Active Tournament": tournament_name}
                )
                logger.info(f"Inserted new active tournament: {tournament_name}")

            # If there is one active tournament, update it if necessary
            elif len(active_tournaments) == 1:
                current_active = active_tournaments[0]
                if current_active['Active Tournament'] != tournament_name:
                    self.db.update_document(
                        collection_name="Tournaments",
                        query={"_id": current_active["_id"]},
                        update_data={"$set": {"Active Tournament": tournament_name}}
                    )
                    logger.info(f"Updated active tournament to: {tournament_name}")
                else:
                    logger.info(f"{tournament_name} is already set as active tournament")
                    return False

            # If there are multiple active tournaments, raise an error
            else:
                logger.error("Multiple active tournaments found. Please resolve manually.")
                raise Exception("Multiple active tournaments found. Please resolve manually.")

            return True
        

        except TypeError as e:
            # Log and raise TypeError for incorrect argument types
            logger.error(f"TypeError in update_active_tournament: {e}")
            raise

        except Exception as e:
            # Log and raise unexpected exceptions
            logger.error(f"Exception in update_active_tournament: {e}")
            raise
        
    @log_call
    def update_division(self, tournament_name, entry_name, entry_school, entry_division, new_division):
        """
        Update the division of a debater in a specific tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_name (str): The full name of the debater.
        - entry_school (str): The school of the debater.
        - entry_division (str): The current division of the debater.
        - new_division (str): The new division to assign to the debater.

        Returns:
        - bool: True if the division was successfully updated, False otherwise.
        """
        try:
            # Fetch tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

            if not data:
                logger.error(f"Tournament {tournament_name} not found in the database.")
                return False

            # Split the debater's name to handle cases with compound last names
            original_name = entry_name
            entry_name_parts = entry_name.split(" ")
            combined_last_name = " ".join(entry_name_parts[1:])
            entry_name_parts.append(combined_last_name)

            # Create a name string based on the presence of entry_school
            if entry_school:
                name = entry_school + " " + entry_name_parts[-1]
            else:
                name = original_name

            update_db = False
            matches = 0

            # Iterate through debaters to find and update the target debater's division
            for debater in data['Debaters']:
                if debater['First Name'] == entry_name_parts[0] and debater['Last Name'] == entry_name_parts[1]:
                    if entry_school and debater['School'] == entry_school:
                        if entry_division and debater['Division'] == entry_division:
                            matches += 1
                            update_db = True
                            debater['Division'] = new_division
                        else:
                            matches += 1
                            update_db = True
                            debater['Division'] = new_division
                    else:
                        matches += 1
                        update_db = True
                        debater['Division'] = new_division

            # Handle cases with multiple matches
            if matches > 1:
                logger.error(f"Multiple entries for {name} found in {tournament_name}. Manual resolution required.")
                return False

            # Update the database if a debater was updated
            if update_db:
                logger.info(f"Updated division for {name} in {tournament_name} to {new_division}")
                self.db.update_document(
                    collection_name="Tournaments",
                    query={"Tournament Name": tournament_name},
                    update_data={"Debaters": data['Debaters']}
                )
                return True
            else:
                logger.info(f"{name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in update_division: {e}")
            return False
        
    @log_call
    def update_name(self, tournament_name, entry_type, entry_name, new_name):
        """
        Update the name of a participant in a specific tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_type (str): The type of participant (e.g., "Debaters").
        - entry_name (str): The full name of the participant.
        - entry_school (str): The current school of the participant.
        - new_school (str): The new school to assign to the participant.

        Returns:
        - bool: True if the name was successfully updated, False otherwise.
        """
        try:
            # Fetch the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                logger.error(f"Tournament {tournament_name} not found in the database.")
                return False
            
            # Process the entry_name to handle cases where the last name might have spaces
            original_name = entry_name
            name = entry_name.split(" ")
            split_name = new_name.split(" ")
            
            update_db = False
            
            # Iterate through the entries and perform the necessary checks
            for entry in data[entry_type]:
                if entry['First Name'] == name[0] and entry['Last Name'] == name[1]:
                    logger.info("Found entry")

                    update_db = True
                    entry['First Name'] = split_name[0]
                    entry['Last Name'] = split_name[1]

            # Update the database if a match was found and updated
            if update_db:
                logger.info(f"Updated {entry_type[:-1].lower()} {original_name} name to {new_name} in {tournament_name}")
                
                self.db.update_document(
                    collection_name="Tournaments", 
                    query={"Tournament Name": tournament_name}, 
                    update_data={entry_type: data[entry_type]}
                )
                return True
            else:
                logger.info(f"{name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in update_school: {e}")
            return False
        
        
    @log_call
    def update_school(self, tournament_name, entry_type, entry_name, entry_school, new_school):
        """
        Update the school of a participant in a specific tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_type (str): The type of participant (e.g., "Debaters").
        - entry_name (str): The full name of the participant.
        - entry_school (str): The current school of the participant.
        - new_school (str): The new school to assign to the participant.

        Returns:
        - bool: True if the school was successfully updated, False otherwise.
        """
        try:
            # Fetch the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                logger.error(f"Tournament {tournament_name} not found in the database.")
                return False
            
            # Process the entry_name to handle cases where the last name might be combined
            original_name = entry_name
            entry_name_parts = entry_name.split(" ")
            combined_last_name = " ".join(entry_name_parts[1:])
            entry_name_parts.append(combined_last_name)
            
            # Create the name string based on the presence of entry_school
            name = f"{entry_school} {entry_name_parts[-1]}" if entry_school else original_name
            
            update_db = False
            original_school = None
            
            # Iterate through the entries and perform the necessary checks
            for entry in data.get(entry_type, []):
                if entry['First Name'] == entry_name_parts[0] and entry['Last Name'] == entry_name_parts[1]:

                    update_db = True
                    original_school = entry['School']
                    entry['School'] = new_school

            # Update the database if a match was found and updated
            if update_db:
                name = f"{original_school} {entry_name_parts[-1]}"
                logger.info(f"Updated {entry_type[:-1].lower()} {name} to {new_school} in {tournament_name}")
                self.db.update_document(
                    collection_name="Tournaments", 
                    query={"Tournament Name": tournament_name}, 
                    update_data={entry_type: data[entry_type]}
                )
                return True
            else:
                logger.info(f"{name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in update_school: {e}")
            return False

        
    @log_call
    def remove_entry(self, tournament_name, entry_type, entry_name, entry_school):
        """
        Remove an entry from a specific tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_type (str): The type of participant (e.g., "Debaters").
        - entry_name (str): The full name of the participant.
        - entry_school (str): The school of the participant.

        Returns:
        - bool: True if the entry was successfully removed, False otherwise.
        """
        try:
            # Fetch the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                logger.error(f"Tournament {tournament_name} not found in the database.")
                return False

            # Process the entry_name to handle cases where the last name might be combined
            entry_name_parts = entry_name.split(" ")
            combined_last_name = " ".join(entry_name_parts[1:])
            entry_name_parts.append(combined_last_name)
            name = entry_name_parts[-1]

            update_db = False
            school = ""

            # Filter out the entry to be removed
            filtered_entries = []
            for entry in data.get(entry_type, []):
                if entry['First Name'] == entry_name_parts[0] and entry['Last Name'] == entry_name_parts[1]:
                    school = entry['School']
                    update_db = True
                else:
                    filtered_entries.append(entry)

            # Update the database if a match was found and removed
            if update_db:
                logger.info(f"Removed {entry_type[:-1].lower()} {school + ' ' + name} from {tournament_name}")
                self.db.update_document(
                    collection_name="Tournaments", 
                    query={"Tournament Name": tournament_name}, 
                    update_data={entry_type: filtered_entries}
                )
                return True
            else:
                logger.info(f"{name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in remove_entry: {e}")
            return False
        
    @log_call
    def update_room(self, tournament_name, entry_name, new_room):
        """
        Update the room assignment for a specific entry in a tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_name (str): The current name of the room.
        - new_room (str): The new name of the room.

        Returns:
        - bool: True if the room was successfully updated, False otherwise.
        """
        try:
            # Fetch the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                logger.info(f"Tournament {tournament_name} not found.")
                return False

            update_db = False
            rooms = []

            # Iterate through the room entries to find and update the specified room
            for entry in data.get("Rooms", []):
                if entry != entry_name:
                    rooms.append(entry)
                else:
                    update_db = True
                    rooms.append(new_room)

            # Update the database if the room was found and changed
            if update_db:
                logger.info(f"Changed Room {entry_name} name to {new_room} in {tournament_name}")
                self.db.update_document(
                    collection_name="Tournaments", 
                    query={"Tournament Name": tournament_name}, 
                    update_data={"Rooms": rooms}
                )
                return True
            else:
                logger.info(f"Room {entry_name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in update_room: {e}")
            return False
        
    @log_call
    def remove_room(self, tournament_name, entry_name):
        """
        Remove a room from the list of rooms in a specified tournament.

        Parameters:
        - tournament_name (str): The name of the tournament.
        - entry_name (str): The name of the room to be removed.

        Returns:
        - bool: True if the room was successfully removed, False otherwise.
        """
        try:
            # Fetch the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                logger.info(f"Tournament {tournament_name} not found.")
                return False

            update_db = False
            filtered_entries = []

            # Iterate through the room entries to find and remove the specified room
            for entry in data.get("Rooms", []):
                if entry != entry_name:
                    filtered_entries.append(entry)
                else:
                    update_db = True

            # Update the database if the room was found and removed
            if update_db:
                logger.info(f"Removed {entry_name} from {tournament_name}")
                self.db.update_document(
                    collection_name="Tournaments", 
                    query={"Tournament Name": tournament_name}, 
                    update_data={"Rooms": filtered_entries}
                )
                return True
            else:
                logger.info(f"Room {entry_name} not found in {tournament_name}")
                return False

        except Exception as e:
            logger.error(f"Exception in remove_room: {e}")
            return False

            
    @log_call
    def update_dropdown_options(self, value):
        """
        Updates the dropdown options with the list of tournament names.

        Args:
            value: The current value selected in the dropdown (not used in this function).

        Returns:
            list: A list of dictionaries with 'label' and 'value' keys for each tournament name.
        """
        try:
            logger.info(f"Updating dropdown options with selected value: {value}")

            # Retrieve all tournament documents from the database (excluding active tournaments)
            tournaments = self.db.find_documents(collection_name="Tournaments", query={"Tournament Name": {"$exists": True}})
            logger.info(f"Retrieved {len(tournaments)} tournaments from the database")
            
            # Extract tournament names from the retrieved documents
            names = [tournament['Tournament Name'] for tournament in tournaments]
            logger.info(f"Tournament names: {names}")

            # Create a list of dictionaries for the dropdown options
            dropdown_options = [{'label': name, 'value': name} for name in names]
            logger.info(f"Dropdown options created: {dropdown_options}")

            return dropdown_options

        except Exception as e:
            logger.error(f"Error updating dropdown options: {e}")
            return [{'label': 'Error retrieving data', 'value': None}]
    
    @log_call
    def populate_search_dropdowns(self, tournament_name, entry_type):
        """
        Populates the search dropdowns with debater names, schools, and divisions.

        Args:
            tournament_name (str): The name of the tournament for which to populate the dropdowns.

        Returns:
            tuple: A tuple containing lists of debater names, schools, and divisions.
        """
        try:
            logger.info(f"Populating search dropdowns for tournament: {tournament_name}")

            names = []
            schools = []
            
            divisions = ["NA"] if entry_type == "Judges" else ["Novice", "Junior Varsity", "Varsity", "Professional", "Team IPDA"]

            # Retrieve the tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if data is None:
                logger.error(f"No data found for tournament: {tournament_name}")
                return [], [], divisions

            logger.info(f"Retrieved data for tournament: {tournament_name}")

            # Convert debaters data to a DataFrame and sort by last name
            debaters = pd.DataFrame(data[entry_type])
            debaters.sort_values(by='Last Name', inplace=True)
            names = (debaters['First Name'] + " " + debaters['Last Name']).tolist()

            # Sort debaters by school and extract unique school names
            debaters.sort_values(by='School', inplace=True)
            schools = debaters['School'].unique().tolist()
            logger.info(f"Schools: {schools}")

            logger.info(f"Divisions: {divisions}")

            return names, schools, divisions

        except Exception as e:
            logger.error(f"Error populating search dropdowns for tournament {tournament_name}: {e}")
            return [], [], []


    @log_call
    def update_tournament_prelim_num(self, tournament_name, num_rounds):
        """
        Updates the number of preliminary rounds for a given tournament.

        Args:
            tournament_name (str): The name of the tournament to update.
            num_rounds (int): The number of preliminary rounds to set.
        """
        try:
            logger.info(f"Updating preliminary round number for tournament: {tournament_name} with value: {num_rounds}")
            
            # Add or update the "Num Rounds" field in the specified tournament document
            self.db.update_document(
                collection_name="Tournaments", 
                query={"Tournament Name": tournament_name}, 
                update_data={"Num Rounds": num_rounds}
            )
            
            logger.info(f"Preliminary round number updated successfully for tournament: {tournament_name}")
        
        except Exception as e:
            logger.error(f"Error updating preliminary round number for tournament {tournament_name}: {e}")
            raise  # Re-raise the exception for higher-level handling


        
    @log_call
    def insert_tournament_structure(self, tournament_name, num_rounds):
        """
        Inserts the tournament structure for a given tournament.

        Args:
            tournament_name (str): The name of the tournament to update.
            num_rounds (int): The number of preliminary rounds for the tournament.
        """
        try:
            logger.info(f"Inserting tournament structure for tournament: {tournament_name} with {num_rounds} preliminary rounds.")
            
            # Set the number of preliminary rounds in the tabbing instance
            self.tabbing.num_prelims = num_rounds
            
            # Create the tournament structure
            self.tabbing.create_tournament_structure()
            logger.info(f"Tournament structure created with {num_rounds} preliminary rounds.")
            
            # Add the tournament structure to the database
            self.db.update_document(
                collection_name="Tournaments", 
                query={"Tournament Name": tournament_name}, 
                update_data={"Tournament": self.tabbing.tournament}
            )
            logger.info(f"Tournament structure inserted successfully for tournament: {tournament_name}.")
        
        except Exception as e:
            logger.error(f"Error inserting tournament structure for tournament {tournament_name}: {e}")
            raise  # Re-raise the exception for higher-level handling

    @log_call
    def tabulate_prelims(self, tournament_name):
        """
        Tabulates preliminary rounds for a given tournament.

        This method retrieves tournament data from the database, sets up the debaters, judges, and rooms
        for the tabbing process, creates divisions, pairs preliminary rounds for the 'Novice' division,
        assigns judges for the 'Novice' division, and updates the tournament data in the database.

        Parameters:
            tournament_name (str): The name of the tournament to tabulate prelims for.

        Returns:
            None
        """
        try:
            logger.info(f"Tabulating preliminary rounds for tournament: {tournament_name}")

            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            # Set up tabbing instance with retrieved data
            self.tabbing.debaters = data['Debaters']
            self.tabbing.judges = data['Judges']
            self.tabbing.rooms = data['Rooms']
            self.tabbing.num_prelims = data.get('Num Rounds', 0)  # Handle case where Num Rounds may not exist yet
            
            # Create divisions and tournament structure
            self.tabbing.create_divisions()
            self.tabbing.create_tournament_structure()
            
            # Pair prelims for the 'Novice' division (TODO: Expand for all divisions)
            self.tabbing.pair_prelims_flight_a(division="Novice")
            
            # Update tournament data in the database
            self.db.update_document(collection_name="Tournaments", 
                                    query={"Tournament Name": tournament_name}, 
                                    update_data={"Tournament": self.tabbing.tournament})
            
            logger.info(f"Preliminary rounds tabulated successfully for tournament: {tournament_name}")

        except Exception as e:
            logger.error(f"Error tabulating preliminary rounds for tournament {tournament_name}: {e}")
            raise  # Re-raise the exception for higher-level handling
        
    @log_call
    def add_prelim_judges(self, tournament_name, division):
        """
        Adds preliminary round judges for a specified division in a tournament.

        Retrieves tournament data from the database, assigns judges to debate rounds in the specified division,
        and updates the tournament data in the database.

        Args:
            tournament_name (str): The name of the tournament.
            division (str): The division to add judges for (e.g., 'Novice', 'Varsity').

        Returns:
            None
        """
        
        try:
            logger.info(f"Adding preliminary round judges for tournament: {tournament_name}, division: {division}")

            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            # Assign judges to debate rounds in the specified division
            tournament = self.tabbing.add_judges_flight_a(
                division=division,
                debaters=data['Debaters'],
                judges=data['Judges'],
                rooms=data['Rooms'],
                num_prelims=data.get('Num Rounds', 0),  # Handle case where Num Rounds may not exist
                tournament=data['Tournament']
            )
            
            # Update the tournament data in the database
            self.db.update_document(
                collection_name="Tournaments",
                query={"Tournament Name": tournament_name},
                update_data={"Tournament": tournament}
            )
            
            # Log successful addition of judges
            logger.info(f"Preliminary round judges added successfully for tournament: {tournament_name}, division: {division}")

        except Exception as e:
            logger.error(f"Error adding preliminary round judges for tournament {tournament_name}, division: {division}: {e}")
            raise  # Re-raise the exception for higher-level handling
        
    @log_call
    def get_num_rounds(self, tournament_name):
        """
        Retrieves the number of preliminary rounds for a given tournament.

        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            int: The number of preliminary rounds.
                Returns 0 if tournament data or number of rounds is not found.
        """
        
        # TODO: this should include elimination rounds too 
        
        try:
            logger.info(f"Retrieving number of preliminary rounds for tournament: {tournament_name}")

            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

            if data and 'Num Rounds' in data.keys():
                num_rounds = data['Num Rounds']
                logger.info(f"Number of preliminary rounds retrieved: {num_rounds}")
                
                if "Elim Rounds" in data.keys():
                    elim_rounds = data['Elim Rounds']['Novice']
                    elim_rounds = [debate['Elim Round'] for debate in elim_rounds]
                    return num_rounds, elim_rounds
                
                return num_rounds, None
            else:
                logger.warning(f"No tournament data found or 'Num Rounds' field missing for tournament: {tournament_name}")
                return 0

        except Exception as e:
            logger.error(f"Error retrieving number of preliminary rounds for tournament: {tournament_name}, Error: {e}")
            return 0

    @log_call
    def update_postings_table(self, tournament_name, division, round_num):
        """
        Updates the postings table for a given tournament, division, and round number.

        Args:
            tournament_name (str): The name of the tournament.
            division (str): The division to update (e.g., 'Novice', 'Varsity').
            round_num (str): The round number to update (e.g., 'Round 1', 'Round 2').

        Returns:
            pd.DataFrame: The updated postings table DataFrame.
                Returns a DataFrame with a message if tournament name, division, or round number is missing.
        """
        try:
            logger.info(f"Updating postings table for tournament: {tournament_name}, division: {division}, round number: {round_num}")

            # Check if required parameters are provided
            if not tournament_name or not division or not round_num:
                logger.warning("Tournament name, division, or round number not provided")
                return pd.DataFrame({"Message": ["Tournament name, division, or round number not provided."]})

            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

            if not data:
                logger.error(f"No tournament data found for tournament: {tournament_name}")
                return pd.DataFrame({"Message": [f"No tournament data found for tournament: {tournament_name}"]})

            # TODO: Adjust this logic based on the actual method for creating postings
            # Currently assuming using prelim postings function
            posting = self.tabbing.create_postings(
                division=division,
                round_no=round_num,
                round_data=data['Tournament'][division][round_num],
                debaters=data["Debaters"],
                judges=data["Judges"],
                prelim=True
            )
            
            logger.info("Postings table updated successfully")
            return posting

        except Exception as e:
            logger.error(f"Error updating postings table for tournament: {tournament_name}, division: {division}, round number: {round_num}, Error: {e}")
            return pd.DataFrame({"Error": [f"Error updating postings table: {e}"]})
            
    @log_call
    def pair_one_elim(self, tournament_name, division):
        """
        Pair elimination rounds for a given tournament and division.

        Args:
            tournament_name (str): The name of the tournament.
            division (str): The division to pair elimination rounds for.

        Returns:
            bool: True if pairing is successful, False otherwise.
        """
        elims = {2: "Finals", 4: "Semifinals", 8: "Quarter Finals", 16: "Octofinals", 32: "Double Octofinals", 64: "Triple Octofinals"}

        logger.info(f"Pairing elimination round for tournament: {tournament_name}, division: {division}")

        try:
            # TODO: eventually i should make this first part through the else statement into its own function
            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

            # Filter debaters based on division
            debaters = pd.DataFrame(data['Debaters'])
            debaters = debaters.loc[debaters['Division'] == division]

            # Calculate elimination round and number of breaks
            elim_round, num_breaks = self.tabbing.calculate_breaks(division=division, num_debaters=len(debaters))

            logger.info(f"Initial elimination round: {elim_round}, number of breaks: {num_breaks}")

            # Update or append elimination round info in tournament data
            if "Elim Rounds" not in data.keys():
                logger.info("Adding Elim Rounds to tournament db entry")
                break_info = {division: [{"Elim Round": elim_round, "Num Breaks": num_breaks}]}
                self.db.update_document(collection_name="Tournaments", query={"Tournament Name": tournament_name}, update_data={"Elim Rounds": break_info})
            else:
                if division in data['Elim Rounds'].keys():
                    last_round = data['Elim Rounds'][division][-1]  # Get the last round
                    new_breaks = last_round['Num Breaks'] // 2
                    logger.info(f"New breaks for next round: {new_breaks}")

                    if new_breaks <= 0:
                        logger.error("New breaks calculated to be zero or less. Ending pairing.")
                        return False

                    elim_round_name = elims.get(new_breaks, f"Round with {new_breaks} breaks")
                    data['Elim Rounds'][division].append({"Elim Round": elim_round_name, "Num Breaks": new_breaks})
                    self.db.update_document(collection_name="Tournaments", query={"Tournament Name": tournament_name}, update_data={"Elim Rounds": data['Elim Rounds']})

            # Re-fetch the data to get the latest updates
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if "Elim Rounds" in data.keys():
                elim_rounds = data['Elim Rounds'][division]
                elim_rounds = [round_info['Elim Round'] for round_info in elim_rounds]
                # print(elim_rounds)
            else:
                elim_rounds = None
            
            num_breaks = data["Elim Rounds"][division][-1]['Num Breaks']
            
            # Pair ranked rounds and update tournament data
            ranks, ids = self.tabbing.pair_elim_round(tournament=data['Tournament'], division=division, num_rounds=data['Num Rounds'], elim_rounds=elim_rounds, num_breaks=num_breaks)

            ranks = ranks.to_dict(orient='records')
           
            aff_ids = [id[0] for id in ids]
            neg_ids = [id[1] for id in ids]
            print(aff_ids, neg_ids)
            wins = [
                [random.choice([0, 1]) for _ in range(len(aff_ids))],
                [random.choice([0, 1]) for _ in range(len(aff_ids))],
                [random.choice([0, 1]) for _ in range(len(aff_ids))]
            ]
            wins = list(zip(wins[0], wins[1], wins[2]))
            wins = [0 if sum(win) <= len(win) // 2 else 1 for win in wins]

            # Update tournament data with pairing results
            data['Elim Rounds'][division][-1]['Ranks'] = ranks
            data["Tournament"][division][data['Elim Rounds'][division][-1]['Elim Round']] = {
                "Aff_ID": aff_ids,
                "Aff_Speaks": [0 for _ in range(len(aff_ids))],
                "Neg_ID": neg_ids,
                "Neg_Speaks": [0 for _ in range(len(aff_ids))],
                "Win": wins,
                "Rooms": [random.choice(data['Rooms']) for _ in range(len(aff_ids))],
            }

            # Update tournament data in the database
            self.db.update_document(collection_name="Tournaments", query={"Tournament Name": tournament_name}, update_data={"Tournament": data['Tournament']})

            logger.info("Elimination round paired successfully")
            return True

        except Exception as e:
            logger.error(f"An error occurred while pairing elimination round: {str(e)}")
            return False

    
    @log_call
    def add_elim_judges(self, tournament_name, division):
        """
        Add judges to elimination rounds for a given tournament and division.

        Args:
            tournament_name (str): The name of the tournament.
            division (str): The division to add judges for.

        Returns:
            bool: True if judges are added successfully, False otherwise.
        """
        # try:
        logger.info(f"Adding judges to elimination rounds for tournament: {tournament_name}, division: {division}")

        # Retrieve tournament data from the database
        data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

        # Get the name of the elimination round
        round_name = data['Elim Rounds'][division][-1]['Elim Round']

        # Add judges to the elimination round in the tournament structure
        tournament = self.tabbing.add_elim_judges(debates=data['Tournament'][division], judges=data['Judges'], round_name=round_name, tournament=data['Tournament'], division=division, num_rounds=data['Num Rounds'])

        # Update tournament data in the database
        self.db.update_document(collection_name="Tournaments", query={"Tournament Name": tournament_name}, update_data={"Tournament": tournament})

        logger.info("Judges added to elimination round successfully")
        return True

        # except Exception as e:
        #     logger.error(f"Error adding judges to elimination round for tournament: {tournament_name}, division: {division}, Error: {e}")
        #     return False
        
    @log_call
    def update_judging_table(self, tournament_name,  round_num=None, division=None):
        """
        Updates the judge table for a given tournament

        Args:
            tournament_name (str): The name of the tournament.
            division (str): The division to update (e.g., 'Novice', 'Varsity').
            round_num (str): The round number to update (e.g., 'Round 1', 'Round 2').

        Returns:
            pd.DataFrame: The updated postings table DataFrame.
                Returns a DataFrame with a message if tournament name, division, or round number is missing.
        """
        try:
            logger.info(f"Updating judge table for tournament: {tournament_name}")

            # Check if required parameters are provided
            if not tournament_name :
                logger.warning("Tournament name, not provided")
                return pd.DataFrame({"Message": ["Tournament name not provided."]})

            # Retrieve tournament data from the database
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})

            if not data:
                logger.error(f"No tournament data found for tournament: {tournament_name}")
                return pd.DataFrame({"Message": [f"No tournament data found for tournament: {tournament_name}"]})

            judges = pd.DataFrame(data['Judges'])
            
            if division is not None and round_num is not None:
                debates = data['Tournament'][division][round_num]
                judge_ids = debates['Judge_ID']
                
                judges = judges[judges['ID'].isin(judge_ids)]
                
            elif division is not None:
                debates = data['Tournament'][division]
                judge_ids = set()
                
                for dbt_round in debates.keys():
                    ids = debates[dbt_round]['Judge_ID']
                    
                    for id in ids:
                        if isinstance(id, int):
                            judge_ids.add(id)
                        else:
                            for judge in id:
                                judge_ids.add(judge)
                judges = judges[judges['ID'].isin(judge_ids)]
            return judges
        except Exception as e:
            logger.error(f"Error updating postings table for tournament: {tournament_name}, division: {division}, round number: {round_num}, Error: {e}")
            return pd.DataFrame({"Error": [f"Error updating postings table: {e}"]})
    
    def update_active_round(self, tournament_name: str, round_num: str) -> bool:
            """
            Update the active round for a given tournament.

            Args:
                tournament_name (str): The name of the tournament.
                round_num (str): The round number to be set as the active round.

            Returns:
                bool: True if the active round was updated successfully.

            Raises:
                Exception: If there is an error during the database operations.
            """
            try:
                # Check if the active round already exists in the tournament document
                active_round_entry = self.db.find_one_document(
                    collection_name="Tournaments",
                    query={"Tournament Name": tournament_name, "Active Round": round_num}
                )
                
                if active_round_entry is None:
                    logger.info(f"{round_num} set as active round for tournament: {tournament_name}, Active Round Created")
                    
                    # Create the active round entry
                    self.db.add_document_entry(
                        collection_name="Tournaments",
                        query={"Tournament Name": tournament_name},
                        new_field="Active Round",
                        new_value=round_num
                    )
                else:
                    logger.info(f"{round_num} set as active round for tournament: {tournament_name}, Active Round Updated")
                    
                    # Update the existing active round entry
                    self.db.update_document(
                        collection_name="Tournaments",
                        query={"Tournament Name": tournament_name},
                        update_data={"Active Round": round_num}
                    )
                    
                return True
            except Exception as e:
                logger.error(f"Error updating active round for tournament '{tournament_name}': {e}")
                raise
            
    
    
    def notify_judges_of_ballots(self, tournament_name: str) -> None:
        """
        Notify judges about available ballots for the active round of a tournament.

        Args:
            tournament_name (str): The name of the tournament.

        Raises:
            ValueError: If the tournament name is not found in the database or if there are issues sending emails.
        """
        elims = ("Triple Octo Finals", "Double Octo Finals", "Octo Finals", "Quarter Finals", "Semifinals", "Finals")
        
        try:
            data = self.db.find_one_document(collection_name="Tournaments", query={"Tournament Name": tournament_name})
            
            if not data:
                raise ValueError(f"Tournament '{tournament_name}' not found in the database.")

            active_round = data.get('Active Round')
            
            if not active_round:
                raise ValueError(f"No active round found for tournament '{tournament_name}'.")
            
            logger.info(f"Sending emails for {tournament_name}, active round: {active_round}")
            
            judge_ids = data['Tournament']['Novice'][active_round]['Judge_ID']
            if active_round in elims:
                judge_ids = [item for sublist in judge_ids for item in sublist]

            judges_df = pd.DataFrame(data['Judges'])

            judges_df = judges_df[judges_df['ID'].isin(judge_ids)]
            judges_df.drop("ID", axis=1, inplace=True)
            judges_df.dropna(subset=['Email'], inplace=True)
            judges = judges_df.to_dict(orient='records')
            
            self.email.login()
            for judge in judges:
                email_body = f"{judge['School']} {judge['Last Name']}'s ballot for {active_round} is available at (website)."  # TODO: Replace with actual website URL
                self.email.send_email(subject="Ballot Notification", recipient=judge['Email'], body=email_body)
            self.email.logout()
        
        except Exception as e:
            logger.error(f"Error notifying judges of ballots: {e}")
            raise

                                        