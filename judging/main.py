import dash
import dash_bootstrap_components as dbc
from flask import Flask
import os


from controller import Controller
from judging import Judging
from db import DB
from model import Model


server = Flask(__name__)

# Initialize the Dash app
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])



# Instantiate UI and Controller
ui = Judging()
controller = Controller(app=app, model=Model(DB()))

# Set up layout using UI class
app.layout = ui.layout()

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
 





 #____________________________________________________________________________________
# TODOs
#____________________________________________________________________________________

# TODO: eventually I should create a dictionary of school keys so that users can insert either their school code like LTU or the full name of the school


### short term TODOs: (by order of priority)### 


# TODO: reset ballot info when ballot is submitted successfully

# TODO: the round info for the debate is being logged twice 

# TODO: encrypt/ decrypt passwords when storing/ retrieving from database

# TODO: i've redone the way users are stored so accessing the data needs to be upated:
# user_data = {
#     "Username": username,
#     "Email": email,
#     "Password": password,
#     "First Name": firstname,
#     "Last Name": lastname,
#     "school": school
# }

# TODO: update submit ballot callback to use the general modal for everything isntead of using a bunch of different modals

# TODO: Confirm Low speaker points modal needs to be tested

# TODO: create modal to confirm judge intends for round to be a low point win

# TODO: make speaker point guide modal work 

# TODO: allow users to change password on signup modal 




