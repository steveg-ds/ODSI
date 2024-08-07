import re
import pandas as pd
import random
from faker import Faker # library for making fake text data 
from logger_config import logger
from db import DB

class Model:
    """
    Class representing the model for the debate judging system.
    Handles database operations and input validation.
    """

    def __init__(self, db):
        """
        Initialize the Model instance with a database connection.
        
        Parameters:
        - db (object): An object representing the database connection.
        """
        # Initialize instance variables
        self._aff_id = None
        self._neg_id = None

        self._division = None
        
        self._aff_name = None
        self._aff_full_name = None
        self._aff_school = None
        
        self._neg_name = None
        self._neg_full_name = None
        self._neg_school = None
        
        self._judge_name = None
        self._judge_full_name = None
        self._judge_school = None
        self._judge_id = None 
        
        self._tournament_name = None
        self._active_round = None
        
        # TODO: add self._room, self_division to model instance variables

        # Set the database connection
        self.db = db
        
        self.set_active_tournament() # set active tournament when app is started
        
        # Create properties dynamically
        self.create_properties(
            "aff_id", "neg_id",  "division",
            "aff_name", "aff_full_name",  "aff_school", "neg_name", "neg_full_name", "neg_school", "judge_name", "judge_full_name", "judge_school", "judge_id", "active_tournament", "active_round"
        )

    @staticmethod
    def log_call(func):
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} called")
            return func(*args, **kwargs)
        return wrapper

    @log_call
    def create_properties(self, *attributes):
        # Dynamically create properties for each attribute
        for attr in attributes:
            # Define getter and setter methods within a helper function
            def make_property(attr):
                def getter(self):
                    return getattr(self, f"_{attr}")

                def setter(self, value):
                    setattr(self, f"_{attr}", value)

                return property(getter, setter)

            # Create property on the current class (type(self))
            setattr(type(self), attr, make_property(attr))
    
    @log_call
    def signup_user(self, firstname, lastname, school, email, username, password):
        """
        Validate user signup information and insert user into the database if validation passes.

        Parameters:
        - firstname (str): First name of the user.
        - lastname (str): Last name of the user.
        - school (str): School or organization of the user.
        - email (str): Email address of the user.
        - username (str): Username chosen by the user.
        - password (str): Password chosen by the user.

        Returns:
        - str: Error message if validation fails, empty string if successful.
        """
        # Type checking
        if not all(isinstance(arg, str) for arg in (firstname, lastname, school, email, username, password)):
            raise TypeError("All arguments must be strings.")

        # Define the regex patterns
        username_pattern = r"^[a-zA-Z0-9]{3,}$"
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Check each condition
        if len(firstname) == 0:
            return "First name cannot be empty."
        elif len(lastname) == 0:
            return "Last name cannot be empty."
        elif len(school) != 3:
            return "School must be exactly 3 characters long."
        elif not re.match(email_pattern, email):
            return "Invalid email format."
        elif not re.match(username_pattern, username):
            return "Username must be at least 3 characters long and contain no special characters."
        elif len(password) < 6:
            return "Password must contain at least 6 characters."

        # Check if username already exists
        user = self.db.find_one_document(collection_name="Users", query={"username": username})

        if user is not None:
            logger.info(f"Username '{username}' already exists.")
            return "Username already exists."

        
        # Prepare user data for insertion
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "firstname": firstname,
            "lastname": lastname,
            "school": school
        }

        try:
            # Insert user data into the database collection 'users'
            self.db.insert_document(collection_name='Users', document=user_data)

            # Log successful user insertion
            logger.info(f"User '{username}' inserted into database")
            
            return ""

        except TypeError as e:
            # Log and raise TypeError for incorrect argument types
            logger.error(f"TypeError in signup_user: {e}")
            raise

        except Exception as e:
            # Log and handle unexpected exceptions
            logger.error(f"Exception in signup_user: {e}")
            raise

        # If all checks pass, return empty string (no errors)
        logger.info(f"Valid signup for user '{username}'.")
        return ""

    @log_call
    def validate_login(self, username, password):
        """
        Validate user login credentials and retrieve associated debate information if valid.

        Parameters:
        - username (str): Username provided by the user for login.
        - password (str): Password provided by the user for login.

        Returns:
        - tuple: (dict or None, str) Dictionary containing debate information if login is successful, None otherwise.
                Status message indicating the result.
        """

        # Ensure username and password are strings
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("Username and password must be strings.")

        # Query the database for user data
        query = {"username": username, "password": password}
        data = self.db.find_one_document(collection_name="Users", query=query)

        logger.info(data)

        if data:
            # Retrieve debate information if user data is found
            debate = self.set_round_info(judge=data)
            print(f"Debate for current round and judge {self._judge_name}: {debate}")
            if debate is not None:
                logger.info(f"Login successful for user: {username}")
                return debate, "close modal"
            else:
                logger.info(f"Login successful for user: {username} but they have no ballot")
                return None, "no ballot"
        else:
            logger.warning(f"Login failed for user: {username}")
            return None, "invalid credentials"
    
    @log_call
    def set_round_info(self, judge):
        
        # TODO: this needs to gracefully handle when active tournament = none, basically popup a modal telling the user that there is no currently active tournament 
        
        first_name = judge['firstname']
        last_name = judge['lastname']
        school = judge['school']
        
        # get tournament data and create judges dataframe
        data = self.db.find_one_document(collection_name="Tournaments", query={'Tournament Name': self._active_tournament})
        
        judges = pd.DataFrame(data['Judges'])
        judge = judges.loc[(judges['First Name'] == first_name) & 
                                (judges['Last Name'] == last_name) & 
                                (judges['School'] == school)]

        if judge.empty:
            return None
        
        judge = judge.to_dict(orient='records')[0]
        
        if self._active_round is None:
            self.set_active_round(tournament_name=self._active_tournament)

        judge_id = judge['ID']
        
        dbt_rnds = pd.DataFrame(data['Tournament']['Novice']['Round 1'])
        dbt_rnd = dbt_rnds[dbt_rnds['Judge_ID'] == judge_id]

        if dbt_rnd.empty:
            raise ValueError(f"No round information found for judge: {first_name} {last_name}, {school}")

        debaters = pd.DataFrame(data['Debaters'])

        aff = debaters.loc[debaters['ID'].isin(dbt_rnd['Aff_ID'])].to_dict(orient='records')[0]
        neg = debaters.loc[debaters['ID'].isin(dbt_rnd['Neg_ID'])].to_dict(orient='records')[0]

        self._aff_id = aff['ID']
        self._neg_id = neg['ID']
        
        self._division = aff['Division']
        
        self._aff_name = aff['School'] + " " + aff['Last Name']
        self._neg_name = neg['School'] + " " + neg['Last Name']
        
        self._aff_full_name = aff['First Name'] + " " + aff['Last Name']
        self._neg_full_name = neg['First Name'] + " " + neg['Last Name']
        
        self._aff_school = aff['School']
        self._neg_school = neg['School']
        self._judge_school = judge['School']
        
        self._judge_full_name = judge['First Name'] + " " + judge['Last Name']
        
        self._judge_id = judge['ID']
        
        self._judge_name = judge['School'] + " " + judge['Last Name']
        
        
        
        self._room = dbt_rnd.iloc[0]['Room']
        
        
        debate = {
            "Affirmative": self._aff_name,
            "Negative": self._neg_name,
            "Judge": self._judge_name,
            "Room": self._room,
            "Round Number": self._active_round,
            "Tournament Name": self._active_tournament,
            "Division": self._division
        }
        
        return debate
        
        # except Exception as e:
        #     logger.error(f"Error in get_round_info: {e}")
        #     raise
    
    @log_call
    def update_round_info(self, debate):
        # Extract relevant information from the debate object
        
        judge_name = f"Judge: {debate.get('Judge', '')}"
        affirmative_name = f"Affirmative: {debate.get('Affirmative', '')}"
        negative_name = f"Negative: {debate.get('Negative', '')}"
        round_number = debate.get('Round Number', '')
        tournament_name = debate.get('Tournament Name', '')

        # Return updated values upon successful login
        return affirmative_name, negative_name, judge_name, round_number, tournament_name, False
        
    @log_call
    def calculate_speaker_points(self, delivery, courtesy, tone, organization, logic, support, cx, refutation):
        """
        Calculates speaker points based on input criteria.

        Args:
            delivery (int): Score for delivery.
            courtesy (int): Score for courtesy.
            tone (int): Score for tone.
            organization (int): Score for organization.
            logic (int): Score for logic.
            support (int): Score for support.
            cx (int): Score for cross-examination.
            refutation (int): Score for refutation.

        Returns:
            int: Calculated speaker points if all inputs are valid, otherwise None.
        """
        try:
            # Ensure each input is an integer and within the valid range
            speaks = {
                'delivery': int(delivery) if delivery is not None else 0,
                'courtesy': int(courtesy) if courtesy is not None else 0,
                'tone': int(tone) if tone is not None else 0,
                'organization': int(organization) if organization is not None else None,
                'logic': int(logic) if logic is not None else 0,
                'support': int(support) if support is not None else None,
                'cx': int(cx) if cx is not None else 0,
                'refutation': int(refutation) if refutation is not None else 0
            }

            # Validate each input
            for key, value in speaks.items():
                if value is not None and not (1 <= value <= 5):
                    logger.error(f"Invalid value for {key}: {value}. Value must be between 1 and 5.")
                    return None

            # Perform calculations (example calculation)
            speaker_points = sum(speaks.values())
            logger.info(f"Calculated speaker points: {speaker_points}")
            return speaker_points
        
        except Exception as e:
            logger.error(f"Error in calculate_speaker_points: {e}")
            return None
        
    @log_call
    def check_ballot_fields(self, ballot):
        # Identify missing fields
        missing_fields = [field for field, value in ballot.items() if not value]
        
        # Return the list of missing fields if any, else return None
        return missing_fields if missing_fields else None
    
    @log_call
    def check_lpw(self, ballot):
        # TODO: this function is not currently implemented because I couldn't make it work with one callback, maybe with a second callback I can make it work
        
        aff_speaks = ballot['Affirmative Speaks']
        neg_speaks = ballot['Negative Speaks']
        
        if ballot['Winning Side'] == "Affirmative" and aff_speaks < neg_speaks:
            print(f"Affirmative Low Point Win: \nAff Speaks: {aff_speaks} \nNeg Speaks: {neg_speaks}")
            return "Affirmative"
        
        elif ballot['Winning Side'] == "Negative" and neg_speaks < aff_speaks:
            print(f"Negative Low Point Win: \nNeg Speaks: {neg_speaks} \nAff Speaks: {aff_speaks} ")
            return "Negative"
        else:
            return None
            
    def validate_judge_name(self, ballot):
        print(ballot['Judge Name'], self._judge_name, self._judge_full_name)

        if ballot['Judge Name'] != self._judge_name and ballot['Judge Name'] != self._judge_full_name:
            logger.info("Judge name validated successfully.")
            return True
        
        return False
        
    def validate_judge_school(self, ballot):
        if ballot['Judge School'] != self._judge_school:
            return True
        
        logger.info("Judge school validated successfully.")
        return False
    
    def validate_winner_name(self, ballot):
        
        if ballot['Winning Side'] == "Affirmative":
            competitor_names = [self._aff_name, self._aff_full_name]
        else:
            competitor_names = [self._neg_name, self._neg_full_name]
            
        if ballot['Competitor Name'] not in competitor_names:
            logger.info("Invalid competitor name.")
            return True
        
        
        logger.info("Winner name validated successfully.")
        return False

        
    def validate_winner_school(self, ballot):
        if ballot['Winning Side'] == "Affirmative":
            competitor_school = self._aff_school
        else:
            competitor_school = self._neg_school
            
        if ballot['Competitor School'] != competitor_school:
            logger.info("Invalid competitor school.")
            return True
        
        
        logger.info("Winner school validated successfully.")
        return False
    
    @log_call
    def submit_ballot(self, ballot):
        # NOTE: keep this data structure simple for easy filtering for sending out ballots and natural language processing (make it a pandas dataframe and filter it as needed)

        try:
            self.db.insert_document(collection_name='Ballots', document=ballot)
            logger.info("Ballot submitted successfully.")
            return True
        
        except Exception as e:
            logger.error(f"Error in submit_ballot: {e}")
            return False
    
    @log_call
    def set_active_round(self, tournament_name):
        active_round = self.db.find_one_document(
                    collection_name="Tournaments",
                    query={"Tournament Name": tournament_name})
        self._active_round = active_round = active_round['Active Round']
        
        logger.info(f"Active round set to: {self._active_round}")
        
    @log_call  
    def set_active_tournament(self):
        active_tournament = self.db.find_documents(
                collection_name="Tournaments",
                query={"Active Tournament": {"$exists": True}}
            )
        
        if active_tournament is not None:
            self._active_tournament = active_tournament[0]['Active Tournament']
            
            
            logger.info(f"Active tournament set to: {self._active_tournament}")
        else:
            logger.error("No active tournament found.")
            

