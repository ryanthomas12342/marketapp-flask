from flask import Flask
# from market.schemas import ItemSchema,handle_validation_error
# from marshmallow import ValidationError
# from market import routes
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime, timedelta

import jwt
app = Flask(__name__)



app.config['SECRET_KEY']='03954c5efe6bffc2bdc8adf20b79c7d1303586cb'
app.config['MONGO_URI']="mongodb+srv://ryanthomas2022:jgt0Ov0Utqu2aPAq@cluster0.wdjeluq.mongodb.net/market?retryWrites=true&w=majority&appName=Cluster0"



client=PyMongo(app)
login_manager=LoginManager(app)
login_manager.login_view='login_page'

login_manager.login_message_category='info'
bcrypt=Bcrypt(app)
db=client.db

from market import routes 



