
from flask import Flask
from tournament import Tournament
from db import DB
from model import Model
from tabbing import Tabbing
from controller import Controller
from emails import EmailSender



server = Flask(__name__)

if __name__ == '__main__':
    manager = Controller(Tournament(), DB(), Model(tabbing=Tabbing(), db=DB(), email=EmailSender()), server=server)
    manager.run()