#____________________________________________________________________________________
# Test Model Code
#____________________________________________________________________________________


# model=Model(DB())

# fake = Faker()

# users = model.db.find_documents(collection_name="Users")
# user = users[0]

# model.set_round_info(user) # set round info for user

# winner = random.choice(("Aff", "Neg"))

# judge_name = model.judge_full_name
# judge_school = model.judge_school

# if winner == "Aff":
#     vote_radio = "Affirmative"
#     competitor_name = model.aff_full_name
#     competitor_school = model.aff_school
# else:
#     vote_radio = "Negative"
#     competitor_name = model.neg_full_name
#     competitor_school = model.neg_school


# ballot = {
#     "Resolution": fake.sentence(10),
#     "Affirmative Speaks": random.choice(range(30,41)),
#     "Affirmative Comments": fake.sentence(10),
#     "Negative Speaks": random.choice(range(30,41)),
#     "Negative Comments": fake.sentence(10),
#     "Competitor Name": "Your Mom",
#     "Competitor School": competitor_school,
#     "Tabula Rasa Checklist": True,
#     "Judge Name": judge_name,
#     "Judge School": judge_school,
#     "Reason for Decision": fake.sentence(10),
#     "Winning Side": vote_radio
# }

# model.validate_winner_name(ballot)

