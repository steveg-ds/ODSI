import pandas as pd
import numpy as np
import random
from collections import deque
from collections import defaultdict
from logger_config import logger

class Tabbing:
    def __init__(self):
        self._num_prelims = None
        
        self._debaters = None
        self._judges = None
        self._rooms = None
        self._tournament_name = None
        
        self._division = "Novice"
        self.divisions =  ["Novice", "Junior Varsity", "Varsity", "Professional"]
        self._tournament = None
        
        self.data =   None
        self.all_pairs = []
        self.num_breaks = None
        self.num_elims = None
       
    def log_call(func):
        def wrapper(self, *args, **kwargs):
            logger.info(f"{func.__name__} called")
            return func(self, *args, **kwargs)
        return wrapper
    
    @property
    def num_prelims(self):
        return self._num_prelims
    
    @num_prelims.setter
    def num_prelims(self, value):
        self._num_prelims = value
        
    @property
    def division(self):
        return self._division
    
    @division.setter
    def division(self, value):
        # Add validation logic if needed
        if value not in ["Novice", "Junior Varsity", "Varsity", "Professional"]:
            raise ValueError("Invalid division. Must be one of 'Novice', 'Junior Varsity', 'Varsity', 'Professional'.")
        self._division = value
        
    @property
    def tournament(self):
        return self._tournament
    
    @tournament.setter
    def tournament(self, value):
        self._tournament = value
        
    @property
    def debaters(self):
        return self._debaters
    
    @debaters.setter
    def debaters(self, value):
        self._debaters = value
        
    @property
    def rooms(self):
        return self._rooms
    
    @rooms.setter
    def rooms(self, value):
        self._rooms = value
    
    @property
    def judges(self):
        return self._judges
    
    @judges.setter
    def judges(self, value):
        self._judges = value
    
    @property
    def tournament_name(self):
        return self._tournament_name
        
    @tournament_name.setter
    def tournament_name(self, value):
        self._tournament_name = value
        
    # TODO: i don't think this gets used but i'm going to leave it for now 
    # def create_data_df(self):
    #     self.data = pd.DataFrame(self.divisions[self._division])
    
    @log_call
    def create_divisions(self):
        """
        Create divisions and organize debaters into respective divisions.

        Raises:
            ValueError: If debaters object (_debaters) is None.

        Returns:
            dict: Dictionary containing divisions with organized debaters.
        """
        try:
            if self._debaters is None:
                raise ValueError("Debaters object not created")

            divisions = {
                "Novice": [],
                "Junior Varsity": [],
                "Varsity": [],
                "Professional": []
            }

            # Assign IDs to debaters and organize into divisions
            for debater in self._debaters:
                division = debater['Division']
                if division in divisions:
                    divisions[division].append(debater)

            # Ensure each division has an even number of debaters or add BYE entry
            bye_entry = {
                'First Name': 'BYE',
                'Last Name': 'BYE',
                'School': 'BYE',
                'Division': '',
                "ID": 0  # Adjust this ID as needed
            }
            for division, debaters in divisions.items():
                if len(debaters) % 2 != 0:
                    bye_entry['Division'] = division  # Set the division for the BYE entry
                    divisions[division].append(bye_entry.copy())

            self.divisions = divisions
            logger.info("Divisions object created")

            return divisions

        except Exception as e:
            logger.error(f"Error creating divisions: {e}")
            raise  # Re-raise the exception for higher-level handling
        

    @log_call
    def create_tournament_structure(self):
        """
        Creates a tournament structure with rounds and columns for each division.

        Returns:
            dict: Dictionary representing the tournament structure with divisions, rounds, and columns.
        """
        try:
            divs = ["Novice", "Junior Varsity", "Varsity", "Professional"]
            rounds = [f"Round {i}" for i in range(1, self.num_prelims + 1)]
            columns = ['Aff_ID', 'Aff_Speaks', 'Neg_ID', 'Neg_Speaks', 'Judge_ID', 'Win', 'Room']

            # Initialize an empty dictionary for tournament columns
            tournament = {}

            # Loop through each division
            for division in divs:
                division_dict = {}
                # Loop through each round within the division
                for round_name in rounds:
                    round_dict = {}
                    # Loop through each column name and initialize it to None
                    for col in columns:
                        round_dict[col] = None
                    division_dict[round_name] = round_dict
                tournament[division] = division_dict

            self._tournament = tournament
            logger.info("Tournament object created")

            return tournament

        except Exception as e:
            logger.error(f"Error creating tournament structure: {e}")
            raise  # Re-raise the exception for higher-level handling

    def fix_invalid_pairs(self, invalid_pairs):
        for round_no, debater, opponent in invalid_pairs:
            affs = deque(self._tournament[self._division][f"Round {round_no}"]['Aff_ID'])
            negs = deque(self._tournament[self._division][f"Round {round_no}"]['Neg_ID'])
            for i in range(len(affs)):
                aff = affs[i]
                neg = negs[i]
                if aff == debater or neg == debater:
                    for j in range(len(affs)):
                        if i == j:
                            continue
                        aff_swap = affs[j]
                        neg_swap = negs[j]
                        if self.can_pair(aff, neg_swap) and self.can_pair(aff_swap, neg):
                            affs[i], affs[j] = affs[j], affs[i]
                            negs[i], negs[j] = negs[j], negs[i]
                            break
            self._tournament[self._division][f"Round {round_no}"]['Aff_ID'] = list(affs)
            self._tournament[self._division][f"Round {round_no}"]['Neg_ID'] = list(negs)

    @log_call
    def can_pair(self, aff, neg):
        """
        Checks if two debaters can be paired based on school affiliation and existing invalid pairings.

        Args:
            aff (int): ID of the affirmative debater.
            neg (int): ID of the negative debater.

        Returns:
            bool: True if the debaters can be paired, False otherwise.
        """
        try:
            # Retrieve schools for the affirmative and negative debaters
            aff_school = self.data.loc[self.data['ID'] == aff, 'School'].values[0]
            neg_school = self.data.loc[self.data['ID'] == neg, 'School'].values[0]

            # Retrieve invalid pairings where the negative debater is already paired with the affirmative debater
            invalid_negs = [pair[0] for pair in self.all_pairs if pair[1] == aff]

            # Check conditions for pairing: different schools and negative debater not in invalid pairings
            return aff_school != neg_school and neg not in invalid_negs
        
        except IndexError:
            logger.error(f"Debater ID not found in data: aff={aff}, neg={neg}")
            return False  # Return False if debater ID is not found in the data
        
        except Exception as e:
            logger.error(f"Error checking pair: {e}")
            return False  # Return False for any other unexpected errors
    @log_call
    def pair_prelims_flight_a(self, division=None):
        """
        Pair debaters for preliminary rounds (flight A) in a debate tournament.
        """
        def swap_and_pair(affs, negs, aff, neg):
            # TODO: Swap and pair needs to be made a class function because flights a and b use it 
            swap_found = False
            for i in range(len(affs)):
                temp_aff = affs[i]
                temp_neg = negs[i]
                if self.can_pair(temp_aff, neg) and self.can_pair(aff, temp_neg):
                    affs[i] = aff
                    negs[i] = neg
                    aff_pair.append(temp_aff)
                    neg_pair.append(temp_neg)
                    swap_found = True
                    logger.info(f"Swapped and Paired: Aff={temp_aff} with Neg={neg}, and Aff={aff} with Neg={temp_neg}")
                    break
            return swap_found

        if division:
            self._division = division
            
        self.data = pd.DataFrame(self.divisions[division])
        
        for round_no in range(1, self.num_prelims + 1):
            current_round = f"Round {round_no}"
            prev_round = f"Round {round_no - 1}"
            
            if round_no == 1:
                # Random pairing for the first round
                debaters = self.data.to_dict(orient='records')
                debaters = deque(debaters)
                affs = []
                negs = []
                
                while debaters:
                    aff = debaters.popleft()
                    
                    # Exclude debaters from the same school as the aff
                    valid_negs = [debater for debater in debaters if debater['School'] != aff['School']]
                    
                    if not valid_negs:
                        # If no valid negs are found, re-add the aff back to the deque and continue
                        debaters.append(aff)
                        continue
                    
                    # Randomly select a neg from valid_negs
                    neg = random.choice(valid_negs)
                    
                    # Remove the selected neg from debaters
                    debaters.remove(neg)
                    
                    affs.append(aff['ID'])
                    negs.append(neg['ID'])
                    
                rooms = random.sample(self._rooms, len(affs))
                self._tournament[self._division][current_round] = {
                    'Aff_ID': affs,
                    "Aff_Speaks": [random.choice(range(30, 41)) for _ in range(len(affs))],
                    'Neg_ID': negs,
                    "Neg_Speaks": [random.choice(range(30, 41)) for _ in range(len(affs))],
                    "Judge_ID": None,
                    'Room': rooms,
                    'Win': [random.choice([0, 1]) for _ in range(len(affs))]
                }
                logger.info(f"Flight A {current_round}, {division} pairing successful!")
                
                continue
                    
                
            self.all_pairs = []
            for r in range(1, round_no):
                round_pairs = [[aff_id, neg_id] for aff_id, neg_id in zip(self._tournament[self._division][f"Round {r}"]['Aff_ID'], self._tournament[self._division][f"Round {r}"]['Neg_ID'])]
                self.all_pairs.extend(round_pairs)

            max_iterations = 100
            paired_successfully = False

            while not paired_successfully:
                prev_negs = self._tournament[self._division][prev_round]['Neg_ID']
                prev_affs = self._tournament[self._division][prev_round]['Aff_ID']
                random.shuffle(prev_negs)
                random.shuffle(prev_affs)

                affs = deque(prev_affs)
                negs = deque(prev_negs)

                aff_pair = []
                neg_pair = []
                its = 0

                while len(aff_pair) < len(self._tournament[self._division][prev_round]['Aff_ID']) and its < max_iterations:
                    its += 1
                    aff = affs.popleft()
                    neg = negs.pop()

                    if self.can_pair(aff, neg):
                        aff_pair.append(aff)
                        neg_pair.append(neg)
                    else:
                        if not swap_and_pair(affs, negs, aff, neg):
                            affs.append(aff)
                            negs.appendleft(neg)
                            logger.info(f"Invalid: Aff={aff} vs Neg={neg}, affs remaining {len(affs)}, negs remaining: {len(negs)}")

                if len(aff_pair) == len(self._tournament[self._division][prev_round]['Aff_ID']):
                    paired_successfully = True
                else:
                    logger.info("Reached max iterations, restarting...")

            logger.info(f"Iterations to Complete Pairing: {its}")

            if round_no % 2 == 0:
                self._tournament[self._division][current_round]['Aff_ID'] = neg_pair
                self._tournament[self._division][current_round]['Neg_ID'] = aff_pair
            else:
                self._tournament[self._division][current_round]['Aff_ID'] = aff_pair
                self._tournament[self._division][current_round]['Neg_ID'] = neg_pair
                

            # TODO: eventually i need to remove the random generation but for now the spoof data is beneficial
            
            self._tournament[self._division][current_round]['Aff_Speaks'] = [random.choice(range(30,41)) for _ in range(len(self._tournament[self._division][current_round]['Aff_ID']))]
            self._tournament[self._division][current_round]['Neg_Speaks'] = [random.choice(range(30,41)) for _ in range(len(self._tournament[self._division][current_round]['Aff_ID']))]
            self._tournament[self._division][current_round]['Room'] = random.sample(self._rooms, len(self._tournament[self._division][current_round]['Aff_ID']))
            self._tournament[self._division][current_round]['Win'] = [random.choice([0, 1]) for _ in range(len(self._tournament[self._division][current_round]['Aff_ID']))]
            
            
            
            logger.info(f"Flight A {current_round}, {division} pairing successful!")
    
    @log_call
    def add_judges_flight_a(self, division, debaters, judges, rooms, num_prelims, tournament):
        # Initialize the already_judged dictionary
        judge_dict = defaultdict(list)
        
        # Create a list of all debate rounds
        rounds = [f"Round {round_num}" for round_num in range(1, num_prelims + 1)]
        
        # Create a list to store each judge's number of assignments
        judge_assignments = defaultdict(int)
        
        for current_round in rounds:
            debates = tournament[division][current_round]
        
            debaters_df = pd.DataFrame(debaters)
            debaters_df = debaters_df.loc[debaters_df['Division'] == division]
            
            affs = debaters_df[debaters_df['ID'].isin(debates['Aff_ID'])]
            negs = debaters_df[debaters_df['ID'].isin(debates['Neg_ID'])]
            
            # Extract schools from affirmative and negative debaters
            aff_schools = affs['School'].tolist()
            neg_schools = negs['School'].tolist()
            
            # Zip the schools together
            schools = list(zip(aff_schools, neg_schools))
            
            # List of debate IDs for tracking
            ids = list(zip(affs['ID'].tolist(), negs['ID'].tolist()))
        
            judge_ids = []
            
            used_judges = []
            
            for debate_index in range(len(schools)):
                aff_id, neg_id = ids[debate_index]
                aff_school, neg_school = schools[debate_index]
                
                valid_judge_found = False
                tried_judges = 0
                
                while not valid_judge_found and tried_judges <= len(judges):
                    judge = random.choice(judges)
                    tried_judges += 1
                    
                    # Ensure the judge is not from the same school as debaters and hasn't judged them before
                    if judge['School'] not in (aff_school, neg_school):
                        if judge['ID'] not in judge_dict.keys() or (aff_id not in judge_dict[judge['ID']] and neg_id not in judge_dict[judge['ID']]):
                            if judge_assignments[judge['ID']] < num_prelims:  # Check if judge has not reached max assignments
                                valid_judge_found = True
                
                if valid_judge_found:
                    judge_ids.append(judge['ID'])
                    used_judges.append(judge)
                    judge_dict[judge['ID']].extend([aff_id, neg_id])
                    judge_assignments[judge['ID']] += 1
                else:
                    print(f"Unable to find a valid judge for debate {debate_index} in {current_round}.")
            
            tournament[division][current_round]['Judge_ID'] = judge_ids
        # print(judge_assignments, sum(judge_assignments.values()))
        return tournament
      
    @log_call
    def rank_debaters(self, tournament, division, num_rounds, elim_rounds=None):
        
            # Initialize ranks with defaultdict
        ranks = {
            "Wins": defaultdict(int),
            "Speaks": defaultdict(list)
        }
        
        # Generate the list of debate rounds
        debate_rounds = [f"Round {i}" for i in range(1, num_rounds + 1)]
        
        if elim_rounds is not None:
            debate_rounds.extend(elim_rounds)
            print(debate_rounds)
        
        # add Out Rounds to ranks if outround has already happened
        if len(elim_rounds) > 1:
            ranks['Out Rounds'] = defaultdict(int)
        
        # Iterate over each round
        for round_num in debate_rounds:
            if round_num in tournament[division]:
                dbt_rnd = tournament[division][round_num]
                for i, aff_id in enumerate(dbt_rnd['Aff_ID']):
                    ranks["Wins"][aff_id] += dbt_rnd['Win'][i]
                    if dbt_rnd['Aff_Speaks'][i] != 0:
                        ranks["Speaks"][aff_id].append(dbt_rnd['Aff_Speaks'][i])
                    if len(elim_rounds) > 1 and round_num in elim_rounds: # set out round status to 1 is win else 0
                        ranks["Out Rounds"][aff_id] = dbt_rnd['Win'][i]
                for i, neg_id in enumerate(dbt_rnd['Neg_ID']):
                    ranks["Wins"][neg_id] += 1 - dbt_rnd['Win'][i]
                    if dbt_rnd['Neg_Speaks'][i] != 0:
                        ranks["Speaks"][neg_id].append(dbt_rnd['Neg_Speaks'][i])
                    if len(elim_rounds) > 1 and round_num in elim_rounds: # set out round status to 1 is win else 0
                        ranks["Out Rounds"][neg_id] = 1 - dbt_rnd['Win'][i]
        
        # Convert defaultdict back to dict for the final output
        ranks = {key: dict(value) if isinstance(value, defaultdict) else value for key, value in ranks.items()}
        
        return ranks
    @log_call
    def calculate_ranks(self, tournament, division, num_rounds, elim_rounds=None, num_breaks=None):
        ranks = pd.DataFrame(self.rank_debaters(tournament, division, num_rounds, elim_rounds))
        
        if "Out Rounds" in ranks.columns:
            ranks = ranks.loc[ranks['Out Rounds'] == 1]
        
        
        ranks.reset_index(inplace=True)
        speaks = ranks['Speaks']

        ranks.drop("Speaks", axis=1, inplace=True)
        ranks['High_Low'] = speaks.apply(lambda x: sum(x) - min(x) - max(x))
        ranks['Speaks'] = speaks.apply(lambda x: sum(x[0:num_rounds]))
        ranks['Average_Speaks'] = speaks.apply(lambda x: round(sum(x) / len(x), 2) if x else 0)

        ranks['STD_Speaks'] = speaks.apply(lambda x: round(np.std(x), 2))
        
        # TODO: eventually this should include double high-low speaks once i'm done with power matching 
        
        ranks = ranks.sort_values(by=['Wins', "High_Low", "Speaks", 'Average_Speaks', "STD_Speaks"], ascending=[False, False, False, False, True])
        ranks['Rank'] = range(1, len(ranks) + 1)
        
        if num_breaks is not None:
            ranks = ranks.loc[ranks['Rank'] <= num_breaks]
            
        ranks['Opponent'] = ranks['Rank'].iloc[::-1].values
        ranks = ranks.rename(columns={"index": "ID"})
        rank_to_id = ranks.set_index('Rank')['ID'].to_dict()
        ranks['Opponent_ID'] = ranks['Opponent'].map(rank_to_id)
        
        return ranks
    
    @log_call
    def pair_elim_round(self, tournament, division, num_rounds, elim_rounds=None, num_breaks=None):
        
        
        ranks = self.calculate_ranks(tournament, division, num_rounds, elim_rounds, num_breaks)
        ranks = ranks.iloc[:len(ranks) // 2, :] # remove duplicate entries so the correct number of debaters remains

        ids = ranks[['ID', "Opponent_ID"]].values.tolist()
        
        return ranks, ids

        
    @log_call
    def calculate_breaks(self, division: str, num_debaters: int, prev_breaks=""):
        num_breaks = 0
        num_elims = 0
        elim_round = ""
        
        # Determine the number of breaks and elimination rounds based on the total number of debaters
        if num_debaters == 0:
            logger.error("Invalid Number of Breaks for Calculating Breaks")
            return None
        elif 4 <= num_debaters <= 6:
            num_breaks = 2
            elim_round = "Finals"
        elif 7 <= num_debaters <= 14:
            num_breaks = 4
            elim_round = "Semifinals"
        elif 15 <= num_debaters <= 30:
            num_breaks = 8
            elim_round = "Quarter Finals"
        elif 31 <= num_debaters <= 62:
            num_breaks = 16
            elim_round = "Octo Finals"
        elif 63 <= num_debaters <= 126:
            num_breaks = 32
            elim_round = "Double Octo Finals"
        elif num_debaters > 126:
            num_breaks = 64
            elim_round = "Triple Octo Finals"

        return elim_round, num_breaks
            
            

        
    @log_call
    def create_postings(self, division, round_no, round_data, debaters, judges, prelim=True):
        
        # Create DataFrames from the provided data
        data = pd.DataFrame(debaters)
        tournament = pd.DataFrame(round_data) 
        judges = pd.DataFrame(judges)
        
        data['Posting'] =  data['School'] +" " + data['Last Name']
        

        
        # Filter data for Affirmative and Negative teams based on IDs from tournament data
        affs = data[data['ID'].isin(tournament['Aff_ID'])]
        negs = data[data['ID'].isin(tournament['Neg_ID'])]
            

        if prelim:
            judges['Posting'] =  data['School'] +" " + data['Last Name']
            
            juds = judges[judges['ID'].isin(tournament['Judge_ID'])]
            # Reset index for concatenation and specify keys for MultiIndex
            df_concat = pd.concat([affs.reset_index(drop=True), negs.reset_index(drop=True), juds.reset_index(drop=True)], axis=1, keys=['Aff', 'Neg', 'Judge'])
            
            
            # Create a MultiIndex for columns
            columns = pd.MultiIndex.from_product([['Aff', 'Neg', 'Judge'], ["First Name", "Last Name", "School", "Posting"]])
        else:
            judge_cols = tournament['Judge_ID'].apply(pd.Series)
            judge_cols.columns = ['Judge 1', 'Judge 2', 'Judge 3']
            
            tournament = tournament.drop("Judges", axis=1).join(judge_cols)
        
            j1 = judges[judges['ID'].isin(tournament['Judge 1'])]
            j1['Posting'] = judges['School'] +" " + judges['Last Name']
            
            j2 = judges[judges['ID'].isin(tournament['Judge 2'])]
            j2['Posting'] = judges['School'] +" " + judges['Last Name']
            
            j3 = judges[judges['ID'].isin(tournament['Judge 3'])]
            j3['Posting'] = judges['School'] +" " + judges['Last Name']
            
            dfs = [affs, negs, j1, j2, j3]
            dfs = [df.reset_index(drop=True) for df in dfs]
            
            # Reset index for concatenation and specify keys for MultiIndex
            
            df_concat = pd.concat(dfs, axis=1, keys=['Aff', 'Neg', 'Judge 1', 'Judge 2', 'Judge 3'])
            
            # Create a MultiIndex for columns
            columns = pd.MultiIndex.from_product([['Aff', 'Neg', 'Judge 1', "Judge 2", "Judge 3"], ["First Name", "Last Name", "School", "Posting"]])
        
        # Reorder columns according to the MultiIndex
        posting = df_concat.reindex(columns=columns)
        # posting['Room'] = tournament[['Room']]
        return posting
        

    @log_call
    def add_elim_judges(self, round_name, debates, judges, tournament, division, num_rounds,num_judges=3):
        judge_dict = defaultdict(list)

        prelims = [f'Round {i}' for i in range(1, num_rounds + 1)]
        
        elim_rounds = [dbt_rnd for dbt_rnd in tournament[division].keys() if dbt_rnd not in prelims] # get names of eliminationo rounds

        # Populate judge_dict with past assignments
        for dbt_rnd in prelims:  # Iterate through prelim rounds
            
            # TODO: this works for the first elim but it needs to be adapted to work for panels of judges 
            
            round_debates = debates[dbt_rnd]
            debate_ids = list(zip(round_debates['Aff_ID'], round_debates['Neg_ID'], round_debates['Judge_ID']))
            
            for debate_id in debate_ids:
                judge_id = debate_id[2]  # Judge ID
                aff_id = debate_id[0]    # Affirmative ID
                neg_id = debate_id[1]    # Negative ID
                
                judge_dict[judge_id].append(aff_id)
                judge_dict[judge_id].append(neg_id)
               

        if len(elim_rounds) > 1: # make sure an outround has already happened
            for elim in elim_rounds[:-1]: 
                
                if elim in tournament[division].keys(): # make sure outround has already happened/ has been added to database 
                    # add elim round judges to judge_dict
                    elims = tournament[division][elim]
                    
                    elims = pd.DataFrame(elims)
                    # print(elims)
                    elims = elims.explode('Judge_ID')[['Judge_ID', 'Aff_ID', "Neg_ID"]].values.tolist() # [Judge_ID, Aff_ID, Neg_ID]
                
                    for elim in elims:
                        # append/ add entries to judge_dict
                        judge_dict[elim[0]].append(elim[1])
                        judge_dict[elim[0]].append(elim[2])
        
        
        # Get the current round debates
        # print(debates)
        current_round_debates = debates[round_name]
        current_round_ids = list(zip(current_round_debates['Aff_ID'], current_round_debates['Neg_ID']))
        
        panels = []
        
        # Assign judges to each debate in the current round
        for dbt_rnd in current_round_ids:
            panel = []
            attempts = 0
            while len(panel) < num_judges and attempts < 100:  # Limiting the number of attempts to avoid infinite loop
                judge = random.choice(judges)
                judge_id = judge["ID"]
                
                if judge_id in judge_dict:
                    already_judged = judge_dict[judge_id]
                    if dbt_rnd[0] in already_judged or dbt_rnd[1] in already_judged:
                        logger.info(f"Judge {judge_id} already judged one of the debaters in {dbt_rnd}")
                        attempts += 1
                        continue
                
                panel.append(judge_id)
                judge_dict[judge_id].append(dbt_rnd[0])
                judge_dict[judge_id].append(dbt_rnd[1])
                attempts = 0  # Reset attempts if a valid judge is found
            
            if len(panel) < num_judges:
                logger.warning("Unable to find enough judges for this debate.")
            
            panels.append(panel)
        tournament[division][round_name]["Judge_ID"] = panels
        # print(tournament)
        return tournament
                
    
    
# Example usage:
#random_rounds = 6  # or any stopping point you wish


#tabbing = Tabbing(random_rounds=6)
#tabbing.pair_prelims_flight_a(division="Novice")
#tabbing.pair_prelims_flight_a("Junior Varsity")
#tabbing.pair_prelims_flight_b("Varsity")
#tabbing.pair_prelims_flight_b("Professional")
#print(self._tournament)
#tabbing.pair_elim_rounds(division="Novice", num_rounds=6)
#print(tabbing.create_postings(division="Novice", round_no="Round 7")) 

