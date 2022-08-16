from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)
app.secret_key="@#!##@%#$$#^%^$^$@!##@#@%"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:vertrigo@localhost/phongkhamdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 3


db = SQLAlchemy(app=app)


login = LoginManager(app=app)


cloudinary.config(cloud_name="drnh9htgv", api_key="538624196835262", api_secret="du3wpYdHCGQn1nKjoIkjz85g3SY")