# ### load in test data and get tournament data
# debaters = pd.read_csv('data/debaters.csv')
# judges = pd.read_csv('data/judges.csv')
# rooms = pd.read_csv('data/rooms.csv')




# data = model.db.find_one_document(collection_name="Tournaments", query={'Tournament Name': model._active_tournament}) # get tournament data from db
# # print(data)

# debates = pd.DataFrame(data['Tournament'][model.division][model.active_round])


# debate = debates.loc[debates['Judge_ID'] == model.judge_id]
# debate = debate.to_dict('records')[0]

# debaters = pd.DataFrame(data['Debaters'])

# judges = pd.DataFrame(data['Judges'])


### code to test validate signup 

# model = Model(DB())
# users = model.db.find_documents(collection_name="users")
# # print(users)
# user = random.choice(users)
# print("Selected User:", user)

# judge = random.choice(judges.to_dict(orient='records'))
# print("Selected Judge:", judge)

# first_name = judge['First Name'] + "asd"
# last_name = judge['Last Name'] + "sdf"
# school = judge['School']
# email = "over.baked.potatoes.420@gmail.com"
# username = f"{first_name[0].lower()}{last_name.lower()}"
# password = "p@ssw0rd"

# x = model.signup_user(firstname=first_name, lastname=last_name, email=email, password=password, school=school, username=username)

# ### test submit_ballot function ###
# fake = Faker()

# aff_speaks = random.choice(range(30,41))
# aff_comments = fake.sentence(nb_words=10)

# neg_speaks = random.choice(range(30,41))
# neg_comments = fake.sentence(nb_words=10)

# rfd = fake.sentence(10)

# judge = judges.loc[judges['ID'] == debate['Judge_ID']].to_dict('records')[0]

# judge_full_name = judge['First Name'] + " " + judge['Last Name']
# judge_name = judge['School'] + " " + judge['Last Name']
# judge_school = judge['School']


# aff = debaters.loc[debaters['ID'] == debate['Aff_ID']].to_dict('records')[0]
# neg = debaters.loc[debaters['ID'] == debate['Neg_ID']].to_dict('records')[0]


# competitor_name = model.neg_name

# competitor_school = competitor_name.split(' ')[0]

# winner='negative'

# acknowledge_chk = True

# model.submit_ballot(aff_speaks=aff_speaks, aff_comments=aff_comments, neg_speaks=neg_speaks, neg_comments=neg_comments, rfd=rfd, winner=winner)


# last_ballot = model.db.find_documents(collection_name="Ballots")[-1]

# for key in last_ballot.keys():
#     print(key, ":", last_ballot[key], )

### test validate_login function ###
# model.validate_login(username=user['username'], password=user['password'])

### test calculate_speaker_points ###
# speaks = {
#     "delivery": random.choice(range(1, 6)),
#     "courtesy": random.choice(range(1, 6)),
#     "tone": random.choice(range(1, 6)),
#     "organization": random.choice(range(1, 6)),
#     "logic": random.choice(range(1, 6)),
#     "support": random.choice(range(1, 6)),
#     "cx": random.choice(range(1, 6)),
#     "refutation": random.choice(range(1, 6))
# }

# total_speaker_points = model.calculate_speaker_points(
#     delivery=speaks['delivery'],
#     courtesy=speaks['courtesy'],
#     tone=speaks['tone'],
#     organization=speaks['organization'],
#     logic=speaks['logic'],
#     support=speaks['support'],
#     cx=speaks['cx'],
#     refutation=speaks['refutation']
# )


